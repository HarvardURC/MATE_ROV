from enum import Enum
from .mockMsg_pb2 import MockMsg
from .cameraFrameMsg_pb2 import CameraFrameMsg

class MsgType(Enum):
    MOCK_MSG = 0
    CAMERA_FRAME_MSG = 1

message_buffers = {
    MsgType.MOCK_MSG: MockMsg,
    MsgType.CAMERA_FRAME_MSG: CameraFrameMsg
}


__all__ = ['MsgType', 'message_buffers', 'MockMsg', 'CameraFrameMsg']
