import sys
import time
import engine.gfx


class Game:
    """
    Base game class which should be extended. Manages the game loop, input, updating, timing and rendering
    Child game classes should implement the following:

     - update(button)
     - render()

    Optional methods to override:

     - init()
     - shutdown()

    The game instance should be started by running game.run()
    """


    def __init__(self):

        self.running = False


    def init(self):
        pass


    def shutdown(self):
        pass


    def update(self, button):
        pass


    def render(self, button):
        pass


    def _loop(self):

        char = sys.stdin.read(1)
        # char = s[len(s)-1]
        self.running = char != 'q'

        self.update(char)
        self.render()

        time.sleep(1/50)


    def run(self):
        """

        """

        self.running = True

        try:

            engine.gfx.init()
            self.init()

            while self.running:
                self._loop()

        except Exception as ex:
            sys.stderr.write(str(ex))
            # TODO display trace

        engine.gfx.shutdown()
        self.shutdown()

