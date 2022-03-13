import sys  # nopep8
import os  # nopep8
sys.path.append(os.path.dirname(__file__))  # nopep8

from app.stats.command import command_pb2_grpc as stats_command_pb2_grpc
from app.stats.command import command_pb2 as stats_command_pb2
from app.proxyman.command import command_pb2_grpc
from app.proxyman.command import command_pb2
from app.proxyman import config_pb2 as proxyman_config_pb2
from common.serial import typed_message_pb2
from common.protocol import user_pb2
from proxy.vmess.inbound import config_pb2 as vmess_inbound_config_pb2
from proxy.vmess import account_pb2
import config_pb2 as core_config_pb2
from common.net import port_pb2, address_pb2
import errors
import grpc
from uuid import UUID


def to_typed_message(message):
    return typed_message_pb2.TypedMessage(
        type=message.DESCRIPTOR.full_name,
        value=message.SerializeToString()
    )


def ip2bytes(ip: str):
    return bytes([int(i) for i in ip.split('.')])


class Proxy(object):
    def __init__(self):
        self.message = None


class VMessInbound(Proxy):
    def __init__(self, *users: dict):
        super(VMessInbound, self).__init__()
        self.message = to_typed_message(
            vmess_inbound_config_pb2.Config(
                user=[
                    user_pb2.User(
                        email=u['email'],
                        level=u['level'],
                        account=to_typed_message(account_pb2.Account(
                            id=u['user_id'],
                            alter_id=u['alter_id']
                        ))
                    ) for u in users
                ]
            )
        )


class VMessClient(object):
    def __init__(self, address, port, default_inbound_tag=None, default_alter_id=4):
        self.errors = errors
        self._channel = grpc.insecure_channel(f"{address}:{port}")
        self._default_inbound_tag = default_inbound_tag
        self._default_alter_id = default_alter_id

    def get_all_traffic_stats(self, reset=False):
        stub = stats_command_pb2_grpc.StatsServiceStub(self._channel)
        try:
            r = stub.QueryStats(stats_command_pb2.GetStatsRequest(
                name=f"",
                reset=reset
            ))
            for stat in r.stat:
                _, email, _, _type = stat.name.split('>>>')
                yield {
                    "email": email,
                    "type": _type,
                    "value": stat.value
                }
        except grpc.RpcError:
            return None

    def get_user_traffic_downlink(self, email, reset=False):
        stub = stats_command_pb2_grpc.StatsServiceStub(self._channel)
        try:
            return stub.GetStats(stats_command_pb2.GetStatsRequest(
                name=f"user>>>{email}>>>traffic>>>downlink",
                reset=reset
            )).stat.value
        except grpc.RpcError:
            return None

    def get_user_traffic_uplink(self, email, reset=False):
        stub = stats_command_pb2_grpc.StatsServiceStub(self._channel)
        try:
            return stub.GetStats(stats_command_pb2.GetStatsRequest(
                name=f"user>>>{email}>>>traffic>>>uplink",
                reset=reset
            )).stat.value
        except grpc.RpcError:
            return None

    def add_user(self, user_id, email, level=0, alter_id=None, inbound_tag=None):
        if isinstance(user_id, UUID):
            user_id = str(user_id)
        if inbound_tag is None:
            inbound_tag = self._default_inbound_tag
        if alter_id is None:
            alter_id = self._default_alter_id
        stub = command_pb2_grpc.HandlerServiceStub(self._channel)
        try:
            stub.AlterInbound(command_pb2.AlterInboundRequest(
                tag=inbound_tag,
                operation=to_typed_message(command_pb2.AddUserOperation(
                    user=user_pb2.User(
                        email=email,
                        level=level,
                        account=to_typed_message(account_pb2.Account(
                            id=user_id,
                            alter_id=alter_id
                        ))
                    )
                ))
            ))
            return user_id
        except grpc.RpcError as e:
            details = e.details()
            if details.endswith(f"User {email} already exists."):
                raise self.errors.EmailExistsError(details, email)
            elif details.endswith(f"handler not found: {inbound_tag}"):
                raise self.errors.InboundNotFoundError(details, inbound_tag)
            else:
                raise self.errors.V2RayError(details)

    def remove_user(self, email, inbound_tag=None):
        if inbound_tag is None:
            inbound_tag = self._default_inbound_tag
        stub = command_pb2_grpc.HandlerServiceStub(self._channel)
        try:
            stub.AlterInbound(command_pb2.AlterInboundRequest(
                tag=inbound_tag,
                operation=to_typed_message(command_pb2.RemoveUserOperation(
                    email=email
                ))
            ))
        except grpc.RpcError as e:
            details = e.details()
            if details.endswith(f"User {email} not found."):
                raise self.errors.EmailNotFoundError(details, email)
            elif details.endswith(f"handler not found: {inbound_tag}"):
                raise self.errors.InboundNotFoundError(details, inbound_tag)
            else:
                raise self.errors.V2RayError(details)

    def add_inbound(self, tag, address, port, proxy: Proxy):
        stub = command_pb2_grpc.HandlerServiceStub(self._channel)
        try:
            stub.AddInbound(command_pb2.AddInboundRequest(
                inbound=core_config_pb2.InboundHandlerConfig(
                    tag=tag,
                    receiver_settings=to_typed_message(
                        proxyman_config_pb2.ReceiverConfig(
                            port_range=port_pb2.PortRange(
                                From=port,
                                To=port,
                            ),
                            listen=address_pb2.IPOrDomain(
                                ip=ip2bytes(address),
                            ),
                            allocation_strategy=None,
                            stream_settings=None,
                            receive_original_destination=None,
                            domain_override=None,
                            sniffing_settings=None
                        )
                    ),
                    proxy_settings=proxy.message
                )
            ))
        except grpc.RpcError as e:
            details = e.details()
            if details.endswith("address already in use"):
                raise self.errors.AddressAlreadyInUseError(details, port)
            else:
                raise self.errors.V2RayError(details)

    def remove_inbound(self, tag):
        stub = command_pb2_grpc.HandlerServiceStub(self._channel)
        try:
            stub.RemoveInbound(command_pb2.RemoveInboundRequest(
                tag=tag
            ))
        except grpc.RpcError as e:
            details = e.details()
            if details == 'not enough information for making a decision':
                raise self.errors.InboundNotFoundError(details, tag)
            else:
                raise self.errors.V2RayError(details)
