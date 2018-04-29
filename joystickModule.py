#!/usr/bin/env python3

import os, random
import robomodules as rm
from messages import *
import pygame, sys
from pygame.locals import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 5

class JoystickModule(rm.ProtoModule):
    def __init__(self, addr, port):
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)
        self.x = 0.
        self.y = 0.
        self.z = 0.
        self.pitch = 0.
        self.yaw = 0.
        self.roll = 0.
        self.camera_tilt = 0.
        self.camera_pan = 0.
        self.logitech = None
        pygame.init()
        pygame.joystick.init()
        njoysticks = pygame.joystick.get_count()
        if njoysticks == 0:
            print("No joysticks found")
            pygame.quit()
            sys.exit('')
        for n in range(0, njoysticks):
            self.logitech = pygame.joystick.Joystick(n)
            self.logitech.init()
            print(self.logitech.get_name())
            if 'Logitech' in self.logitech.get_name():
                break
            elif n == njoysticks - 1:
                print("Correct Joystick Not Found")
                pygame.quit()

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        return

    def tick(self):
        # this function will get called in a loop with FREQUENCY frequency
        # for this mock module we will just send a random int
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit('quit')
        msg = CtrlMsg()
        self._get_input()
        msg.x = self.x
        msg.y = self.y
        msg.z = self.z
        msg.pitch = self.pitch
        msg.yaw = self.yaw
        msg.roll = self.roll
        msg.cameraTilt = self.camera_tilt
        msg.cameraPan = self.camera_pan
        msg = msg.SerializeToString()
        self.write(msg, MsgType.CTRL_MSG)

    def _get_input(self):
        joy = self.logitech
        if not joy:
            return
        buttonA = joy.get_button(1)
        buttonB = joy.get_button(2)
        buttonX = joy.get_button(0)
        buttonY = joy.get_button(3)
        buttonLB = joy.get_button(4)
        buttonRB = joy.get_button(5)
        buttonLT = joy.get_button(6)
        buttonRT = joy.get_button(7)
        tpl = joy.get_hat(0)

        # -1 = top, 1 = bottom
        leftY = joy.get_axis(1)
        rightY = joy.get_axis(3)

        # -1 = left, 1 = right
        leftX = joy.get_axis(0)
        rightX = joy.get_axis(2)

        self.camera_tilt = tpl[0]
        self.camera_pan = tpl[1]

        # the following is a temporary control scheme
        # many buttons above are not currently in use,
        # but can easily be used.
        if buttonLB:
            self.y = 0.
            self.z = leftY
        else:
            self.y = leftY
            self.z = 0.
        self.pitch = rightY

        if buttonRB:
            self.yaw = 0.
            self.roll = rightX
        else:
            self.yaw = rightX
            self.roll = 0.
        self.x = leftX


def main():
    module = JoystickModule(ADDRESS, PORT)
    module.run()
    pygame.quit()


if __name__ == "__main__":
    main()
