#!/usr/bin/env python3

import time, os, sys, logging
import asyncio # minimum Python 3.4, changed in 3.5.1
from comm.serverProto import ServerProto
from comm.constants import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

class RovController():
    def __init__(self, loop):
        self.loop = loop
        self.clients = []
        self.subs = {}

        coro = loop.create_server(lambda: ServerProto(self), ADDRESS, PORT)
        self.server = loop.run_until_complete(coro)

    def _add_subscriptions(self, protocol, data):
        for msg_type in data.msg_types:
            if msg_type in self.subs:
                self.subs[MsgType(msg_type)].append(protocol)
            else:
                self.subs[MsgType(msg_type)] = [protocol]

    def _forward_msg(self, msg, msg_type):
        if msg_type in self.subs:
            for protocol in self.subs[msg_type]:
                protocol.write(msg, msg_type)


    def msg_received(self, protocol, msg, msg_type):
        if msg_type == MsgType.SUBSCRIBE:
            data = message_buffers[msg_type]()
            data.ParseFromString(msg)
            self._add_subscriptions(protocol, data)
        else:
            self._forward_msg(msg, msg_type)

    def quit(self):
        self.loop.stop()

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.quit()

def main():
    # logger automatically adds timestamps
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s',
                        datefmt="%I:%M:%S %p")
    loop = asyncio.get_event_loop()
    controller = RovController(loop)
    controller.run()

if __name__ == "__main__":
    main()
