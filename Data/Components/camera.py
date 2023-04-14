import pygame as pg
import numpy as np
import math
from Utils import ParentComponents as pc
import ResourceManager as rc


class Camera(object):
    def __init__(self):
        self.position = pg.math.Vector2()
        self.size = 1000  # how many units the y axis of the camera is long
        self.velocity = pg.math.Vector2()


    def draw_frame(self, surface, objects):
        self.position = np.add(self.position, self.velocity)

        objects = objects.get_objects()

        drawableObjects = self.check_within_range(objects)

        self.set_objects_world_to_screen_space(drawableObjects)

        drawableObjects.custom_draw(surface)

    def set_objects_world_to_screen_space(self, objects):
        for obj in objects:
            obj.screenposition = self.world_to_screen_space(obj.worldposition)

    def check_within_range(self, objects):
        drawableObjects = CameraRenderGroup()
        for obj in objects:
            if not "DRAWABLE" in obj.tags:
                continue
            direction = obj.worldposition - self.position
            dist = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            if (dist < self.size) or ("ALWAYS_RENDER" in obj.tags):
                drawableObjects.add(obj)

        return drawableObjects

    def get_keys(self, keys):
        if keys[pg.K_UP]:
            self.velocity = rc.DIRECT_DICT["front"]
        elif keys[pg.K_DOWN]:
            self.velocity = rc.DIRECT_DICT["back"]
        elif keys[pg.K_LEFT]:
            self.velocity = rc.DIRECT_DICT["left"]
        elif keys[pg.K_RIGHT]:
            self.velocity = rc.DIRECT_DICT["right"]
        else:
            self.velocity = [0, 0]

        pass

    def uv_to_screen_space(self, coords):
        coords[0] = (coords[0] + 1) / 2.0
        coords[0] *= rc.SCREEN_SIZE[0]
        coords[1] = (coords[1] + 1) / 2.0
        coords[1] = 1 - coords[1]
        coords[1] *= rc.SCREEN_SIZE[1]
        return coords

    def world_to_screen_space(self, coords):
        direction = np.array(coords) - self.position
        direction[0] = direction[0] * (2.0 / ((self.size * rc.SCREEN_SIZE[0]) / rc.SCREEN_SIZE[1]))
        direction[1] = direction[1] * (2.0 / self.size)
        screenPos = self.uv_to_screen_space(direction)
        return screenPos

class CameraRenderGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        
    def custom_draw(self, surface):
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            sprite.reset_position(sprite.screenposition)
            surface.blit(sprite.image, sprite.rect)
