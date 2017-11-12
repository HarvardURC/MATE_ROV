#!/usr/bin/env python3

import os
import robomodules as rm
import serial
from messages import message_buffers, MsgType


ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 10

class ArduinoCommsModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.CTRL_MSG]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        try:
            self.serialConnection = serial.Serial('/dev/ttyUSB0', 9600)
        except Exception:
            raise RuntimeError("serial connection to Arduino failed")

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        if msg_type == MsgType.CTRL_MSG:
            # turn it into a string
            # turn the string into binary
            # send the binary
            self.serialConnection.write(self.stringToBinary(self.messageToString(msg)))

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        pass
        
    def messageToString(self, m):
        ans = ""
        # go through each of the properties in the message
        for prop in ["x", "y", "z", "roll", "pitch", "yaw"]:
            # convert the number into a string
            # separate the properties with a semicolon
            ans += (str(getattr(m, prop)) + ";")
        return ans
        
    def stringToBinary(self, s):
        return bytes(s)


def main():
    print("No main written for ArduinoCommsModule yet!")

if __name__ == "__main__":
    main()
