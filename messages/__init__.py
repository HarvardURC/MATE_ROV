from enum import Enum
from .mockMsg_pb2 import MockMsg

class MsgType(Enum):
    MOCK_MSG = 0

message_buffers = {
    MsgType.MOCK_MSG: MockMsg
}


__all__ = ['MsgType', 'message_buffers', 'MockMsg']
