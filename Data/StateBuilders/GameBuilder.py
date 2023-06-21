from Utils import ParentComponents as pc
import ResourceManager as resources
import pygame as pg
from Utils import Tools
from Components import player, terrain_generator, applecreator


def make_elements(camera):
    elements = Tools.GameObjectsCollection()
    elements.add(player.Player(pg.math.Vector2(-20, 10)))
    
    elements.add(applecreator.AppleCreator())
    
    elements.add(terrain_generator.TerrainGenerator(camera, "Ground"))
    elements.add(terrain_generator.TerrainGenerator(camera, "Objects", True))

    return elements    
