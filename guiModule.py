#!/usr/bin/env python3

import os, sys
import cv2
import robomodules as rm
import pickle
import pygame
import numpy
from messages import message_buffers, MsgType
from navball import NavBall

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 25
NAVBALL_FREQ = 1
FRAME_WIDTH = 640
SCREEN_SIZE = (FRAME_WIDTH*3, 900)
NAVBALL_SIZE = 300

class GuiModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.CAMERA_FRAME_MSG, MsgType.CTRL_MSG, MsgType.HUMIDITY_MSG]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.frames = {}
        pygame.init()
        pygame.font.init()
        self.text_surf = pygame.Surface((300, 50))
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        self.navball = NavBall(self.display, NAVBALL_SIZE, SCREEN_SIZE[0]/2, SCREEN_SIZE[1] - NAVBALL_SIZE/2 - 50)
        self.navball_ticks = 0
        self.roll = 0
        self.yaw = 0
        self.pitch = 0
        self.humidity = 0

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # We receive pickled frames here.
        if msg_type == MsgType.CAMERA_FRAME_MSG:
            self.frames[msg.id] = msg.cameraFrame
        elif msg_type == MsgType.CTRL_MSG:
            self.roll = msg.roll * 90
            self.pitch = msg.pitch * 90
            self.yaw = msg.yaw * 90
        elif msg_type == MsgType.HUMIDITY_MSG:
            self.humidity = msg.humidity
        
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit('quit')
        self._display_frames()
        if self.navball_ticks % int(FREQUENCY/NAVBALL_FREQ) == 0:
            self.navball.draw(self.yaw, self.roll, self.pitch)
        self._draw_sensor_values()
        pygame.display.update()
        self.navball_ticks += 1

    def _draw_sensor_values(self):
        self.text_surf.fill((0,0,0))
        hum_surface = self.font.render('Humidity={0:0.1f}%'.format(self.humidity), True, (255, 255, 255))
        self.text_surf.blit(hum_surface, (0, 0))
        self.display.blit(self.text_surf, (SCREEN_SIZE[0]-300, SCREEN_SIZE[1]-50))

    def _display_frames(self):
        cur_x = 0
        for frame_id in self.frames:
            raw_frame = self.frames[frame_id]
            frame = pickle.loads(raw_frame)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = numpy.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            cur_width = frame.get_width()
            cur_height = frame.get_height()
            new_height = int(cur_height * FRAME_WIDTH/cur_width)
            frame = pygame.transform.scale(frame, (FRAME_WIDTH, new_height))
            self.display.blit(frame,(cur_x,0))
            cur_x += frame.get_width()

def main():
    module = GuiModule(ADDRESS, PORT)
    module.run()
    pygame.quit()

if __name__ == "__main__":
    main()
