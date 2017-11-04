#!/usr/bin/env python3

import os
import robomodules as rm
from messages import message_buffers, MsgType

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 10

class CameraDisplayModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.CAMERA_MSG]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.value = -1
        self.sub_ticks = 0
        self.subbed = True

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # We received pickled frames here.
        if msg_type == MsgType.CAMERA_FRAME_MSG:
            self.frame = msg.cameraFrame


    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        # process the serialized frame
        displaySerializedImage(self.frame)

    def displaySerializedImage(si):
        frame = pickle.loads(si)
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)


def main():
    module = MockGuiModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
