import pygame as pg
from ResourceManager import *

class UIDrawer():
    def __init__(self):
        pass

    def draw(self, surface, GameInfo):
        # Draw how many apples still need to be collected
        font = pg.font.Font(FONT_PATH, 50)
        _render = font.render(str(GameInfo.maxapples - GameInfo.applecount) + "/" + str(GameInfo.maxapples), False, pg.Color("white"))
        surface.blit(_render, (50, 15))

        #Draw how much time it took
        _render = font.render("Time: " + str(GameInfo.now - GameInfo.runstarttime), False, pg.Color("white"))
        surface.blit(_render, (50, 80))


        pass
        
