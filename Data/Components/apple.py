import pygame as pg
from ResourceManager import *
from Utils import ParentComponents as pc
import math

class Apple(pc.GameObject):
    def __init__(self, pos, size = pg.Vector2(1, 1), *groups):
        pc.GameObject.__init__(self, "Sprites", "Apple", pos, size)
        pc.Collider.__init__(self, "Radius")
        self.radius = 0.2

        self.worldposition = pos
        self.screenposition = [0, 0]
        self.collisions = []

    def update(self, now, keys, GameInfo, dt):
        pc.GameObject.update(self, now, keys, GameInfo, dt)

        self.worldposition.y = math.sin(now / 300) * 0.1
        
    def collided_with(self, collision):
        if("Player" in collision.tags):
            pg.event.post(pg.event.Event(RESET_GAME))
            pass

        
