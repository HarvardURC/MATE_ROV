#!/usr/bin/env python3

import os
import sys

import cv2
import pickle

from messages import *
import robomodules as rm

ADDRESS = os.environ.get("BIND_ADDRESS", "localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 4


class CameraSensorModule(rm.ProtoModule):
    def __init__(self, addr, port, camera_port):
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.cam = cv2.VideoCapture(camera_port)
        self.id = camera_port

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        return

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        # gets the camera feed, puts it into the message
        msg = CameraFrameMsg()
        ret, frame = self.cam.read()
        h, w, _ = frame.shape
        frame = cv2.resize(frame, (int(w/4), int(h/4)))
        msg.cameraFrame = pickle.dumps(frame)
        msg.id = self.id
        msg = msg.SerializeToString()
        self.write(msg, MsgType.CAMERA_FRAME_MSG)


def main():
    port = 0
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    module = CameraSensorModule(ADDRESS, PORT, port)
    module.run()

if __name__ == "__main__":
    main()
