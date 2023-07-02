from Utils import ParentComponents as pc
import ResourceManager as resources
import pygame as pg
import math


class TitleImage(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = resources.GFX["UI"]["Title"]

        self.rect = resources.SCREEN_RECT



class AnyKey(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.rawimage = resources.GFX["UI"]["PressPlayDark"]
        self.null_image = resources.GFX["UI"]["PressPlayLight"]
        self.image = self.rawimage
        self.rect = resources.SCREEN_RECT

    def update(self, now):
        if now % 1000 < 500:
            self.image = self.rawimage
        else:
            self.image = self.null_image

class AppleGlow(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.rawimage = resources.GFX["UI"]["AppleGlow"]
        self.image = self.rawimage
        self.rect = self.rawimage.get_rect()
        self.rect.center = (640, 371)

    def update(self, now):
        #Scale
        w, h = self.rawimage.get_size()
        scalar = 1 + (((math.sin(now/500) + 1) / 2) * 0.25)
        self.image = pg.transform.scale(self.rawimage, (w * scalar, h * scalar))
        #Rotate
        self.image = pg.transform.rotate(self.image, (now/1000) * 45)
        #keep position
        self.rect = self.image.get_rect()
        self.rect.center = (640, 371)


class Apple(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.rawimage = resources.GFX["Sprites"]["Apple"]
        self.image = pg.transform.scale(self.rawimage, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.center = (640, 367)

    def update(self, now):
        pass


class Player(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = resources.GFX["UI"]["MainMenuPlayer"]

        self.rect = resources.SCREEN_RECT.copy()
    
    def update(self, now):
        self.rect.topleft = (0, math.sin(now/500) * 5)
        


def render_font(font, size, msg, color=(255, 255, 255)):
    """
    Takes the name of a loaded font, the size, and the color and returns
    a rendered surface of the msg given.
    """
    selected_font = pg.font.Font(resources.FONTS[font], size)
    return selected_font.render(msg, True, color)
