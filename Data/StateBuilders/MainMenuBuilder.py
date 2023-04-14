from Utils import ParentComponents as pc
import ResourceManager as resources
import pygame as pg


class TitleImage(pc.BaseSprite):
    def __init__(self, *groups):
        self.image = resources.GFX["Misc"]["Title"]
        pc.BaseSprite.__init__(self, pg.math.Vector2(0, 0), pg.math.Vector2(1, 1), *groups)
        self.needed_groups = groups


class AnyKey(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.rawimage = render_font("Fixedsys500c", 30,
                                 "[Press Any Key]", (255, 255, 0))
        self.null_image = pg.Surface((1,1)).convert_alpha()
        self.null_image.fill((0,0,0,0))
        self.image = self.rawimage
        center = (resources.SCREEN_RECT.centerx, 650)
        self.rect = self.image.get_rect(center=center)

    def update(self, now):
        if now % 700 < 350:
            self.image = self.rawimage
        else:
            self.image = self.null_image



def render_font(font, size, msg, color=(255, 255, 255)):
    """
    Takes the name of a loaded font, the size, and the color and returns
    a rendered surface of the msg given.
    """
    selected_font = pg.font.Font(resources.FONTS[font], size)
    return selected_font.render(msg, True, color)
