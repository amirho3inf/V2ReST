import sys
import pathlib
from contextlib import contextmanager


@contextmanager
def set_proto_path():
    proto_path = str(pathlib.Path(__file__).parent / 'proto')
    try:
        sys.path.append(proto_path)
        yield
    finally:
        sys.path.remove(proto_path)


with set_proto_path():
    from .client import Client
    from . import errors, types


__all__ = [
    'Client',
    'errors',
    'types'
]
