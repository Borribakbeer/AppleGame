import pygame as pg
from pygame.math import Vector2
from ResourceManager import *
from Utils import ParentComponents as pc
from Utils import Tools
import tilemap_generator
import numpy as np

class TerrainGenerator():
    def __init__(self):
        self.camera
        elements = Tools.GameObjectsCollection()
        elements.add(tilemap_generator.TileChunk(tilemap_generator.Tileset("Grass", 0, 0), pg.math.Vector2(0, 0), (10, 10), PIXELSCALE_IMAGES))
        elements.add(tilemap_generator.TileChunk(tilemap_generator.Tileset("Grass", 0, 0), pg.math.Vector2(20, 0), (10, 10), PIXELSCALE_IMAGES))
        elements.add(tilemap_generator.TileChunk(tilemap_generator.Tileset("Grass", 0, 0), pg.math.Vector2(-20, 0), (10, 10), PIXELSCALE_IMAGES))
        elements.add(tilemap_generator.TileChunk(tilemap_generator.Tileset("Grass", 0, 0), pg.math.Vector2(0, 20), (10, 10), PIXELSCALE_IMAGES))
        elements.add(tilemap_generator.TileChunk(tilemap_generator.Tileset("Grass", 0, 0), pg.math.Vector2(0, -20), (10, 10), PIXELSCALE_IMAGES))
        pass