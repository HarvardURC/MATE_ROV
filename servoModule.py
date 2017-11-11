#!/usr/bin/env python3

from maestro import Controller
import time
import os, random
import robomodules as rm
from messages import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 20

class ServoModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = []

        self.servo = Controller()

        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        if msg_type == MsgType.CTRL_MSG:
            self._servo_ctrl(msg.servoX, msg.servoY)
        return

    def tick(self):
        self.subscribe(MsgType.CTRL_MSG)

    def _servo_ctrl(servoX, servoY):
        servo.setAccel(0, 4*servoX)
        servo.setAccel(1, 4*servoY)
        


def main():
    module = ServoModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
