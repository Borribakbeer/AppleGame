import pygame as pg
from pygame.math import Vector2
from ResourceManager import *
from Utils import ParentComponents as pc
import numpy as np

class Tilemap(pc.BaseSprite):
    def __init__(self, tileset, size=(10, 20), pixelscale = PIXELSCALE_IMAGES, rect=None, *groups):
        pg.sprite.Sprite.__init__(self, *groups)

        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)
        self.tags = {"DRAWABLE", "GROUND"}

        self.pixelscale = UNIT_SCALE * pixelscale

        h, w = self.size
        self.image = pg.Surface((pixelscale*w, pixelscale*h))
        if rect:
            self.rect = pg.Rect(rect)
        else:
            self.rect = self.tileset.rect

    def update(self, now, keys, dt):
        pass

    def draw(self, surface):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*UNIT_SCALE, i*UNIT_SCALE))
        pc.BaseSprite.draw(self, surface)

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        self.draw()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
    
    def get_event(self, event):
        pass

    def get_key(self, keys):
        if keys[pg.K_r]:
            self.set_random()
        pass

    def __str__(self):
        return f'{self.__class__.__name__}: {self.size}'      

class Tileset(object):
    def __init__(self, imageName, margin=1, spacing=1 , tilesize = pg.math.Vector2(PIXELSCALE_IMAGES, PIXELSCALE_IMAGES)):
        self.tiles = []
        self.image = GFX["Tilemaps"][imageName]   
        w, h = self.image.get_rect().size    
        self.size = (UNIT_SCALE, UNIT_SCALE)
        self.image = pg.transform.scale(self.image, (round((w / tilesize.x)*UNIT_SCALE), round((h / tilesize.y)*UNIT_SCALE)))
        self.margin = margin
        self.spacing = spacing
        self.rect = self.image.get_rect()
        self.load()

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        print(UNIT_SCALE)
        print(PIXELSCALE_IMAGES)
        print(f"Rectsize: w:{w}, h:{h}")

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pg.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)
        pass

    
