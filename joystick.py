import pygame, sys
from pygame.locals import *

pygame.init()
pygame.joystick.init()
pygame.display.init()
windowSurface = pygame.display.set_mode((800, 600), 0, 32)