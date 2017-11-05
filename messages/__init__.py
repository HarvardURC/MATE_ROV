from enum import Enum
from .mockMsg_pb2 import MockMsg
from .ctrlMsg_pb2 import CtrlMsg

class MsgType(Enum):
    MOCK_MSG = 0
    CTRL_MSG = 1

message_buffers = {
    MsgType.MOCK_MSG: MockMsg
    MsgType.CTRL_MSG: CtrlMsg
}


__all__ = ['MsgType', 'message_buffers', 'MockMsg', 'CtrlMsg']
