import cocos
import pyglet
import random
import math
import PlayLayer


class CollisionSpriteAction(cocos.actions.Action):
    """ 
    This class exists to forward the step(dt) method call to the 
    receiver's target object. It is a hook that enables targets to
    perform logic each time the display is updated.
    """
    
    def step(self, dt):
        """ """
        self.target.step(dt)


class CollisionSprite(cocos.sprite.Sprite):
    """
    This class exists to provide several features shared by almost
    every game object.
    
    Each instance has the following:
    A unique identifier
    A radius used to detect collisions with other CollisionSprite 
        instances
    Collision detections
    A flag, shouldDie, used to signal when the instance should be
    removed from the game.
    
    """
    next_unique_id = 1
    live_instances = {} # map unique_id to instance with that id

    @staticmethod
    def handleCollisions():
        """ """
        objects = CollisionSprite.live_instances.values()
        for object in objects:
            for other_object in objects:
                if other_object.id != object.id and \
                        object.isHitByCircle(other_object.position,\
                        other_object.radius):
                    object.onCollision(other_object)
    @staticmethod
    def getInstances(klass):
        """ """
        result = []
        for object in CollisionSprite.live_instances.values():
            if isinstance(object, klass):
                result.append(object)
        return result

    def __init__(self, anim, id=None, position=(0, 0), rotation=0,
            scale=1, opacity = 255, color=(255, 255, 255),
            anchor=None):
        """ """
        super( CollisionSprite, self ).__init__( anim, position, rotation,
            scale, opacity, color, anchor)
        if not id:
            self.id = CollisionSprite.next_unique_id
        else:
            self.id = id
        
        CollisionSprite.next_unique_id += 1
        self.radius = 3             # Small default radius
        self.shouldDie = False
        self.type = '_'
        CollisionSprite.live_instances[self.id] = self

    def getInfo(self):
        """ """
        x, y = self.position
        rot_deg = self.rotation
        return {'id':self.id,
            'type':self.type,
            'pos':(int(x), int(y)),
            'shouldDie' : self.shouldDie }
    
    def updateWithInfo(self, info):
        """ """
        self.position = info['pos']
        self.shouldDie = info['shouldDie']
    
    def setRandomPosition(self):
        width, height = cocos.director.director.get_window_size()
        self.position = (random.random() * width, random.random() * height)
    
    def markForDeath(self):
        """ """
        self.shouldDie = True
    
    def isHitByCircle(self, center, radius):
        """ Returns True if and only if the receiver's circle 
            calculated using the receiver's position and radius 
            overlaps the circle calculated using the center and radius 
            arguments to this method. 
        """
        total_radius = self.radius + radius
        total_radius_squared = total_radius * total_radius
        x, y = self.position
        delta_x = center[0] - x
        delta_y = center[1] - y
        distance_squared = delta_x * delta_x + delta_y * delta_y
        
        return distance_squared < total_radius_squared

    def processCollision(self, other_object):
        """ """
        playLayer = self.get_ancestor(PlayLayer.PlayLayer)
        #if playLayer:
        #    playLayer.addExplosion(self.position)
        return True
    
    def onRespawn(self):
        """ Adds the receiver back into collision detection set after
            receiver has respawned """
        CollisionSprite.live_instances[self.id] = self
        self.do(CollisionSpriteAction())
    
    def onCollision(self, other_object):
        """ """
        if self.processCollision(other_object):
            self.markForDeath()

    def start(self):
        """ """
        self.do(CollisionSpriteAction())
        
    def step(self, dt):
        """ Perform any updates that should occur after dt seconds 
            from the last update.
        """
        if self.shouldDie:
            self.stop()
            self.kill()
            if self.id in CollisionSprite.live_instances:
                del CollisionSprite.live_instances[self.id];


if __name__ == "__main__":
   assert False

