# Messages

A message is a package of data.
Modules send messages to the server, and then the server sends the message to *all* modules.
Modules will run a bit of code (`msg_received`) whenever they receive a message from the server.
Modules only need to process relevant messages, and can check what the message is by checking `msg_type`.

Here's an example from `guiModule.py` (commit 30c806e), where you see that it processes four types of messages. It ignores the `CTRL_MSG`.

```python
def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # We receive pickled frames here.
        if msg_type == MsgType.CAMERA_FRAME_MSG:
            self.frames[msg.id] = msg.cameraFrame
        elif msg_type == MsgType.CTRL_MSG:
            return 
        elif msg_type == MsgType.HUMIDITY_MSG:
            self.humidity = msg.humidity
        elif msg_type == MsgType.ORIENTATION_MSG:
            self.roll = msg.roll
            self.yaw = msg.yaw + 180
            self.pitch = msg.pitch + 180
```

## Messages Directory

For each message type, there are two files in the messages directory. One has extension `.proto` and one like `_pb2.py`.
The `.proto` one describes to `protobuf` what to make. In `Makefile`, you'll see that these files are compiled into the resulting
`_pb2.py` file. This compiled `.py` file is what is used in Python. In `__init__.py` you'll see that how these files are being used.

## Message Types

|Message|Use in our Python modules|Protobuf class|
|-------|-------------|--------------|
| Mock | MsgType.MOCK_MSG | MockMsg |
| Camera Frame | MsgType.CAMERA_FRAME_MSG | CameraFrameMsg |
| Control (joystick) | MsgType.CTRL_MSG | CtrlMsg |
| Humidity | MsgType.HUMIDITY_MSG | HumidityMsg |
| Orientation | MsgType.ORIENTATION_MSG | OrientationMsg |

## Adding a new message type

Check the README.md at the root of the project.

Otherwise, here's a different way to describe how to do it.

1. You need to make a `.proto` file with the new message type
2. Add a line to the `Makefile`
    - `protoc -I=./ --python_out=./ ./##yourTypeHere##.proto`
3. Do `make`, which will generate a new `_pb2.py` file. You must have protocol buffers installed to do this. If you don't want to install it, ask someone to compile your `.proto` file for you.
4. Four lines to `__init__.py`:
    - import the message type up top
    - add to the `MsgType` Enum
    - add to the `message_buffers` dictionary
    - add to the list `__all__` at the bottom
