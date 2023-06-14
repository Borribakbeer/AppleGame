import pygame as pg
from pygame.math import Vector2
from ResourceManager import *
from Utils import ParentComponents as pc
from Utils import Tools
from Components import tilemap_generator
import numpy as np
import math

class TerrainGenerator():
    def __init__(self, camera, tilemapLayer = "Ground", hasCollision = False):
        self.tags = {"COLLECTION"}
        if hasCollision:
             self.tags.add("Collider")
        self.camera = camera
        self.lastCameraPosition = Vector2(1, 0)
        self.tilemapLayer = tilemapLayer
        #Create chunks
        self.chunks = Tools.GameObjectsCollection()
        self.hasCollision = hasCollision
        

    def update(self, now, keys, GameInfo, dt):
        chunksToCheck = []
        chunksToCheck += self.chunks.get_objects()
        rounded_camera_position = pg.math.Vector2(self.camera.position.x, self.camera.position.y)
        rounded_camera_position.x = round(rounded_camera_position.x / 2, -1)*2
        rounded_camera_position.y = round(rounded_camera_position.y / 2, -1)*2        

        if(self.lastCameraPosition != rounded_camera_position):
            #Set testposition to top left
            rounded_camera_position.x -= round(40, -1)
            rounded_camera_position.y -= round(20, -1)
            #check every nessecary position
            for x in range(5):
                for y in range(4):
                        chunksToCheck = self.check_position_for_chunk(chunksToCheck, pg.math.Vector2(rounded_camera_position.x + x * 20, rounded_camera_position.y + y * 20))

            #Delete chunks that are outside of range
            for chunk in chunksToCheck:
                chunk.destroyed = True
                self.chunks.remove(chunk)

            self.lastCameraPosition = rounded_camera_position

        
    def check_position_for_chunk(self, chunksToCheck, position):
        found = False
        for chunk in chunksToCheck:
            if chunk.worldposition == position:
                chunksToCheck.remove(chunk)
                found = True
                break
        if not found:
                self.chunks.add(tilemap_generator.TileChunk(tilemap_generator.Tileset(WORLDDATA.tilesets, 0, 0), position, (10, 10), PIXELSCALE_IMAGES, self.tilemapLayer, self.hasCollision))

        return chunksToCheck      
        

    def get_objects(self):
        return self.chunks.get_objects()

    def draw(self, surface):
        pass

    def get_event(self, event):
        pass

    def get_key(self, keys):
        self.chunks.get_keys(keys)
            