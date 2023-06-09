import pygame as pg
from ResourceManager import *
from Utils import ParentComponents as pc
import math

class Apple(pc.GameObject):
    def __init__(self, pos, size = pg.Vector2(1, 1), *groups):
        pc.GameObject.__init__(self, "Sprites", "Apple", pos, size)

        pc.Collider.__init__(self, "Radius")
        self.radius = 0.2

        self.origin = pg.Vector2(pos)
        self.worldposition = pos
        self.screenposition = [0, 0]
        self.collisions = []

        self.destroyed = False

        self.collected = False

        self.GameInfo = None

    def update(self, now, keys, GameInfo, dt):
        pc.GameObject.update(self, now, keys, GameInfo, dt)
        if not self.GameInfo:
            self.GameInfo = GameInfo
        self.worldposition.y = self.origin.y + (math.sin(now / 300) * 0.1)
        
    def collided_with(self, collision):
        if("Player" in collision.tags):
            self.collected = True
            self.GameInfo.soundplayer.PlaySound("Pickup")
            pass

    def Destroy(self):
        self.destroyed = True

    def draw(self, surface):
        if self.destroyed:
            return self
        pc.GameObject.draw(self, surface)

    def get_key(self, receivedKeys):
        return super().get_key(receivedKeys)

        
