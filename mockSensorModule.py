#!/usr/bin/env python3

import asyncio, os
from modules.protoModule import ProtoModule
from comm.constants import *
from comm.mockMsg_pb2 import MockMsg

import random

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)


FREQUENCY = 2

class MockSensorModule(ProtoModule):
    def __init__(self, loop):
        super().__init__(loop, ADDRESS, PORT, [])

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
    loop = asyncio.get_event_loop()
    module = MockSensorModule(loop)
    module.run()

if __name__ == "__main__":
    main()
