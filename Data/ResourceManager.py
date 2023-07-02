"""
This module initializes the display and creates dictionaries of resources.
Also contained are various constants used throughout the program.
"""

import os, json
import pygame as pg

from Utils import Tools

pg.init()

SCREEN_SIZE = (1280, 720)
ASPECT_RATIO = SCREEN_SIZE[0] / SCREEN_SIZE[1]

CAMERA_ZOOM = 15
CAMERA_UNLOAD_DISTANCE = CAMERA_ZOOM * 4
UNIT_SCALE = round(SCREEN_SIZE[1] / CAMERA_ZOOM)
def set_camera_zoom(zoom):
    global CAMERA_ZOOM
    global CAMERA_UNLOAD_DISTANCE
    global UNIT_SCALE

    CAMERA_ZOOM = zoom
    CAMERA_UNLOAD_DISTANCE = CAMERA_ZOOM * 4
    UNIT_SCALE = round(SCREEN_SIZE[1] / CAMERA_ZOOM)

PIXELSCALE_IMAGES = 16
ORIGINAL_CAPTION = "Apple Colector: Rise of the Wizard"
SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)
FONT_PATH = os.path.join("Resources", "Fonts", "Fixedsys500c.ttf")
BIG_FONT = pg.font.Font(FONT_PATH, 100)

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

DIRECT_DICT = {"front": pg.Vector2(0, 1),
               "back": pg.Vector2(0, -1),
               "left": pg.Vector2(-1, 0),
               "right": pg.Vector2(1, 0)}

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


_GFX_SUB_DIRECTORIES = ["Misc", "Debug", "Tilemaps", "UI", "Sprites"]
GFX = graphics_from_directories(_GFX_SUB_DIRECTORIES)

def sounds_from_directories(directories):
    """
    Calls the tools.load_all_sounds() function for all directories passed.
    """
    base_path = os.path.join("Resources", "Sounds")
    SFX = {}
    for directory in directories:
        path = os.path.join(base_path, directory)
        SFX[directory] = Tools.load_all_sounds(path)
    return SFX

_SOUND_SUB_DIRECTORIES = ["SFX"]
SFX = sounds_from_directories(_SOUND_SUB_DIRECTORIES)

MUSIC_PATHS = ["GerudoValley", "MasterKohga", "FallGuys", "Celeste", "TalusBattle"]
MUTED_MUSIC = True

import Utils.WorldData as WorldData

file = open(os.path.join("Resources", "World", "World.json"),)
WORLDDATA = WorldData.Object(json.load(file))


def load_chunk_from_position(position, layerName):
    #find layer
    failedSearch = True
    for layer in WORLDDATA.layers:
        if layer.layerName == layerName:
            chunkLayer = layer
            failedSearch = False
            break
    
    if failedSearch:
        print("Error: Failed to locate layer " + layerName + " in World.json")
        return [0] * 100
    
    failedSearch = True
    #find chunk in layer
    for chunk in chunkLayer.chunks:
        if(chunk.position.x == position.x / 2):
            if chunk.position.y == -position.y / 2:
                failedSearch = False
                return chunk.data
            
    if failedSearch:
        print("Error: Failed to locate chunk at " + str(position / 2) + " in World.json")
        return [0] * 100

    pass

#Custom Event Creation
RESET_GAME = pg.USEREVENT + 1
ENDING_MUSIC = pg.USEREVENT + 2