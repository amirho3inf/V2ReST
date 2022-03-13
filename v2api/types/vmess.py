from uuid import UUID
import typing

from ..utils import to_typed_message

from ..proto.proxy.vmess.inbound import config_pb2 as vmess_inbound_config_pb2
from ..proto.proxy.vmess import account_pb2
from ..proto.common.protocol import user_pb2

from .common import Account, Inbound


class VMessInbound(Inbound):
    def __init__(self, users: typing.List[dict], secure_encryption_only: bool):
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
                ],
                secure_encryption_only=secure_encryption_only
            )
        )


class VMessAccount(Account):
    def __init__(self, user_id: typing.Union[UUID, str], alter_id: int = 0):
        if isinstance(user_id, UUID):
            user_id = str(user_id)

        self.message = to_typed_message(account_pb2.Account(
            id=user_id,
            alter_id=alter_id
        ))
