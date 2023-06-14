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

    def draw(self, surface):
        pc.GameObject.draw(self, surface)

    def get_key(self, receivedKeys):
        self.keys = receivedKeys
        self.velocity = pg.Vector2(0, 0)

        if self.keys[pg.K_w]:
            self.velocity.y = 1
        if self.keys[pg.K_s]:
            self.velocity.y = -1
        if self.keys[pg.K_d]:
            self.velocity.x = 1
        if self.keys[pg.K_a]:
            self.velocity.x = -1

        if not (self.velocity == pg.Vector2(0,0)):
            self.velocity = pg.Vector2.normalize(self.velocity) * PlayerStats.SPEED

