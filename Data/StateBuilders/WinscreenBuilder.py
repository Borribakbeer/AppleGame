from Utils import ParentComponents as pc
import ResourceManager as resources
import pygame as pg

class RestartButton(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.text = render_font("Fixedsys500c", 100,
                                 "[Restart]", (100, 0, 100))
        center = (resources.SCREEN_RECT.centerx, 600)
        self.rect = self.text.get_rect(center=center)

        self.image = pg.Surface((self.rect.width, self.rect.height))
        self.image.fill((200, 255, 150))
        self.image.blit(self.text, (0,0))

    def update(self, now):
        pass

    def Activate(self):
        pg.event.post(pg.event.Event(resources.RESET_GAME))
        pass 

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.image.fill((100, 200, 150))
            self.image.blit(self.text, (0,0))

        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()

            if self.rect.collidepoint(pos):
                self.image.fill((200, 255, 150))
                self.image.blit(self.text, (0,0))
                self.Activate()
        pass

class WinText(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = render_font("Fixedsys500c", 200,
                                 "You Win!", (255, 255, 255))
        center = (resources.SCREEN_RECT.centerx, 250)
        self.rect = self.image.get_rect(center=center)

    def get_event(self, event):
        pass



def render_font(font, size, msg, color=(255, 255, 255)):
    """
    Takes the name of a loaded font, the size, and the color and returns
    a rendered surface of the msg given.
    """
    selected_font = pg.font.Font(resources.FONTS[font], size)
    return selected_font.render(msg, True, color)
