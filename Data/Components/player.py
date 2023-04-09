import Data.Utils.ParentComponents as pc
from Data.Utils import Tools
import Data.ResourceManager as resources
import pygame as pg
import numpy as np


class Player(pc.GameObject, pc.Rigidbody):
    def __init__(self, pos):
        pc.Rigidbody.__init__(self)
        pc.GameObject.__init__(self, "Misc", "Heart", pos, (1, 1))
        self.position = pos

    def update(self, now):
        pc.GameObject.update(self)
        pc.Rigidbody.update(self)
        self.position = self.worldPosition

    def draw(self, surface):
        pc.GameObject.draw(self, surface)

    def get_key(self, receivedKeys):
        self.keys = receivedKeys
        if self.keys[pg.K_w]:
            self.velocity = np.array(resources.DIRECT_DICT["front"])
        elif self.keys[pg.K_s]:
            self.velocity = np.array(resources.DIRECT_DICT["back"])
        elif self.keys[pg.K_d]:
            self.velocity = np.array(resources.DIRECT_DICT["right"])
        elif self.keys[pg.K_a]:
            self.velocity = np.array(resources.DIRECT_DICT["left"])
