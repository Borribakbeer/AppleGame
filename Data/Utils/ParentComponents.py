# Some Basic Components from which all other components can derive
import pygame as pg
import Data.ResourceManager as resources


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
        self.acceleration = (0, 0)
        self.velocity = (0, 0)
        self.position = (0, 0)

    def get_position(self):
        return self.position

    def add_force(self, force):
        self.velocity += force

    def update(self):
        dt = pg.time.Clock.get_time()
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt


class GameObject(BaseSprite):
    def __init__(self, folder, name, pos=(0, 0), size=(1, 1), *groups):
        self.image = resources.GFX[folder][name]
        BaseSprite.__init__(self, pos, self.image.get_size(), *groups)

    def update(self):
        pass

    def draw(self, surface):
        BaseSprite.reset_position(self.position)
        BaseSprite.draw(surface)
