import struct
from enum import Enum
from .mockMsg_pb2 import MockMsg
from .subscribe_pb2 import Subscribe

class MsgType(Enum):
    SUBSCRIBE = 0
    MOCK_MSG = 1

message_buffers = {
    MsgType.SUBSCRIBE: Subscribe,
    MsgType.MOCK_MSG: MockMsg
}

# Message sizes are communicated as a single unsigned short
# encoded using network byte-order (big-endian).
# receiving libraries will need to account for this properly.
# The header also includes a magic number (also a short) for verification
MAGIC_HEADER = 17380
SIZE_HEADER = struct.Struct("!HHH")
