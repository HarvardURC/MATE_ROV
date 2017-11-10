import math
import pygame
import numpy as np
import scipy
import scipy.misc
import scipy.ndimage.interpolation

NAVBALL_SOURCE = './navball/ji80w.png'

class NavBall():
    def __init__(self, display, size, x, y):
        self.display = display
        self.src = scipy.misc.imread(NAVBALL_SOURCE)
        self.size = size
        self.x = x
        self.y = y

    def _adjust_inputs(self, yaw, pitch):
        yaw = (yaw+90)/360
        pitch = (pitch/360)*16
        return (yaw, pitch)

    def _get_view(self, yaw, pitch):

        yaw, pitch = self._adjust_inputs(yaw, pitch)

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

    def draw(self, yaw, roll, pitch):
        ball = self._get_view(yaw, pitch)
        surf = pygame.surfarray.make_surface(ball)
        rotated_surf = pygame.transform.rotate(surf, roll)
        rotated_rect = rotated_surf.get_rect()
        rotated_rect.center = (self.x, self.y)
        self.display.blit(rotated_surf, rotated_rect)
        pygame.draw.lines(self.display, (255, 255, 255), False, [[self.x - self.x/8, self.y], [self.x - self.x/15, self.y], [self.x, self.y + self.y/18], [self.x + self.x/15, self.y], [self.x + self.x/8, self.y]], 3)
        pygame.draw.line(self.display, (255, 255, 255), [self.x - self.x/50, self.y], [self.x + self.x/50, self.y], 3)

