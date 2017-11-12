#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import os, random
import robomodules as rm
from messages import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 10
STEP = 5

class ServoModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.CTRL_MSG]
        GPIO.setmode(GPIO.BCM)
		GPIO.setup(18, GPIO.OUT)
		self.servos = [GPIO.PWM(18, 100)]
		self.positions = [0 for _ in range(len(self.servos))]
		self.msg = None

		for servo in self.servos:
			servo.start(5)

        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)

    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.CTRL_MSG:
            self.msg = msg
        return

    def tick(self):
        if self.msg:
        	if self.msg.servoX == 1:
        		self.positions[0] += STEP
        	elif self.msg.servoX == -1:
        		self.positions[0] -= STEP
        	if self.positions[0] > 180:
        		self.positions[0] = 180
        	elif self.positions[0] < 0:
        		self.positions[0] = 0

        	if self.msg.servoY == 1:
        		self.positions[1] += STEP
        	elif self.msg.servoY == -1:
        		self.positions[1] -= STEP
        	if self.positions[1] > 180:
        		self.positions[1] = 180
        	elif self.positions[1] < 0:
        		self.positions[1] = 0
        self._set_servo_angle(0)
        self._set_servo_angle(1)


    def _set_servo_angle(servo):
    	angle = self.positions[servo]
    	duty = float(angle) / 10.0 + 2.5
        self.servos[servo].ChangeDutyCycle(duty)


def main():
    module = ServoModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
