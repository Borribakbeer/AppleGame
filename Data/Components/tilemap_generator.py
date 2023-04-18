import pygame as pg
from ResourceManager import *
from Utils import ParentComponents as pc
import numpy as np

class TileChunk(pc.BaseSprite):
    def __init__(self, tileset, pos, size=(8, 8), pixelscale = PIXELSCALE_IMAGES, *groups):
        pg.sprite.Sprite.__init__(self, *groups)

        self.worldposition = pos
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)
        self.tags = {"DRAWABLE", "GROUND"}

        self.pixelscale = UNIT_SCALE * pixelscale

        h, w = self.size
        self.image = pg.Surface((w * UNIT_SCALE, h * UNIT_SCALE))
        self.rect = self.tileset.rect

        self.exact_position = list(self.rect.topleft)
        self.old_position = self.exact_position[:]

        self.construct_image()

    def update(self, now, keys, dt):
        pass

    def draw(self, surface):
        pc.BaseSprite.reset_position(self, self.screenposition)
        pc.BaseSprite.draw(self, surface)

    def construct_image(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*UNIT_SCALE, i*UNIT_SCALE))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        self.construct_image()

    def set_map(self, map):
        self.map = map
        self.construct_image()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        self.construct_image()
    
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

    
