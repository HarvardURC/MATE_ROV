from enum import Enum
from .mockMsg_pb2 import MockMsg
from .cameraFrameMsg_pb2 import CameraFrameMsg
from .ctrlMsg_pb2 import CtrlMsg
from .humidityMsg_pb2 import HumidityMsg
from .orientationMsg_pb2 import OrientationMsg

class MsgType(Enum):
    MOCK_MSG = 0
    CAMERA_FRAME_MSG = 1
    CTRL_MSG = 2
    HUMIDITY_MSG = 3
    ORIENTATION_MSG = 4

message_buffers = {
    MsgType.MOCK_MSG: MockMsg,
    MsgType.CAMERA_FRAME_MSG: CameraFrameMsg,
    MsgType.CTRL_MSG: CtrlMsg,
    MsgType.HUMIDITY_MSG: HumidityMsg,
    MsgType.ORIENTATION_MSG: OrientationMsg
}

__all__ = ['MsgType', 'message_buffers', 'MockMsg', 'CameraFrameMsg', 'CtrlMsg', 'HumidityMsg', 'OrientationMsg']
