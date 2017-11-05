#!/usr/bin/env python3

import os, random
import robomodules as rm
from messages import *
import numpy as np
import cv2
import pickle

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 30

class CameraSensorModule(rm.ProtoModule):
    def __init__(self, addr, port, camera_port):
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.cam = cv2.VideoCapture(camera_port)

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        return

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        # gets the camera feed, puts it into the message
        msg = CameraFrameMsg()
        ret, frame = self.cam.read()
        msg.cameraFrame = pickle.dumps(frame)
        msg = msg.SerializeToString()
        self.write(msg, MsgType.CAMERA_FRAME_MSG)

def main():
    module = CameraSensorModule(ADDRESS, PORT, 0)
    module.run()

if __name__ == "__main__":
    main()
