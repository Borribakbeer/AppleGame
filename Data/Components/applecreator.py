import pygame as pg
from ResourceManager import *
from Utils import ParentComponents as pc
from Stats import AppleStats
from Components import apple

class AppleCreator():
    def __init__(self):
        self.objects = []
        self.tags = {"COLLECTION", "APPLEBOX", "Collider"}

        for appledesc in AppleStats.apples:
            self.objects.append(apple.Apple(appledesc.pos))
            pass

    def add(self, obj):
        self.objects.append(obj)
        return obj

    def addCollection(self, collection):
        objects = collection.get_objects()
        for obj in objects:
            self.add(obj)

    def addIterable(self, iterable):
        for obj in iterable:
            self.add(obj)

    def remove(self, objToRemove, destroy=False):
        if(destroy):
            objToRemove.Destroy()
        self.objects.remove(objToRemove)

    def update(self,now, keys, GameInfo, dt):
        for obj in self.objects:
            if obj.update(now, keys, GameInfo, dt):
                self.remove(obj)

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

    def get_event(self, event):
        for obj in self.objects:
            obj.get_event(event)

    def get_key(self, keys):
        for obj in self.objects:
            obj.get_key(keys)

    def get_objects(self):
        return self.objects
