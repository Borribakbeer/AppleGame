# Some Basic Components from which all other components can derive
import pygame as pg
import Utils.Tools as tools
import ResourceManager as resources
import numpy as np


class BaseSprite(pg.sprite.Sprite):
    # A very basic base class that contains some commonly used functionality.
    def __init__(self, pos, size, *groups, setRect = False, rect = pg.Rect((0, 0), (0,0))):
        pg.sprite.Sprite.__init__(self, *groups)

        size = pg.math.Vector2(size) * resources.UNIT_SCALE
        self.image = pg.transform.scale(self.image, size)

        if setRect:
            self.rect = rect
        else:
            self.pixelsize = pg.math.Vector2(self.image.get_size())
            leftTopPosition = pos - (self.pixelsize / 2)
            self.rect = pg.Rect(leftTopPosition, self.pixelsize)

        self.exact_position = list(self.rect.topleft)
        self.old_position = self.exact_position[:]

    def reset_position(self, value, attribute="center"):
        #Relocate the sprite
        setattr(self.rect, attribute, value)
        self.exact_position = list(self.rect.center)
        self.old_position = self.exact_position[:]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        return True


class Rigidbody(object):
    def __init__(self, pos):
        self.acceleration = pg.math.Vector2()
        self.velocity = pg.math.Vector2()
        self.worldposition = pos

    def add_force(self, force):
        self.velocity += force

    def update(self, dt):
        self.velocity = [self.velocity[x] + self.acceleration[x] for x in range(len(self.acceleration))]
        self.worldposition += pg.math.Vector2(self.velocity) * (dt / 1000)


class GameObject(BaseSprite):
    def __init__(self, folder, name, pos, size, *groups):
        self.size = size
        self.worldposition = pos

        self.image = resources.GFX[folder][name]        

        BaseSprite.__init__(self, pos, size, *groups)

        self.keys = []

        # Possible tags are: "ALWAYS_RENDER", "DRAWABLE"
        self.tags = {"DRAWABLE"}

    def update(self, now, keys, dt):
        pass

    def draw(self, surface):
        BaseSprite.reset_position(self, self.screenposition)
        BaseSprite.draw(self, surface)

    def get_event(self, event):
        pass

    def get_key(self, receivedKeys):
        self.keys = receivedKeys

    def Destroy(self):
        raise Exception("No handling was implemeted for destruction of object")
