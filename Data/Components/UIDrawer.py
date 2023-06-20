import pygame as pg
from ResourceManager import *
from datetime import timedelta

class UIDrawer():
    def __init__(self):
        pass

    def draw(self, surface, GameInfo):
        # Draw how many apples still need to be collected
        font = pg.font.Font(FONT_PATH, 50)
        applecounter = font.render(str(GameInfo.maxapples - GameInfo.applecount) + "/" + str(GameInfo.maxapples), False, pg.Color("white"))
        surface.blit(applecounter, (15, 15))



        #Draw how much time it took
        td = timedelta(milliseconds=(GameInfo.now - GameInfo.runstarttime))

        timetext = font.render("Time: " + str(td.seconds) + ":" + f'{round(td.microseconds/1000):03}', False, pg.Color("white"))
        rect = timetext.get_rect()
        surface.blit(timetext, (1280 - rect.width - 15, 15))


        pass
        
