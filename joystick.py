#!/usr/bin/env python3

import os, random
import robomodules as rm
from messages import *
import pygame, sys
from pygame.locals import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 20

global logitech
global x
global y
global z
global pitch
global yaw
global roll

class MockSensorModule(rm.ProtoModule):
	def __init__(self, addr, port):
		super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)

	def msg_received(self, msg, msg_type):
		# This gets called whenever any message is received
		# This module only sends data, so we ignore incoming messages
		return

	def tick(self):
		# this function will get called in a loop with FREQUENCY frequency
		# for this mock module we will just send a random int
		msg = CtrlMsg()
		input()
		msg.x = x
		msg.y = y
		msg.z = z
		msg.pitch = pitch
		msg.yaw = yaw
		msg.roll = roll
		msg = msg.SerializeToString()
		self.write(msg, MsgType.CTRL_MSG)

def main():
	module = MockSensorModule(ADDRESS, PORT)
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
			if joylist[n].get_name() != "Logitech Dual Action":
				print("Wrong Controller")
				pygame.quit
		logitech = joylist[0]
		module.run()
		pygame.quit()

def input():
	# EVENT PROCESSING STEP
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop
		
		# Possible joystick actions: JOYAXISMOTION 
		# 	JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
	

	buttonA = logitech.get_button(1)
	buttonB = logitech.get_button(2)
	buttonX = logitech.get_button(0)
	buttonY = logitech.get_button(3)
	buttonLB = logitech.get_button(4)
	buttonRB = logitech.get_button(5)
	buttonLT = logitech.get_button(6)
	buttonRT = logitech.get_button(7)

	# -1 <= up < 0 < down <= +1
	if buttonLB:
		y = 0.
		z = logitech.get_axis(1)
	else:
		y = logitech.get_axis(1)
		z = 0.
	pitch = logitech.get_axis(3)

	# -1 <= left < 0 < right <= +1
	if buttonRB:
		yaw = 0.
		roll = logitech.get_axis(2)
	else:
		yaw = logitech.get_axis(2)
		roll = 0.
	x = logitech.get_axis(0)

if __name__ == "__main__":
	main()
