import pygame as pg
from ResourceManager import *

class SoundPlayer():
    def __init__(self):
        pass
        
    def PlaySound(self, name):
        pg.mixer.Sound.play(SFX["SFX"][name])
