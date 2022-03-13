import grpc
import typing

from .proto.app.stats.command import command_pb2_grpc as stats_command_pb2_grpc
from .proto.app.stats.command import command_pb2 as stats_command_pb2
from .proto.app.proxyman.command import command_pb2_grpc
from .proto.app.proxyman.command import command_pb2
from .proto.app.proxyman import config_pb2 as proxyman_config_pb2
from .proto.common.protocol import user_pb2
from .proto import config_pb2 as core_config_pb2
from .proto.common.net import port_pb2, address_pb2


from . import errors
from .utils import to_typed_message, ip2bytes
from .types.common import Account, Inbound


class Client(object):
    def __init__(self, address, port):
        self._channel = grpc.insecure_channel(f"{address}:{port}")

    def get_all_traffic_stats(self, reset: bool = False) -> typing.Iterable:
        stub = stats_command_pb2_grpc.StatsServiceStub(self._channel)
        try:
            r = stub.QueryStats(stats_command_pb2.GetStatsRequest(
                name="",
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
            return

    def get_user_traffic_downlink(self, email: str, reset: bool = False) -> int:
        stub = stats_command_pb2_grpc.StatsServiceStub(self._channel)
        try:
            return stub.GetStats(stats_command_pb2.GetStatsRequest(
                name=f"user>>>{email}>>>traffic>>>downlink",
                reset=reset
            )).stat.value
        except grpc.RpcError:
            return 0

    def get_user_traffic_uplink(self, email: str, reset: bool = False) -> int:
        stub = stats_command_pb2_grpc.StatsServiceStub(self._channel)
        try:
            return stub.GetStats(stats_command_pb2.GetStatsRequest(
                name=f"user>>>{email}>>>traffic>>>uplink",
                reset=reset
            )).stat.value
        except grpc.RpcError:
            return 0

    def add_user(self,
                 email: str,
                 inbound_tag: str,
                 account: Account,
                 level: int = 0) -> bool:

        stub = command_pb2_grpc.HandlerServiceStub(self._channel)
        try:
            stub.AlterInbound(command_pb2.AlterInboundRequest(
                tag=inbound_tag,
                operation=to_typed_message(command_pb2.AddUserOperation(
                    user=user_pb2.User(
                        level=level,
                        email=email,
                        account=account.message
                    )
                ))
            ))
            return True

        except grpc.RpcError as e:
            details = e.details()

            if details.endswith(f"User {email} already exists."):
                raise errors.EmailExistsError(details, email)
            elif details.endswith(f"handler not found: {inbound_tag}"):
                raise errors.InboundNotFoundError(details, inbound_tag)
            else:
                raise errors.V2RayError(details)

    def remove_user(self, email: str, inbound_tag: str) -> bool:
        stub = command_pb2_grpc.HandlerServiceStub(self._channel)
        try:
            stub.AlterInbound(command_pb2.AlterInboundRequest(
                tag=inbound_tag,
                operation=to_typed_message(command_pb2.RemoveUserOperation(
                    email=email
                ))
            ))
            return True
        except grpc.RpcError as e:
            details = e.details()

            if details.endswith(f"User {email} not found."):
                raise errors.EmailNotFoundError(details, email)
            elif details.endswith(f"handler not found: {inbound_tag}"):
                raise errors.InboundNotFoundError(details, inbound_tag)
            else:
                raise errors.V2RayError(details)

    def add_inbound(self,
                    tag: str,
                    address: str,
                    port: int,
                    inbound: Inbound) -> bool:
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
                    proxy_settings=inbound.message
                )
            ))
            return True

        except grpc.RpcError as e:
            details = e.details()

            if details.endswith("address already in use"):
                raise errors.AddressAlreadyInUseError(details, port)
            else:
                raise errors.V2RayError(details)

    def remove_inbound(self, tag: str) -> bool:
        stub = command_pb2_grpc.HandlerServiceStub(self._channel)
        try:
            stub.RemoveInbound(command_pb2.RemoveInboundRequest(
                tag=tag
            ))
            return True
        except grpc.RpcError as e:
            details = e.details()
            if details == 'not enough information for making a decision':
                raise errors.InboundNotFoundError(details, tag)
            else:
                raise errors.V2RayError(details)
