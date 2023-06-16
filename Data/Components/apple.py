import pygame as pg
from ResourceManager import *
from Utils import ParentComponents as pc

class Apple(pc.GameObject):
    def __init__(self, pos, size = pg.Vector2(1, 1), *groups):
        pc.GameObject.__init__(self, "Sprites", "Apple", pos, size)
        pc.Collider.__init__(self, "Radius")
        self.radius = 0.2

        self.worldposition = pos
        self.screenposition = [0, 0]
        self.collisions = []
        
    def collided_with(self, collision):
        if("Player" in collision.tags):
            print("Reset")
            pg.event.post(pg.event.Event(RESET_GAME))

        
