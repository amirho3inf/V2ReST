import re
import json
import atexit
import socket
import typing
import subprocess
from v2api import Client
from . import database as db
from .logger import logger
from config import (
    V2RAY_HOST,
    V2RAY_PORT,
    V2RAY_LOCATION_BIN,
    V2RAY_LOCATION_ASSET,
    V2RAY_API_HOST,
    V2RAY_API_PORT,
)


global process
global client


class V2rayConfig(dict):
    def __init__(self, config: typing.Union[str, dict] = {}):
        if isinstance(config, str):
            config = json.loads(config)
        super().__init__(config)

    def to_json(self):
        return json.dumps(self)

    def find_inbound(self, inbound_tag):
        for inbound in self.get('inbounds', []):
            if inbound.get('tag') == inbound_tag:
                return inbound


class V2rayCore(object):
    def __init__(self, bin_path: str, assets_path: str = ''):
        self._process = None
        self._bin_path = bin_path
        self._assets_path = assets_path

        @atexit.register
        def stop_v2ray():
            if self._process:
                self._process.terminate()

    def start(self, config: V2rayConfig):
        """
        Start v2ray server

        :raise: when server is already started :obj:`RuntimeError`
        """
        if self._process:
            raise RuntimeError('V2ray is already started')

        cmd = [self._bin_path, '-config', 'stdin:']

        self._process = subprocess.Popen(
            cmd,
            env={"V2RAY_LOCATION_ASSET": V2RAY_LOCATION_ASSET},
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        self._process.stdin.write(config.to_json().encode())
        self._process.stdin.flush()
        self._process.stdin.close()
        while output := self._process.stdout.readline().decode():
            logger.info(output.strip('\n'))
            if 'started' in output:
                break

    def stop(self):
        """
        Stop v2ray server

        :raise: when server is not started :obj:`RuntimeError`
        """
        if self._process:
            self._process.terminate()
            self._process = None
        else:
            raise RuntimeError("V2ray is not started yet")


def v2ray_is_running():
    """
    Check v2ray running with port checking
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((V2RAY_HOST, V2RAY_PORT)) == 0


def generate_db_config():
    conf = V2rayConfig({
        "log": {
            "logLevel": "debug"
        },
        "api": {},
        "stats": {},
        "inbounds": [],
        "outbounds": [],
        "policy": {
            "levels": {}
        },
        "routing": {
            "rules": []
        },
        "log": {
            "loglevel": "warning"
        }
    })

    # Add API
    conf['api']['services'] = [
        "HandlerService",
        "StatsService",
        "LoggerService"
    ]
    conf['api']['tag'] = "API"
    # Add API inbound
    conf['inbounds'].append(
        {
            "listen": V2RAY_API_HOST,
            "port": V2RAY_API_PORT,
            "protocol": "dokodemo-door",
            "settings": {
                "address": V2RAY_API_HOST
            },
            "tag": "API_INBOUND"
        }
    )
    # Add API routing rule
    conf['routing']['rules'].append(
        {
            "inboundTag": [
                "API_INBOUND"
            ],
            "outboundTag": "API",
            "type": "field"
        }
    )

    # Add default system policy
    conf['policy']['system'] = {
        "statsInboundDownlink": False,
        "statsInboundUplink": False,
        "statsOutboundDownlink": False,
        "statsOutboundUplink": False
    }

    # Add default (DIRECT & BLACKHOLE) outbounds
    conf['outbounds'].extend(
        [
            {
                "protocol": "freedom",
                "settings": {},
                "tag": "DIRECT"
            },
            {
                "protocol": "blackhole",
                "settings": {},
                "tag": "BLACKHOLE"
            }
        ]
    )

    # Add local IP's and domain routing rule
    conf['routing']['rules'].extend(
        [
            {
                "ip": [
                    "geoip:private"
                ],
                "outboundTag": "BLACKHOLE",
                "type": "field"
            },
            {
                "domain": [
                    "localhost"
                ],
                "outboundTag": "BLACKHOLE",
                "type": "field"
            }
        ]
    )

    # Add default (0) user level
    conf['policy']['levels'] = conf['policy'].get('levels') or {}
    conf['policy']['levels']['0'] = {
        "statsUserUplink": True,
        "statsUserDownlink": True
    }

    # Add user inbounds
    conf['inbounds'].append(
        {
            "listen": V2RAY_HOST,
            "port": V2RAY_PORT,
            "protocol": "vmess",
            "settings": {
                "clients": [
                    {
                        "id": user['id'],
                        "email": user['username'],
                        "level": 0
                    }
                    for user in db.get_users(only_active_users=True)
                ]
            },
            "streamSettings": {
                "network": "ws",
                "wsSettings": {
                    "path": "/"
                }
            },
            "tag": "VMESS_INBOUND"
        }
    )

    # Add user inbounds routing rule
    conf['routing']['rules'].append(
        {
            "inboundTag": [
                "VMESS_INBOUND"
            ],
            "outboundTag": "DIRECT",
            "type": "field"
        }
    )

    return conf


if not v2ray_is_running():
    process = V2rayCore(V2RAY_LOCATION_BIN, V2RAY_LOCATION_ASSET)
    config = generate_db_config()

    with open("generated_config.json", "w") as file:
        file.write(json.dumps(config, indent=4))

    process.start(config)

    if not v2ray_is_running():
        raise RuntimeError("V2ray doesn't start")


client = Client(V2RAY_API_HOST, V2RAY_API_PORT)


__all__ = [
    'process',
    'client',
    'v2ray_is_running',
    'generate_db_config',


]
