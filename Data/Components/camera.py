import pygame as pg
import numpy as np
import math
from Data.Utils import ParentComponents as pc
import Data.ResourceManager as rc


class Camera(object):
    def __init__(self):
        self.position = np.array([0, 0])
        self.size = 1000  # how many units the y axis of the camera is long

    def draw_frame(self, surface, objects):
        objects = objects.get_objects()

        drawableObjects = self.check_within_range(objects)

        self.set_objects_world_to_screen_space(drawableObjects)

        self.draw_objects(drawableObjects, surface)

    def set_objects_world_to_screen_space(self, objects):
        for obj in objects:
            obj.screenposition = self.world_to_screen_space(obj.worldPosition)

    def draw_objects(self, objects, surface):
        for obj in objects:
            obj.draw(surface)

    def check_within_range(self, objects):
        drawableObjects = []
        for obj in objects:
            direction = np.array(obj.screenposition) - np.array(self.position)
            dist = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            if (dist < self.size + 5) or ("ALWAYS_RENDER" in obj.tags):
                drawableObjects.append(obj)

        return drawableObjects

    def uv_to_screen_space(self, coords):
        coords[0] = (coords[0] + 1) / 2.0
        coords[0] *= rc.SCREEN_SIZE[0]
        coords[1] = (coords[1] + 1) / 2.0
        coords[1] *= rc.SCREEN_SIZE[1]
        return coords

    def world_to_screen_space(self, coords):
        direction = np.array(coords) - self.position
        direction[0] = direction[0] * (2.0 / self.size)
        direction[1] = direction[1] * (2.0 / self.size)
        screenPos = self.uv_to_screen_space(direction)
        return screenPos
