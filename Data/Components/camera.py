import pygame as pg
import numpy as np
import math
from Utils import ParentComponents as pc
import ResourceManager as rc


class Camera(object):
    def __init__(self):
        self.position = pg.math.Vector2()
        self.player = None
        self.velocity = pg.math.Vector2()
        self.objects = CameraRenderGroup()
        self.ground = CameraRenderGroup(False)
        self.mouseZoom = 0

    def draw_frame(self, surface, objectsCollection):
        if self.player:
            self.position = self.player.worldposition
        else:
            for obj in self.objects.sprites():
                if "Player" in obj.tags:
                    self.player = obj

        objects = objectsCollection.get_objects()

        self.check_within_range(objects)

        self.set_objects_world_to_screen_space(self.objects)
        self.set_objects_world_to_screen_space(self.ground)

        #Render order: (1 tilemaps, 2 un-y-sorted ground, 3 y-sorted objects)
        self.ground.custom_draw(surface)
        self.objects.custom_draw(surface)

    def set_objects_world_to_screen_space(self, objects):
        for obj in objects:
            obj.screenposition = self.world_to_screen_space(obj.worldposition)

    def check_within_range(self, objects):
        for obj in objects:
            if not "DRAWABLE" in obj.tags:
                if "COLLECTION" in obj.tags:
                    self.check_within_range(obj.get_objects())
                continue
            if "GROUND" in obj.tags:
                direction = obj.worldposition - self.position
                dist = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
                if (dist < rc.CAMERA_UNLOAD_DISTANCE) or ("ALWAYS_RENDER" in obj.tags):
                    self.ground.add(obj)
                continue

            direction = obj.worldposition - self.position
            dist = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            if (dist < rc.CAMERA_UNLOAD_DISTANCE) or ("ALWAYS_RENDER" in obj.tags):
                self.objects.add(obj)

    def get_event(self, event):
        if event == pg.MOUSEWHEEL:
            self.mouseZoom = event.y



    def world_to_screen_space(self, coords):
        # scaleY        
        # 0                     
        # -scaleY / -scaleX     0   scaleX
        
        size = rc.CAMERA_ZOOM;
        
        scaleY = size
        scaleX = (size / rc.SCREEN_SIZE[1]) * rc.SCREEN_SIZE[0]
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
                if sprite.draw(surface):
                    self.remove(sprite)
        else:
            for sprite in self.sprites():
                if sprite.draw(surface):
                    self.remove(sprite)
        
