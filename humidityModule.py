#!/usr/bin/env python3

import os, random
import Adafruit_DHT
import robomodules as rm
from messages import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 0.25
SENSOR_PIN1 = 21

class MockSensorModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = []
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.sensor = Adafruit_DHT.DHT22

    def msg_received(self, msg, msg_type):
        return

    def tick(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, SENSOR_PIN1)

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        
        msg = MockMsg()
        msg.mockValue = random.randint(1, 9)
        msg = msg.SerializeToString()
        self.write(msg, MsgType.MOCK_MSG)


def main():
    module = MockSensorModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
