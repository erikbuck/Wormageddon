import PlayLayer
import cocos
import pyglet


class GameServer(object):
    """
    """
    def __init__(self, playLayer):
        """ """
        super( GameServer, self ).__init__()
        
        self.game_layer = playLayer        
        self.game_scene = cocos.scene.Scene(self.game_layer)

    def start(self):
        """ """
        # setup to handle asynchronous network messages
        #self.game_layer.do(ServerPlayLayerAction())
        self.game_layer.addPlayer(PlayLayer.PlayLayer.ownID)

    def get_scene(self):
        """ """
        return self.game_scene


if __name__ == "__main__":
    assert False
