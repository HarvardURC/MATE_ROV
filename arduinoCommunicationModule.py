#!/usr/bin/env python3

import os
import robomodules as rm
import serial
from messages import *

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
            self.serialConnection.write(self._stringToBinary(self._messageToString(msg)))

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        # from https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=54182
        msg = self._stringToMessage(self._binaryToString(self.serialConnection.readline()))
        if msg:
            self.write(msg, MsgType.ORIENTATION_MSG)

    def _messageToString(self, m):
        ans = "$"
        # go through each of the properties in the message
        for prop in ["x", "y", "z", "roll", "pitch", "yaw"]:
            # convert the number into a string
            # separate the properties with a semicolon
            ans += (str(getattr(m, prop)) + ";")
        return ans
        
    def _stringToBinary(self, s):
        return bytes(s, "ascii")
        
    def _binaryToString(self, b):
        return b.decode('ascii')
        
    def _stringToMessage(self, s):
        ans = OrientationMsg()
        # take off leading '$'
        s = s[1:] if s[0] == "$"
        # get all of the values in the string
        # need to take off the last empty string that split will leave
        numbers = (s.split(";"))[0:-1]
        # didn't get a good input
        if len(numbers) != 3:
            return None
        # assumes the values are coming in in that order
        for (number, name) in zip(numbers, ["roll", "pitch", "yaw"]):
            setattr(ans, name, number)
        
        return ans
            

def main():
    module = ArduinoCommsModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
