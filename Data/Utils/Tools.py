# Some usefull tools
import os
import pygame as pg


# [<<<Manage Resource Loading...>>>]
def load_all_gfx(path, tint=(255, 0, 255), accept=(".png", ".jpg")):
    """
        Load all graphics that have correct extensions.
        If alpha transparency is found in the image the image will be converted using
        convert_alpha().
        If no alpha transparency is detected image will be
        converted using convert() and tint will be set.
    """
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(tint)
            graphics[name] = img
    return graphics


def load_all_fonts(directory, accept=(".ttf",)):
    """
    Create a dictionary of paths to font files in given directory
    if their extensions are correct
    """
    fonts = {}
    for font in os.listdir(directory):
        name, ext = os.path.splitext(font)
        if ext.lower() in accept:
            fonts[name] = os.path.join(directory, font)
    return fonts
