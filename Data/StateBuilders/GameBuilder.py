from Utils import ParentComponents as pc
import ResourceManager as resources
import pygame as pg
from Utils import Tools
from Components import player, terrain_generator


def make_elements(camera):
    elements = Tools.GameObjectsCollection()
    playerObj = elements.add(player.Player(pg.math.Vector2(0,0)))
    playerObj.collisions =  elements.add(pc.GameObject("Debug", "Grid", pg.math.Vector2(0, 0), pg.math.Vector2(1, 1)))
    
    elements.add(terrain_generator.TerrainGenerator(camera, "Ground"))
    elements.add(terrain_generator.TerrainGenerator(camera, "Objects"))

    return elements    
