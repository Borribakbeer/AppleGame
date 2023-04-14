"""
This module initializes the display and creates dictionaries of resources.
Also contained are various constants used throughout the program.
"""

import os
import pygame as pg

from Utils import Tools

pg.init()

SCREEN_SIZE = (1280, 720)
ORIGINAL_CAPTION = "The Apple Game"
SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)
_FONT_PATH = os.path.join("Resources", "Fonts", "Fixedsys500c.ttf")
BIG_FONT = pg.font.Font(_FONT_PATH, 100)

# Initialization
pg.display.set_caption(ORIGINAL_CAPTION)
_screen = pg.display.set_mode(SCREEN_SIZE)

# Display until loading finishes.
_screen.fill((255, 0, 255))
_render = BIG_FONT.render("LOADING...", False, pg.Color("white"))
_screen.blit(_render, _render.get_rect(center=SCREEN_RECT.center))
pg.display.update()

# General constants
DIRECTIONS = ["front", "back", "left", "right"]

DIRECT_DICT = {"front": (0, 1),
               "back": (0, -1),
               "left": (-1, 0),
               "right": (1, 0)}

# Draw layer order for all types of items.
Z_ORDER = {"Background": -100,
           "Foreground": 100}

# Resource loading (Fonts and music just contain path names).
SAVE_PATH = os.path.join("Resources", "Save_data", "save_data.save")
FONTS = Tools.load_all_fonts(os.path.join("Resources", "Fonts"))


def graphics_from_directories(directories):
    """
    Calls the tools.load_all_graphics() function for all directories passed.
    """
    base_path = os.path.join("Resources", "Graphics")
    GFX = {}
    for directory in directories:
        path = os.path.join(base_path, directory)
        GFX[directory] = Tools.load_all_gfx(path)
    return GFX


_SUB_DIRECTORIES = ["Misc", "Debug"]
GFX = graphics_from_directories(_SUB_DIRECTORIES)
