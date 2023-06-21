import pygame.math

from Utils import ParentComponents as pc
from Utils import Tools
from Stats import PlayerStats
import ResourceManager as resources
import pygame as pg


class Player(pc.GameObject, pc.Rigidbody):
    def __init__(self, pos):
        pc.GameObject.__init__(self, "Misc", "Heart", pos, (1, 1))
        pc.Rigidbody.__init__(self, pos)
        pc.Collider.__init__(self, "Mask")
        self.worldposition = pos
        self.screenposition = [0, 0]
        self.collisions = []
        self.tags.add("Player")

    def update(self, now, keys, GameInfo, dt):
        pc.GameObject.update(self, now, keys, GameInfo, dt)
        pc.Rigidbody.update(self, GameInfo, dt)
        print(self.worldposition)

    def draw(self, surface):
        pc.GameObject.draw(self, surface)

    def get_key(self, receivedKeys):
        self.keys = receivedKeys
        self.velocity = pg.Vector2(0, 0)

        if self.keys[pg.K_w] or self.keys[pg.K_UP]:
            self.velocity.y = 1
        if self.keys[pg.K_s] or self.keys[pg.K_DOWN]:
            self.velocity.y = -1
        if self.keys[pg.K_d] or self.keys[pg.K_RIGHT]:
            self.velocity.x = 1
        if self.keys[pg.K_a] or self.keys[pg.K_LEFT]:
            self.velocity.x = -1

        if not (self.velocity == pg.Vector2(0,0)):
            self.velocity = pg.Vector2.normalize(self.velocity) * PlayerStats.SPEED

