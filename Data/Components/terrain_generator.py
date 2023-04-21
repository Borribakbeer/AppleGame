import pygame as pg
from pygame.math import Vector2
from ResourceManager import *
from Utils import ParentComponents as pc
from Utils import Tools
from Components import tilemap_generator
import numpy as np
import math

class TerrainGenerator():
    def __init__(self, camera):
        self.tags = {"COLLECTION"}
        self.camera = camera
        #Create chunks
        self.chunks = Tools.GameObjectsCollection()
        self.chunks.add(tilemap_generator.TileChunk(tilemap_generator.Tileset("Grass", 0, 0), pg.math.Vector2(0, 0), (10, 10), PIXELSCALE_IMAGES))
        self.chunks.add(tilemap_generator.TileChunk(tilemap_generator.Tileset("Grass", 0, 0), pg.math.Vector2(20, 0), (10, 10), PIXELSCALE_IMAGES))
        self.chunks.add(tilemap_generator.TileChunk(tilemap_generator.Tileset("Grass", 0, 0), pg.math.Vector2(-20, 0), (10, 10), PIXELSCALE_IMAGES))
        self.chunks.add(tilemap_generator.TileChunk(tilemap_generator.Tileset("Grass", 0, 0), pg.math.Vector2(0, 20), (10, 10), PIXELSCALE_IMAGES))
        self.chunks.add(tilemap_generator.TileChunk(tilemap_generator.Tileset("Grass", 0, 0), pg.math.Vector2(0, -20), (10, 10), PIXELSCALE_IMAGES))
        
        #Make chunks a default square
        map = np.array([[0, 3, 3, 3, 3, 3, 3, 3, 3, 6],
                        [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                        [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                        [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                        [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                        [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                        [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                        [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                        [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                        [2, 5, 5, 5, 5, 5, 5, 5, 5, 8]])
        for chunk in self.chunks.get_objects():
            chunk.set_map(map)

    def update(self, now, keys, dt):
        for chunk in self.chunks.get_objects():
            if math.dist(chunk.worldposition, self.camera.position) > CAMERA_UNLOAD_DISTANCE:
                self.chunks.remove(chunk, True)


    def get_objects(self):
        return self.chunks.get_objects()

    def draw(self, surface):
        pass

    def get_event(self, event):
        pass

    def get_key(self, keys):
        if keys[pg.K_r]:
            for chunk in self.chunks.get_objects():
                chunk.set_random()   

        if keys[pg.K_SPACE]:
            for chunk in self.chunks.get_objects():
                #Make chunks a default square
                map = np.array([[0, 3, 3, 3, 3, 3, 3, 3, 3, 6],
                                [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                                [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                                [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                                [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                                [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                                [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                                [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                                [1, 4, 4, 4, 4, 4, 4, 4, 4, 7],
                                [2, 5, 5, 5, 5, 5, 5, 5, 5, 8]])
                for chunk in self.chunks.get_objects():
                    chunk.set_map(map)
            