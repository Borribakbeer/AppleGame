import pygame as pg
import numpy as np
import math
from Utils import ParentComponents as pc
import ResourceManager as rc


class Camera(object):
    def __init__(self):
        self.position = pg.math.Vector2()
        self.size = rc.CAMERA_ZOOM # how many units the y axis of the camera is long
        self.velocity = pg.math.Vector2()
        self.objects = CameraRenderGroup()
        self.ground = CameraRenderGroup(False)

    def draw_frame(self, surface, objects):
        self.position = np.add(self.position, self.velocity)

        objects = objects.get_objects()

        self.check_within_range(objects)

        self.set_objects_world_to_screen_space(self.objects)
        self.set_objects_world_to_screen_space(self.ground)

        self.ground.custom_draw()
        self.objects.custom_draw(surface)


    def set_objects_world_to_screen_space(self, objects):
        for obj in objects:
            obj.screenposition = self.world_to_screen_space(obj.worldposition)

    def check_within_range(self, objects):
        for obj in objects:
            if not "DRAWABLE" in obj.tags:
                continue
            if "GROUND":
                self.ground.add(obj)
                continue
            direction = obj.worldposition - self.position
            dist = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            if (dist < self.size * rc.ASPECT_RATIO * 1.3) or ("ALWAYS_RENDER" in obj.tags):
                self.drawableObjects.add(obj)

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


    def world_to_screen_space(self, coords):
        # scaleY        
        # 0                     
        # -scaleY / -scaleX     0   scaleX
        scaleY = self.size
        scaleX = (self.size / rc.SCREEN_SIZE[1]) * rc.SCREEN_SIZE[0]
        direction = coords - self.position
        
        direction[0] = (direction[0] + scaleX) / (2 * scaleX)
        direction[0] *= rc.SCREEN_SIZE[0]
        
        direction[1] = -(direction[1] - scaleY) / (2 * scaleY)
        direction[1] *= rc.SCREEN_SIZE[1]
        return direction

class CameraRenderGroup(pg.sprite.Group):
    def __init__(self, sorting = True):
        self.sorting = sorting
        super().__init__()
        
    def custom_draw(self, surface):
        if self.sorting:
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                sprite.reset_position(sprite.screenposition)
                surface.blit(sprite.image, sprite.rect)
        else:
            for sprite in self.sprites():
                sprite.reset_position(sprite.screenposition)
                surface.blit(sprite.image, sprite.rect)
