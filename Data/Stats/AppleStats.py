import pygame as pg

class AppleDescriber:
    def __init__(self, position):
        self.pos = position

apples = []

apples.append(AppleDescriber(pg.Vector2(5, 0)))
apples.append(AppleDescriber(pg.Vector2(5, 5)))
apples.append(AppleDescriber(pg.Vector2(0, 5)))