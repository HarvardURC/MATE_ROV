#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *
import cv2, pickle, pygame, numpy

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 0
SCREEN_SIZE = 800

class CameraDisplayModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.CAMERA_FRAME_MSG]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.frame = None
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # We receive pickled frames here.
        if msg_type == MsgType.CAMERA_FRAME_MSG:
            self.frame = msg.cameraFrame
        self._display_serialized_image()
        
    def tick(self):
        # FREQUENCY is 0, so this will never be called.
        return

    def _display_serialized_image(self):
        if self.frame == None:
            print('frame == None')
            return
        frame = pickle.loads(self.frame)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame = numpy.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        self.display.blit(frame,(0,0))
        pygame.display.flip()

def main():
    module = CameraDisplayModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
