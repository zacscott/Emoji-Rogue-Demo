import sys
import time
import engine.gfx
import engine.input


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
        self.fps = 10


    def init(self):
        """Initialise the game. Called automatically before the game is started, in run()."""
        pass


    def shutdown(self):
        """Shutdown the game. Called automatically when the game is ended, in run()"""
        pass


    def update(self, button):
        """
        Update the game a single step. Called automatically in the game loop.
        :param button: The button pressed which caused the game update.
        """
        pass


    def render(self):
        """Render the game screen. Called automatically in the game loop"""
        pass


    def run(self):
        """Start running the game. Will not return until the game has been quit / stopped."""

        try:

            engine.gfx.init()
            self.init()

            self.running = True
            while self.running:
                self._step()

        except Exception as ex:
            sys.stderr.write("%s\n" % str(ex))
            # TODO display trace

        engine.gfx.shutdown()
        self.shutdown()


    def _step(self):
        """Run a single step of the game loop"""

        start_time = time.time()

        # wait for input, then update and render game
        # rinse and repeat, this is the game loop
        char = engine.input.poll()
        self.update(char)
        self.render()

        # enforce maximum framerate limit
        elapsed_time = (time.time() - start_time) / 1000
        delay_time = (1/self.fps) - elapsed_time
        if delay_time > 0:
            time.sleep(delay_time)
