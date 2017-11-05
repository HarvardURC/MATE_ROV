#!/usr/bin/env python3

import os
import cv2
import robomodules as rm
import pickle
import pygame
import numpy
from messages import message_buffers, MsgType
from navball import NavBall

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 30
NAVBALL_FREQ = 5
SCREEN_SIZE = (1600, 900)
NAVBALL_SIZE = 300

class GuiModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.CAMERA_FRAME_MSG, MsgType.CTRL_MSG]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.frame = None
        pygame.init()
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        self.navball = NavBall(self.display, NAVBALL_SIZE, SCREEN_SIZE[0]/2, SCREEN_SIZE[1] - NAVBALL_SIZE/2 - 50)
        self.navball_ticks = 0
        self.roll = 0
        self.yaw = 0
        self.pitch = 0

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # We receive pickled frames here.
        if msg_type == MsgType.CAMERA_FRAME_MSG:
            self.frame = msg.cameraFrame
        elif msg_type == MsgType.CTRL_MSG:
            self.roll = msg.roll * 90
            self.pitch = msg.pitch * 90
            self.yaw = msg.yaw * 90
        
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit('quit')
        self._display_serialized_image()
        if self.navball_ticks % int(FREQUENCY/NAVBALL_FREQ) == 0:
            self.navball.draw(self.yaw, self.roll, self.pitch)
        pygame.display.update()
        self.navball_ticks += 1

    def _display_serialized_image(self):
        if not self.frame:
            return
        frame = pickle.loads(self.frame)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame=numpy.rot90(frame)
        frame=pygame.surfarray.make_surface(frame)
        self.display.blit(frame,(0,0))

def main():
    module = GuiModule(ADDRESS, PORT)
    module.run()
    pygame.quit()

if __name__ == "__main__":
    main()
