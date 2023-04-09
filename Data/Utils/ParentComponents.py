# Some Basic Components from which all other components can derive
import pygame as pg
import Data.ResourceManager as resources
import numpy as np


class BaseSprite(pg.sprite.Sprite):
    # A very basic base class that contains some commonly used functionality.
    def __init__(self, pos, size, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.rect = pg.Rect(pos, size)
        self.exact_position = list(self.rect.topleft)
        self.old_position = self.exact_position[:]

    @property
    def delta_velocity(self):
        """
        Returns the total displacement undergone in a frame. Used for the
        interpolation of the sprite's location in the draw phase.
        """
        return (self.exact_position[0] - self.old_position[0],
                self.exact_position[1] - self.old_position[1])

    def set_position(self):
        pass

    def reset_position(self, value, attribute="topleft"):
        """
        Set the sprite's location variables to a new point.  The attribute
        argument can be specified to assign to a chosen attribute of the
        sprite's rect.
        """
        setattr(self.rect, attribute, value)
        self.exact_position = list(self.rect.topleft)
        self.old_position = self.exact_position[:]

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Rigidbody(object):
    def __init__(self):
        self.acceleration = [0, 0]
        self.velocity = [0, 0]
        self.worldPosition = [0.0, 0.0]

    def add_force(self, force):
        print("Adding force: " + str(force))
        self.velocity = np.add(self.velocity, force)
        print("current velocity: " + str(self.velocity))

    def update(self):
        dt = pg.time.Clock().get_time()
        self.velocity = np.add(self.velocity, self.acceleration)
        self.worldPosition = np.add(self.worldPosition, self.velocity)


class GameObject(BaseSprite):
    def __init__(self, folder, name, pos=(0, 0), size=(1, 1), *groups):
        self.image = resources.GFX[folder][name]
        self.position = pos
        BaseSprite.__init__(self, pos, self.image.get_size(), *groups)
        self.keys = []

    def update(self):
        pass

    def draw(self, surface):
        BaseSprite.reset_position(self, self.position)
        BaseSprite.draw(self, surface)

    def get_event(self, event):
        pass

    def get_key(self, receivedKeys):
        self.keys = receivedKeys
