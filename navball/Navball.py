#!/usr/bin/env python

import math
import pygame
import numpy as np
import scipy
import scipy.misc
import scipy.ndimage.interpolation
import time

SRC = 'ji80w.png'
SIZE = 300

class NavBall():
    def __init__(self, source, size):
        self.src = scipy.misc.imread(source)
        self.size = size

    def get_view(self, yaw, pitch):

        yaw = (yaw+90)/360
        pitch = (pitch/360)*16

        # Image pixel co-ordinates
        px=np.arange(-1.0,1.0,2.0/self.size)+1.0/self.size
        py=np.arange(-1.0,1.0,2.0/self.size)+1.0/self.size
        hx,hy=scipy.meshgrid(px,py)

        # Compute z of sphere hit position, if pixel's ray hits
        r2=hx*hx+hy*hy
        hit=(r2<=1.0)
        hz=np.where(
            hit,
            -np.sqrt(1.0-np.where(hit,r2,0.0)),
            np.NaN
            )


        spin=2.0*np.pi*(-yaw)
        cs=math.cos(spin)
        ss=math.sin(spin)
        ms=np.array([[cs,0.0,ss],[0.0,1.0,0.0],[-ss,0.0,cs]])

        tilt=0.125*np.pi*pitch
        ct=math.cos(tilt)
        st=math.sin(tilt)
        mt=np.array([[1.0,0.0,0.0],[0.0,ct,st],[0.0,-st,ct]])

        # Rotate the hit points
        xyz=np.dstack([hx,hy,hz])
        xyz=np.tensordot(xyz,mt,axes=([2],[1]))
        xyz=np.tensordot(xyz,ms,axes=([2],[1]))
        x=xyz[:,:,0]
        y=xyz[:,:,1]
        z=xyz[:,:,2]

        # Compute map position of hit
        latitude =np.where(hit,(0.5+np.arcsin(y)/np.pi)*self.src.shape[0],0.0)
        longitude=np.where(hit,(1.0+np.arctan2(z,x)/np.pi)*0.5*self.src.shape[1],0.0)
        latlong=np.array([latitude,longitude])

        # Resample, and zap non-hit pixels
        dst=np.zeros((self.size,self.size,3))
        for channel in [0,1,2]:
            dst[:,:,channel]=np.where(
                hit,
                scipy.ndimage.interpolation.map_coordinates(
                    self.src[:,:,channel],
                    latlong,
                    order=1
                    ),
                0.0
                )
        return np.rot90(np.fliplr(dst))

def main():
    navball = NavBall(SRC, SIZE)
    pygame.init()
    display = pygame.display.set_mode((350, 350))

    running = True
    pitch = 90
    yaw = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        ball = navball.get_view(yaw, pitch)
        surf = pygame.surfarray.make_surface(ball)
        display.blit(surf, (0, 0))
        pygame.display.update()
        print("Y:{}\nP:{}".format(yaw, pitch))
        time.sleep(0.1)
    pygame.quit()


if __name__ == "__main__":
    main()
