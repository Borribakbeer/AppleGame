import Data.Utils.ParentComponents as pc
import Data.ResourceManager as resources
import pygame as pg


class Player(pc.GameObject, pc.Rigidbody):
    def __init__(self, pos):
        pc.Rigidbody.__init__(self)
        pc.GameObject.__init__(self, "Misc", "Heart", pos, (1, 1))
        self.position = pos

    def update(self):
        pc.GameObject.update(self)
        pc.Rigidbody.update(self)
        self.position = pc.Rigidbody.get_position(self)

    def draw(self, surface):
        pc.GameObject.draw(self, surface)

    def get_event(self, event):
        if event == pg.K_w:
            pc.Rigidbody.add_force(self, resources.DIRECT_DICT["front"])

