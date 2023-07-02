import pygame as pg
import ResourceManager

class SoundPlayer():
    def __init__(self, Gameinfo):
        self.Game = Gameinfo
        pass
        
    def PlaySound(self, name):
        if not ResourceManager.MUTED_MUSIC:
            pg.mixer.Sound.play(ResourceManager.SFX["SFX"][name])
