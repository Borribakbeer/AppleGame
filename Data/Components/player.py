import pygame.math
import math

from Utils import ParentComponents as pc
from Utils import Tools
from Stats import PlayerStats
import ResourceManager as resources
import pygame as pg


class Player(pc.GameObject, pc.Rigidbody):
    def __init__(self, pos):
        pc.GameObject.__init__(self, "Sprites", "Player", pos, (1, 2))
        pc.Rigidbody.__init__(self, pos)
        pc.Collider.__init__(self, "Mask")
        self.worldposition = pos
        self.screenposition = [0, 0]
        self.offset = pg.Vector2(0, 0)
        self.collisions = []
        self.tags.add("Player")
        self.bobtime = 0
        self.bobbin = True
        self.dir = 0

    def update(self, now, keys, GameInfo, dt):
        pc.GameObject.update(self, now, keys, GameInfo, dt)
        pc.Rigidbody.update(self, GameInfo, dt)
        if(self.bobbin):
            self.bobtime += dt

    def draw(self, surface):
        offsetX = self.offset.x
        offsetY = self.offset.y
        if (self.colliding == False) and (self.velocity.magnitude() > 0):
            self.bobbin = True
            offsetY = math.sin(self.bobtime * PlayerStats.Bobspeed) * PlayerStats.Bobamount
        else:
            self.bobbin = False
        print(self.bobtime)
        self.offset = pg.Vector2(offsetX, offsetY)
        self.screenposition += self.offset
        pc.GameObject.draw(self, surface)


    def get_key(self, receivedKeys):
        self.keys = receivedKeys
        self.velocity = pg.Vector2(0, 0)

        if self.keys[pg.K_w] or self.keys[pg.K_UP]:
            self.velocity.y = 1
        if self.keys[pg.K_s] or self.keys[pg.K_DOWN]:
            self.velocity.y = -1
        if self.keys[pg.K_d] or self.keys[pg.K_RIGHT]:
            if(self.dir != 0):
                self.dir = 0
                self.image = pygame.transform.flip(self.image, True, False)
            self.velocity.x = 1
        if self.keys[pg.K_a] or self.keys[pg.K_LEFT]:
            if(self.dir != 1):
                self.dir = 1
                self.image = pygame.transform.flip(self.image, True, False)
            self.velocity.x = -1

        if not (self.velocity == pg.Vector2(0,0)):
            self.velocity = pg.Vector2.normalize(self.velocity) * PlayerStats.SPEED

