import base64
import json
import io
import re
import qrcode
from config import (
    V2RAY_ADDRESS,
    V2RAY_PORT
)

USERNAME_REGEXP = re.compile(r'^(?=\w{3,32}\b)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*$')


def share_vmess(user_id: str, username: str) -> tuple:
    """
    Returns share link and qr code respectively in tuple
    """

    v = {
        'ps': f'{V2RAY_ADDRESS} [{username}]',
        'v': '2',
        'id': str(user_id),
        'aid': '0',
        'add': V2RAY_ADDRESS,
        'port': V2RAY_PORT,
        'type': 'none',
        'tls': '',
        'net': 'ws',
        'path': '',
        'host': ''
    }
    link = "vmess://" + base64.b64encode(json.dumps(v, sort_keys=True).encode('utf-8')).decode()
    with io.BytesIO() as buffered:
        img = qrcode.make(link)
        img.save(buffered, format="PNG")
        qr = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return (link, qr)


def validate_username(username: str) -> bool:
    return bool(USERNAME_REGEXP.match(username))
