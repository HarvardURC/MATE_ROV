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
            self.serialConnection = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
        except Exception:
            raise RuntimeError("serial connection to Arduino failed")

    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.CTRL_MSG:
            arduino_msg = self._stringToBinary(self._messageToString(msg))
            print(arduino_msg)
            self.serialConnection.write(arduino_msg)

    def tick(self):
        line = self.serialConnection.readline()
        if len(line) > 0:
            msg = self._stringToMessage(self._binaryToString(line))
            if msg:
                self.write(msg.SerializeToString(), MsgType.ORIENTATION_MSG)

    def _messageToString(self, m):
        ans = "$"
        for prop in ["x", "y", "z", "roll", "pitch", "yaw", "cameraTilt", "cameraPan"]:
            ans += (str(getattr(m, prop)) + ";")
        ans += "\0"
        return ans
        
    def _stringToBinary(self, s):
        return bytes(s, "ascii")
        
    def _binaryToString(self, b):
        return b.decode('ascii')
        
    def _stringToMessage(self, s):
        ans = OrientationMsg()
        # take off leading '$'
        s = s[1:] if s[0] == "$" else s
        # get all of the values in the string
        # need to take off the last empty string that split will leave
        numbers = (s.split(";"))[0:-1]
        # didn't get a good input
        if len(numbers) != 3:
            return None
        # assumes the values are coming in in that order
        for (number, name) in zip(numbers, ["roll", "pitch", "yaw"]):
            setattr(ans, name, float(number))
        return ans
            

def main():
    module = ArduinoCommsModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
