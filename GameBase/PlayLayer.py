import cocos
import pyglet
import socket


class KeyboardInputLayer(cocos.layer.Layer):
   """
   """

   # You need to tell cocos that your layer is for handling input!
   # This is key (no pun intended)!
   # If you don't include this you'll be scratching your head wondering why your game isn't accepting input
   is_event_handler = True

   def __init__(self):
      """ """
      super(KeyboardInputLayer, self).__init__()
      self.keys_being_pressed = set()

   def on_key_press(self, key, modifiers):
      """ """
      self.keys_being_pressed.add(key)

   def on_key_release(self, key, modifiers):
      """ """
      if key in self.keys_being_pressed:
         self.keys_being_pressed.remove(key)


class PlayLayerAction(cocos.actions.Action):
    """ 
    This class exists to forward the step(dt) method call to the 
    receiver's target object. It is a hook that enables targets to
    perform logic each time the display is updated.
    """
    
    def step(self, dt):
        """ """
        self.target.handleLocalKeyInput(dt)

class PlayLayer(KeyboardInputLayer):
   """ """
   ownID = socket.gethostbyname(socket.gethostname())
    
   def __init__(self):
      """ """
      super( PlayLayer, self ).__init__()
      self.players = {}
      self.batch = cocos.batch.BatchNode()
      self.add(self.batch)
      self.makePlayerFunc = None
      self.do(PlayLayerAction())

   def addPlayer(self, player_id):
      """ """
      new_player = None
      if player_id in self.players:
         new_player = self.players[player_id]
         new_player.setRandomPosition()
         new_player.onRespawn()
         #print 'respawning ', player_id
      else:
         new_player = self.makePlayerFunc(self, player_id)
         self.players[player_id] = new_player
         new_player.start(self)

      new_player.shouldDie = False
      if PlayLayer.ownID != player_id:
         pass
      else:
         pass

   def handleLocalKeyInput(self, dt):
      """ """
      if PlayLayer.ownID in self.players:
         local_player = self.players[PlayLayer.ownID]
         local_player.handleLocalKeyInput(self, dt)
      
if __name__ == "__main__":
   assert False
