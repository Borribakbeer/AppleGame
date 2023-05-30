import pygame as pg
from ResourceManager import *
from Utils import ParentComponents as pc
import numpy as np

class TileChunk(pc.BaseSprite):
    def __init__(self, tileset, pos, size=(8, 8), pixelscale = PIXELSCALE_IMAGES, tilemapLayer = 'Ground', *groups):
        pg.sprite.Sprite.__init__(self, *groups)

        self.worldposition = pos
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)
        self.tags = {"DRAWABLE", "GROUND"}

        self.pixelscale = UNIT_SCALE * pixelscale

        h, w = self.size
        self.image = pg.Surface((w * UNIT_SCALE, h * UNIT_SCALE), pg.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.tileset.rect

        self.destroyed = False

        self.exact_position = list(self.rect.topleft)
        self.old_position = self.exact_position[:]

        self.set_map(pos, tilemapLayer)
        

    def update(self, now, keys, dt):
        if self.destroyed:
            return self
        pass

    def draw(self, surface):
        if self.destroyed:
            return self
        pc.BaseSprite.reset_position(self, self.screenposition)
        pc.BaseSprite.draw(self, surface)

    def construct_image(self):
        h, w = self.size
        self.image = pg.Surface((w * UNIT_SCALE, h * UNIT_SCALE), pg.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        m, n = self.map.shape
        counter = 0
        for i in range(m):
            for j in range(n):
                if self.map[counter] == -1:
                    continue

                tile = self.tileset.tiles[self.map[counter]]
                self.image.blit(tile, (j*UNIT_SCALE, i*UNIT_SCALE))
                counter += 1


    def set_map(self, position, tilemapLayer):
        self.map = load_chunk_from_position(position, tilemapLayer)
        self.construct_image()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        self.construct_image()
    
    def get_event(self, event):
        pass

    def get_key(self, keys):
        pass

    def Destroy(self):
        self.destroyed = True

    def __str__(self):
        return f'{self.__class__.__name__}: {self.size}, \n{self.map}'      

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

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pg.Surface(self.size, pg.SRCALPHA, 32)
                tile = tile.convert_alpha()
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)
        pass

    
