#!/usr/bin/env python3

import os, random
import robomodules as rm
from messages import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 2

class MockSensorModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = []
        super().__init__(addr, port, message_buffers, MsgType, self.subscriptions)

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        return

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        self.loop.call_later(1.0/FREQUENCY, self.tick)

        # for this mock module we will just send a random int
        msg = MockMsg()
        msg.mockValue = random.randint(1, 9)
        msg = msg.SerializeToString()
        self.write(msg, MsgType.MOCK_MSG)


def main():
    module = MockSensorModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
