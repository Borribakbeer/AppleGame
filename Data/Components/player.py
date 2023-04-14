import pygame.math

from Utils import ParentComponents as pc
from Utils import Tools
from Stats import PlayerStats
import ResourceManager as resources
import pygame as pg
import numpy as np


class Player(pc.GameObject, pc.Rigidbody):
    def __init__(self, pos):
        pc.Rigidbody.__init__(self, pos)
        pc.GameObject.__init__(self, "Misc", "Heart", pos, (1, 1))
        self.worldposition = pos
        self.screenposition = [0, 0]

    def update(self, now):
        pc.GameObject.update(self, now)
        pc.Rigidbody.update(self)

    def draw(self, surface):
        pc.GameObject.draw(self, surface)

    def get_key(self, receivedKeys):
        self.keys = receivedKeys
        if self.keys[pg.K_w]:
            self.velocity = np.array(resources.DIRECT_DICT["front"]) * PlayerStats.SPEED
        elif self.keys[pg.K_s]:
            self.velocity = np.array(resources.DIRECT_DICT["back"]) * PlayerStats.SPEED
        elif self.keys[pg.K_d]:
            self.velocity = np.array(resources.DIRECT_DICT["right"]) * PlayerStats.SPEED
        elif self.keys[pg.K_a]:
            self.velocity = np.array(resources.DIRECT_DICT["left"]) * PlayerStats.SPEED
        else:
            self.velocity = np.array((0, 0))
