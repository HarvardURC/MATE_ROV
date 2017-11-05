#!/usr/bin/env python3

import os
import robomodules as rm
from messages import message_buffers, MsgType
import pickle

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 10

class CameraDisplayModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.CAMERA_FRAME_MSG]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.frame = None

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # We receive pickled frames here.
        if msg_type == MsgType.CAMERA_FRAME_MSG:
            self.frame = msg.cameraFrame

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        # process the serialized frame
        self._display_serialized_image()

    def _display_serialized_image(self):
        if self.frame == None:
            print("frame == None")
            return
        frame = pickle.loads(self.frame)
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv2.imshow('frame',gray)

def main():
    module = CameraDisplayModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
