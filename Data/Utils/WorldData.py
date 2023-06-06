import pygame as pg
import os, json

class Object:
    def __init__(self, worldDataJson) :
        self.layers = []
        for layer in worldDataJson['layers']:
            self.layers.append(Layer(layer))
            
        self.tilesets = []
        for tileset in worldDataJson['tilesets']:
            self.tilesets.append(TileSet(tileset))
        
    
class Layer:
    def __init__(self, layerJson):
        self.layerName = layerJson['name']
        self.chunks = []
        for chunk in layerJson['chunks']:
            self.chunks.append(Chunk(chunk))
    
class Chunk:
    def __init__(self, chunkJson):
        self.data = chunkJson['data']
        self.position = pg.Vector2(chunkJson['x'], chunkJson['y'])
    
class TileSet:
    def __init__(self, tilesetJson):
        self.firstId = tilesetJson['firstgid']
        self.imageSource = self.GetSource(tilesetJson)

        
    def GetSource(self, tilesetJson):
        tilesetDataPath = tilesetJson['source']
        file = open(os.path.join("Resources", "World", tilesetDataPath),)
        jsonFile = json.load(file)
        path = jsonFile['image']
        path = path.replace('../../','')
        print(path)
        return os.path.join("Resources", path)
        