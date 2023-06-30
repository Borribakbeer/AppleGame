# Some Basic Components from which all other components can derive
import pygame as pg
import Utils.Tools as tools
import ResourceManager as resources


class BaseSprite(pg.sprite.Sprite):
    # A very basic base class that contains some commonly used functionality.
    def __init__(self, pos, size, *groups, setRect = False, rect = pg.Rect((0, 0), (0,0))):
        pg.sprite.Sprite.__init__(self, *groups)

        scalar = pg.math.Vector2(size) * resources.UNIT_SCALE
        self.image = pg.transform.scale(self.image, scalar)

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
        scalar = pg.math.Vector2(self.size) * resources.UNIT_SCALE
        self.image = pg.transform.scale(self.image, pg.Vector2(abs(scalar.x), abs(scalar.y)))

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

    def collision_is_true(self, collider):
        if hasattr(collider, 'collided_with') and callable(collider.collided_with):
            collider.collided_with(self)
        return True  
     
    def Collide(self, collider):
        if(self.collisionType == "None"):
            return False
        elif(collider.collisionType == "Box"):
            if(self.collisionrect.colliderect(collider.collisionrect)):
                return Collider.collision_is_true(self,collider)
            else:
                False
        elif(collider.collisionType == "Mask"):
            if(pg.Vector2.distance_to(self.nextWorldPosition, collider.worldposition) < self.radius + collider.radius*1.35):
                offset = pg.Vector2(collider.collisionrect.topleft) - pg.Vector2(self.collisionrect.topleft)
                if(self.mask.overlap_area(collider.mask, offset) > 0):
                    return Collider.collision_is_true(self,collider)
                else:
                    return False 
            else:
                return False
        elif(collider.collisionType == "Radius"):
            if(pg.Vector2.distance_to(self.nextWorldPosition, collider.worldposition) < self.radius + collider.radius):
                return Collider.collision_is_true(self,collider)
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
        self.nextWorldPosition += pg.math.Vector2(self.velocity) * (1/dt)
        
        self.collisionrect = pg.Rect(self.rect)
        setattr(self.collisionrect, "center", GameInfo.camera.world_to_screen_space(self.nextWorldPosition))
        
        if(GameInfo.colliders != None):
            self.check_collisions(GameInfo.colliders)
            

    def check_collisions(self, colliders, inTheRabbithole = False):
        for collider in colliders:
                if("COLLECTION" in collider.tags):
                    if self.check_collisions(collider.get_objects(), True):
                        return True
                    continue
                if(collider == self): 
                    continue
                if Collider.Collide(self, collider):
                    return True
        
        #If it is checking collision in a collection (down a rabbit hole) and not in the original space then we can't already update the position
        if inTheRabbithole:
            return False
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

class Animation(GameObject):
    def __init__(self, folder, name, pos, spritesize, frameratems, *groups):
        GameObject.__init__(self, folder, name, pos, pg.Vector2(spritesize) / resources.UNIT_SCALE, *groups)

        self.frames = self.GetFrames(spritesize, folder, name)

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        
        self.frameIndex = 0
        self.frameratems = frameratems
        self.timer = frameratems

    def GetFrames(self, spritesize, folder, name):
        w, h = resources.GFX[folder][name].get_size()
        frames = []

        for x in range(0, w, spritesize[0]):
                for y in range(0, h, spritesize[1]):
                    frame = pg.Surface(spritesize, pg.SRCALPHA, 32)
                    frame = frame.convert_alpha()
                    frame.blit(self.image, (0, 0), (x, y, *spritesize))
                    frames.append(frame)
        
        return frames
                
    def update(self, now, keys, GameInfo, dt):
        GameObject.update(self, now, keys, GameInfo, dt)

        if now > self.timer:
            self.timer = now + self.frameratems
            
            if self.frameIndex < len(self.frames):
                self.image.blit(self.frames[self.frameIndex], (0, 0))
                print(self.frameIndex)
                self.frameIndex = self.frameIndex + 1
            else:
                self.image = self.frames[0]
                print("Frame 0 at " + str(now))
                self.image.blit(self.frames[0], (0, 0))
                self.frameIndex = 1



