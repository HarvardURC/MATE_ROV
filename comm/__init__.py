from .constants import *

class UnavailableClient:
    def __init__(self, *args, **kwargs):
        raise ImportError("Could not import client.")

try:
    from .asyncClient import AsyncClient
except ImportError:
    AsyncClient = UnavailableClient

try:
    from .serverProto import ServerProto
except ImportError:
    ServerProto = UnavailableClient

def pack_msg(msg, msg_type):
    header = SIZE_HEADER.pack(MAGIC_HEADER, msg_type.value, len(msg))
    return header + msg
    
__all__ = ['AsyncClient', 'ServerProto']
