import pygame as pg
import numpy as np
import math
from Data.Utils import ParentComponents as pc


class Camera(object):
    def __init__(self):
        self.position = [0, 0]
        self.size = 10

    def draw_frame(self, surface, objects):
        drawableObjects = self.check_within_range(objects)

        # Todo: Render objects to surface at correct position

    def check_within_range(self, objects):
        drawableObjects = []
        for obj in objects:
            direction = np.array(obj.position) - np.array(self.position)
            dist = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            if (dist < self.size + 5) or ("ALWAYS_RENDER" in obj.tags):
                drawableObjects.append(obj)

        return drawableObjects
