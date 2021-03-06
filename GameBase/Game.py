import GameServer
import PlayLayer
import cocos
from cocos.scenes.transitions import FadeTRTransition
import pyglet


class Game(object):
   """
   """

   default_window_width = 1024
   default_window_height = 768

   def __init__(self, title = "--------"):
      """ """
      super( Game, self ).__init__()

      director_width = Game.default_window_width
      director_height = Game.default_window_height

      caption = title + ' ' + PlayLayer.PlayLayer.ownID
      cocos.director.director.init(director_width, director_height,
         caption = caption, fullscreen=False)

      intro_layer = self.getPlayLayer()
      intro_layer.anchor_x = director_width * 0.5
      intro_layer.anchor_y = director_height * 0.5

      intro_menu = IntroMenu(self)
      intro_layer.add(intro_menu)

      self.intro_scene = cocos.scene.Scene(intro_layer)

   def run(self, host=None, port=None):
      """ """
      self.host = host
      self.port = port
      cocos.director.director.set_show_FPS(True)
      cocos.director.director.run (self.intro_scene)

   def on_join_game( self ):
      """ """
      gameInstance = GameServer.GameServer(self.getPlayLayer())
      cocos.director.director.replace(FadeTRTransition(gameInstance.get_scene(), 2))
      gameInstance.start()

   def on_host_game( self ):
      """ """
      playLayer = self.getPlayLayer()
      gameInstance = GameServer.GameServer(playLayer)
      cocos.director.director.replace(FadeTRTransition(gameInstance.get_scene(), 2))
      gameInstance.start()

   def on_name( self, value ):
      """ """
      self.player_name = value

   def on_quit( self ):
      """ """
      pyglet.app.exit()


class IntroMenu(cocos.menu.Menu):
   """
   """
   
   def __init__( self, game ):
      """ """
      super( IntroMenu, self ).__init__()
      self.game = game
      self.font_item = {
         'font_name': 'Arial',
         'font_size': 32,
         'bold': True,
         'color': (128, 100, 128, 100),
      }
      self.font_item_selected = {
         'font_name': 'Arial',
         'font_size': 42,
         'bold': True,
         'color': (64, 0, 64, 200),
      }

      l = []
      l.append( cocos.menu.MenuItem('Join Game',
         self.game.on_join_game ) )
      l.append( cocos.menu.MenuItem('Host Game',
         self.game.on_host_game ) )
      l.append( cocos.menu.EntryMenuItem('Name:',
         self.game.on_name,
         PlayLayer.PlayLayer.ownID) )
      l.append( cocos.menu.MenuItem('Quit', self.game.on_quit ) )

      self.create_menu( l )


if __name__ == "__main__":
   assert False
