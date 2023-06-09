from Utils import ParentComponents as pc
import ResourceManager as resources
import pygame as pg
from Utils import Tools
from Components import player, terrain_generator


def make_elements(camera):
    elements = Tools.GameObjectsCollection()
    elements.add(player.Player(pg.math.Vector2(0,0)))
    grid = elements.add(pc.GameObject("Debug", "Grid", pg.math.Vector2(3, 0), pg.math.Vector2(1, 1), "Box"))    
    grid.add_tag("Collider")
    
    elements.add(terrain_generator.TerrainGenerator(camera, "Ground"))
    elements.add(terrain_generator.TerrainGenerator(camera, "Objects"))

    return elements    
