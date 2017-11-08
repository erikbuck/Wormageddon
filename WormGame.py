import GameBase.Game
import GameBase.CollisionSprite
import sys
import socket
import random
import cocos
import pyglet

atlasLarge = pyglet.resource.image('atlasLarge.png')
atlas = pyglet.resource.image('atlas.png')
grid = pyglet.image.ImageGrid(atlas, 4, 4)
textures = pyglet.image.TextureGrid(grid)
segmentSpacing = 24
boardWidth = 2048
boardHeight = 1400
   


##########################################################################################
###
class WormSegment(GameBase.CollisionSprite.CollisionSprite):
    """
    """
    
    def __init__(self, anim, id=None, position=(0, 0), rotation=0, scale=1,
                 opacity = 255, color=(255, 255, 255), anchor = None):
        """ """
        super( WormSegment, self ).__init__(anim, id, position, rotation,
            scale, opacity, color, anchor)
        
        if hasattr(anim, 'get_max_width'):
           # Radius is a bit less than half width
           self.radius = anim.get_max_width() * self.scale * 0.4
        else:
           self.radius = anim.width


##########################################################################################
###
class WormHead(WormSegment):
   """
   """

   def __init__(self, anim, id=None, position=(0, 0), rotation=0, scale=1,
              opacity = 255, color=(255, 255, 255), anchor = None):
      """ """
      super( WormHead, self ).__init__(anim, id, position, rotation,
         scale, opacity, color, anchor)
      self.worm = None
     
   def processCollision(self, other_object):
      """ Overrides inherited version so heads cannot collide with heads. """
      result = not isinstance(other_object, WormHead)
      if result:
         # Let inherited behavior rule the day
         super( WormHead, self ).processCollision(other_object)

      return result
     
   def on_arival(self):
      """ """
      self.worm.on_arival()
      
##########################################################################################
###
class WormPlayer(object):
   """ """

   directionDeltas = ((0, -segmentSpacing),
         (segmentSpacing, 0),
         (0, segmentSpacing),
         (-segmentSpacing, 0))
   numDirections = len(directionDeltas)
   directionDeltaChoices = [-1, 0, 0, 0, 0, 1]
   tail_textures_list = textures[4:8] + textures[0:4]
   frame_period = 1.0 / 12.0
   tail_animation = pyglet.image.Animation.from_image_sequence(
         tail_textures_list, frame_period, loop=True)
    
    
   def start(self, layer):
      """ """
      batch = layer.batch
      background = cocos.layer.ColorLayer(255, 255, 255, 255,
         width=boardWidth,
         height=boardHeight)
      layer.add(background, z=-2000)
      
      self.direction = random.randint(0, WormPlayer.numDirections - 1)  
      self.segments = [WormSegment(WormPlayer.tail_animation)]
      for i in range(1, random.randint(2,6)):
         self.segments.append(WormSegment(textures[8]))
      self.segments.append(WormHead(textures[12]))
      head = self.segments[-1]
      count = len(self.segments)
      index = count
      headPosition = (segmentSpacing, segmentSpacing)
      for i in range(0, count-1):
         batch.add(self.segments[i], z = index)
         self.segments[i].position = headPosition
         index -= 1
      batch.add(head, z = count)
      head.worm = self
      head.position = headPosition
      
      self.isAutomated = False
      head.on_arival()
      
   def moveTo(self, nextPos):
      """ """
      for i in range(0, len(self.segments)-1):
         self.segments[i].do(cocos.actions.MoveTo(
               self.segments[i+1].position, 0.5))
      self.segments[-1].do(cocos.actions.MoveTo(nextPos, 0.5)+\
            cocos.actions.CallFuncS(WormHead.on_arival))

   def getNextDirection(self):
      """ """
      result = self.direction + random.choice(WormPlayer.directionDeltaChoices)
      result = (result + WormPlayer.numDirections) % WormPlayer.numDirections
      return result
   
   def getHeadImageForDirection(self, direction):
      """ """
      return textures[12 + direction]

   def getNextPosition(self, nextDirection):
      """ """
      self.segments[-1].image = self.getHeadImageForDirection(nextDirection)
      deltas =  WormPlayer.directionDeltas[nextDirection]
      nextX = self.segments[-1].position[0] + deltas[0]
      nextY = self.segments[-1].position[1] + deltas[1]
      return (nextX, nextY)
   
   def on_arival(self):
      """ """
      pass
      
   def makeAutomatedMove(self):
      """ """
      nextDirection = self.getNextDirection()
      nextPos = self.getNextPosition(nextDirection)
      #print(nextPos)
      if not self.isPositionOnBoard(nextPos):
         nextPos = self.getNextPosition(nextDirection)
      if not self.isPositionOnBoard(nextPos):
         nextDirection = (self.direction - 1 + WormPlayer.numDirections) % WormPlayer.numDirections
         nextPos = self.getNextPosition(nextDirection)
      if not self.isPositionOnBoard(nextPos):
         nextDirection = self.direction
         nextPos = self.getNextPosition(nextDirection)

      self.direction = nextDirection
      self.moveTo(nextPos)

   def isPositionOnBoard(self, aPos):
      """ """
      return aPos[0] >= segmentSpacing and \
            aPos[1] >= segmentSpacing and \
            aPos[0] <= (boardWidth-segmentSpacing) and \
            aPos[1] <= boardHeight-segmentSpacing

   def handleLocalKeyInput(self, playLayer, dt):
      """ """
      deltas = (0, 0)
      deltaX = deltas[0]
      deltaY = deltas[1]
      
      if pyglet.window.key.LEFT in playLayer.keys_being_pressed:
         #print('Left')
         deltas = WormPlayer.directionDeltas[3]
         deltaX += deltas[0]
         deltaY += deltas[1]
      if pyglet.window.key.RIGHT in playLayer.keys_being_pressed:
         #print('Right')
         deltas = WormPlayer.directionDeltas[1]
         deltaX += deltas[0]
         deltaY += deltas[1]
      if pyglet.window.key.UP in playLayer.keys_being_pressed:
         #print('Up')
         deltas = WormPlayer.directionDeltas[2]
         deltaX += deltas[0]
         deltaY += deltas[1]
      if pyglet.window.key.DOWN in playLayer.keys_being_pressed:
         #print('Down')
         deltas = WormPlayer.directionDeltas[0]
         deltaX += deltas[0]
         deltaY += deltas[1]
         
      nextX = self.segments[-1].position[0] + deltaX
      nextY = self.segments[-1].position[1] + deltaY
      nextPos = (nextX, nextY)
      
      #print(nextPos)
      if self.isPositionOnBoard(nextPos):
         self.moveTo(nextPos)
   
##########################################################################################
###
def makeWormPlayer(layer, id):
   """ """
   return WormPlayer()
   
   
##########################################################################################
###
class WormPlayLayer(GameBase.PlayLayer.PlayLayer):
   """ """
   ownID = socket.gethostbyname(socket.gethostname())
    
   def __init__(self):
      """ """
      super( WormPlayLayer, self ).__init__()

      self.makePlayerFunc = makeWormPlayer
         

##########################################################################################
###
class WormGame(GameBase.Game.Game):
   """ """
   
   def getPlayLayer(self):
      """ """
      return WormPlayLayer()
   
   
##########################################################################################
###
if __name__ == "__main__":
    game = WormGame("Wormageddon")
    if len(sys.argv) == 2:
        host, port = sys.argv[1].split(":")
        print host, port
        game.run(host, int(port))
    else:
        game.run()
