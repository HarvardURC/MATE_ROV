#!/usr/bin/env python3

import os, random
import Adafruit_DHT
import robomodules as rm
from messages import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 10
SENSOR_PIN1 = 21

class HumidityModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = []
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.sensor = Adafruit_DHT.DHT22

    def msg_received(self, msg, msg_type):
        return

    def tick(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, SENSOR_PIN1)

        if humidity is not None and temperature is not None:
            msg = HumidityMsg()
            msg.humidity = humidity
            msg = msg.SerializeToString()
            self.write(msg, MsgType.HUMIDITY_MSG)

def main():
    module = HumidityModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
