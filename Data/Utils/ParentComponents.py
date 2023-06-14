# Some Basic Components from which all other components can derive
import pygame as pg
import Utils.Tools as tools
import ResourceManager as resources


class BaseSprite(pg.sprite.Sprite):
    # A very basic base class that contains some commonly used functionality.
    def __init__(self, pos, size, *groups, setRect = False, rect = pg.Rect((0, 0), (0,0))):
        pg.sprite.Sprite.__init__(self, *groups)

        size = pg.math.Vector2(size) * resources.UNIT_SCALE
        self.image = pg.transform.scale(self.image, size)

        if setRect:
            self.rect = rect
        else:
            self.pixelsize = pg.math.Vector2(self.image.get_size())
            leftTopPosition = pos - (self.pixelsize / 2)
            self.rect = pg.Rect(leftTopPosition, self.pixelsize)

        self.exact_position = list(self.rect.topleft)
        self.old_position = self.exact_position[:]

    def reset_position(self, value, attribute="center"):
        #Relocate the sprite
        setattr(self.rect, attribute, value)
        self.exact_position = list(self.rect.center)
        self.old_position = self.exact_position[:]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        return True


class Collider:
    def __init__(self, collisionType):
        self.collisionType = collisionType
        self.radius = max(self.size)
        self.collisionrect = self.rect
        self.add_tag("Collider")
        
        if(collisionType == "Mask"):
            self.mask = pg.mask.from_surface(self.image)

        
    def Collide(self, collider):
        if(self.collisionType == "None"):
            return False
        elif(self.collisionType == "Box"):
            return self.collisionrect.colliderect(collider.collisionrect)
        elif(self.collisionType == "Mask"):
            if(pg.Vector2.distance_to(self.nextWorldPosition, collider.worldposition) < self.radius + collider.radius):
                offset = pg.Vector2(collider.collisionrect.topleft) - pg.Vector2(self.collisionrect.topleft)
                print(str(self.mask.overlap_area(collider.mask, offset)))
                return self.mask.overlap_area(collider.mask, offset) > 0
            else:
                return False
        elif(self.collisionType == "Radius"):
            if(pg.Vector2.distance_to(self.nextWorldPosition, collider.worldposition) < self.radius + collider.radius):
                return True
            else:
                return False
        else:
            print("Collisiontype: '" + self.collisionType + "' is not implemented yet")
            return False

class Rigidbody(object):
    def __init__(self, pos):
        self.acceleration = pg.math.Vector2(0, 0)
        self.velocity = pg.math.Vector2()
        self.worldposition = pos
        self.nextWorldPosition = pos

    def add_force(self, force):
        self.velocity += force
        
    def update(self, GameInfo, dt):        
        self.nextWorldPosition = pg.Vector2(self.worldposition.x, self.worldposition.y)
        self.velocity += self.acceleration
        self.nextWorldPosition += pg.math.Vector2(self.velocity) * (dt / 1000)
        
        self.collisionrect = pg.Rect(self.rect)
        setattr(self.collisionrect, "center", GameInfo.camera.world_to_screen_space(self.nextWorldPosition))
        
        if(GameInfo.colliders != None):
            self.check_collisions(GameInfo.colliders)
            

    def check_collisions(self, colliders):
        for collider in colliders:
                if("COLLECTION" in collider.tags):
                    if self.check_collisions(collider.get_objects()):
                        return
                    continue
                if(collider == self): 
                    continue
                if Collider.Collide(self, collider):
                    return True
        #THE FOLLOWING CODE IS ONLY EXECUTED WHEN THERE HAS NOT BEEN ANY COLLISION
        
        self.worldposition = self.nextWorldPosition

        return False
        


class GameObject(BaseSprite):
    def __init__(self, folder, name, pos, size, *groups):
        self.size = size
        self.worldposition = pos

        self.image = resources.GFX[folder][name]   
        
        self.colliders = None     

        BaseSprite.__init__(self, pos, size, *groups)

        self.keys = []

        # Possible tags are: "ALWAYS_RENDER", "DRAWABLE"
        self.tags = {"DRAWABLE"}

    def update(self, now, keys, GameInfo, dt):
        pass

    def draw(self, surface):
        BaseSprite.reset_position(self, self.screenposition)
        BaseSprite.draw(self, surface)

    def get_event(self, event):
        pass

    def get_key(self, receivedKeys):
        self.keys = receivedKeys

    def Destroy(self):
        raise Exception("No handling was implemeted for destruction of object")
    
    def add_tag(self, tag):
        self.tags.add(tag)
