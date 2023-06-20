from Utils import ParentComponents as pc
import ResourceManager as resources
import pygame as pg
from Utils import Tools
from Components import player, terrain_generator, applecreator


def make_elements(camera):
    elements = Tools.GameObjectsCollection()
    elements.add(player.Player(pg.math.Vector2(0,0)))
    grid = elements.add(pc.GameObject("Debug", "Grid", pg.math.Vector2(3, 0), pg.math.Vector2(1, 1)))    
    pc.Collider.__init__(grid, "Box")
    
    elements.add(applecreator.AppleCreator())
    #elements.add(pc.Animation("Sprites", "MagicalGlow", pg.Vector2(-5, 0), (48, 48), 500))
    
    elements.add(terrain_generator.TerrainGenerator(camera, "Ground"))
    elements.add(terrain_generator.TerrainGenerator(camera, "Objects", True))

    return elements    
