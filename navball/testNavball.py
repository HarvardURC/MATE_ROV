#!/usr/bin/env python3

import pygame
import time
from navball import NavBall

SRC = 'ji80w.png'
NAVBALL_SIZE = 300
SCREEN_SIZE = 800
FREQUENCY = 30


def main():
    pygame.init()
    display = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    navball = NavBall(display, SRC, NAVBALL_SIZE, SCREEN_SIZE/2, SCREEN_SIZE/2)

    running = True
    pitch = 0
    yaw = 0
    roll = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        navball.draw_ball_surf(yaw, roll, pitch)
        pygame.display.update()
        roll += 10
        yaw += 5
        pitch += 10
        time.sleep(1/FREQUENCY)
    pygame.quit()

if __name__ == "__main__":
    main()
