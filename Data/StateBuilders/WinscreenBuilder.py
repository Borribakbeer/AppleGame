from Utils import ParentComponents as pc
import ResourceManager as resources
import pygame as pg

class RestartButton(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)

        self.unpressed = resources.GFX["UI"]["RestartButton"]
        self.pressed = resources.GFX["UI"]["RestartButtonPressed"]

        self.rect = self.unpressed.get_rect()

        self.image = self.unpressed


    def update(self, now):
        pass

    def Activate(self):
        pg.event.post(pg.event.Event(resources.RESET_GAME))
        pass 

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.image = self.pressed

        if event.type == pg.MOUSEBUTTONUP:
            self.image = self.unpressed
            self.Activate()

        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if keys[pg.K_r]:
                self.Activate()
        pass

class WinText(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = resources.GFX["UI"]["WinscreenBG"]

        self.rect = resources.SCREEN_RECT

    def get_event(self, event):
        pass

class HighscoreText():
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = resources.GFX["UI"]["HighscoreText"]

        self.rect = resources.SCREEN_RECT

    def draw(self, surface):
        surface.blit(self.image, [0, 0])
        pass


def render_font(font, size, msg, color=(255, 255, 255)):
    """
    Takes the name of a loaded font, the size, and the color and returns
    a rendered surface of the msg given.
    """
    selected_font = pg.font.Font(resources.FONTS[font], size)
    return selected_font.render(msg, True, color)
