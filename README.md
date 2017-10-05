# MATE_ROV

Code for The Harvard Undergraduate Robotics Club's MATE ROV team.

The code consist of separate modules that are run on either the ROV or on a ground base. Inter-module communications are orchestrated by the RovController (rovController.py), which acts like a server. Modules send messages to the rovController and subscribe to certain messagetypes. When the RovController receives a message of a certain type, it forwards it to all the modules that have subscribed to that message type.

## How to run

1. Execute ./rovController
2. Execute all of your modules

## Adding new modules

1. If necessary, create a new protocol buffer for your data.
    - Create a new .proto file describing your buffer in the comm folder.
    - Add your new .proto file to the Makefile in the comm folder.
        - Before:
        ```
        protobuf: first.proto
    	    protoc -I=./ --python_out=./ ./first.proto
        ```
        - After:
        ```
        protobuf: first.proto second.proto
    	    protoc -I=./ --python_out=./ ./first.proto
    	    protoc -I=./ --python_out=./ ./second.proto
        ```
    - Run the make command in the comm folder.
    - In comm/constants.py do the following:
        - Import your new compiled buffer.
        - Add a message type enum for your new buffer.
        - Add the new message type and the associated buffer to message_buffers.
        - Example:
            - Before:
            ```
            import struct
            from .first_pb2 import FirstMsg

            class MsgType(Enum):
                FIRST = 0

            message_buffers = {
                MsgType.FIRST: FirstMsg
            }
            ```
            - After:
            ```
            import struct
            from .first_pb2 import FirstMsg
            from .second_pb2 import SecondMsg

            class MsgType(Enum):
                FIRST = 0
                SECOND = 1

            message_buffers = {
                MsgType.FIRST: FirstMsg,
                MsgType.SECOND: SecondMsg
            }
            ```
2. Make a new module class that inherits from modules.ProtoModule. Look at MockGuiModule.py and MockSensorModule for examples on modules
