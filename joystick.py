#!/usr/bin/env python3

import os, random
import robomodules as rm
from messages import *
import pygame, sys
from pygame.locals import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 20

class GUIModule(rm.ProtoModule):
	def __init__(self, addr, port):
		super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
		self.x = 0.
		self.y = 0.
		self.z = 0.
		self.pitch = 0.
		self.yaw = 0.
		self.roll = 0.
		pygame.init()
		pygame.joystick.init()
		njoysticks = pygame.joystick.get_count()
		if njoysticks == 0:
			print("No joysticks found")
			pygame.quit()
		else:
			joylist = []
			for n in range(0, njoysticks):
				joylist.append(pygame.joystick.Joystick(n))
				joylist[n].init()
				print(joylist[n].get_name())
				if joylist[n].get_name() = "Logitech Dual Action":
					self.logitech = joylist[n]
					n = njoysticks - 1
				elif n = njoysticks - 1
					print("Correct Joystick Not Found")
					pygame.quit()


	def msg_received(self, msg, msg_type):
		# This gets called whenever any message is received
		# This module only sends data, so we ignore incoming messages
		return

	def tick(self):
		# this function will get called in a loop with FREQUENCY frequency
		# for this mock module we will just send a random int
		msg = CtrlMsg()
		self._get_input()
		msg.x = self.x
		msg.y = self.y
		msg.z = self.z
		msg.pitch = self.pitch
		msg.yaw = self.yaw
		msg.roll = self.roll
		msg = msg.SerializeToString()
		self.write(msg, MsgType.CTRL_MSG)

	def _get_input(self):
		joy = self.logitech
		buttonA = joy.get_button(1)
		buttonB = joy.get_button(2)
		buttonX = joy.get_button(0)
		buttonY = joy.get_button(3)
		buttonLB = joy.get_button(4)
		buttonRB = joy.get_button(5)
		buttonLT = joy.get_button(6)
		buttonRT = joy.get_button(7)

		# -1 <= up < 0 < down <= +1
		if buttonLB:
			y = 0.
			z = joy.get_axis(1)
		else:
			y = joy.get_axis(1)
			z = 0.
		pitch = joy.get_axis(3)

		# -1 <= left < 0 < right <= +1
		if buttonRB:
			yaw = 0.
			roll = joy.get_axis(2)
		else:
			yaw = joy.get_axis(2)
			roll = 0.
		x = joy.get_axis(0)


def main():
	module = GUIModule(ADDRESS, PORT)
	module.run()
	pygame.quit()	


if __name__ == "__main__":
	main()
