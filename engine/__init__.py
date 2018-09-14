import sys
import time
import engine.entity
import engine.gfx
import engine.input
import engine.map


class Game:
    """
    Base game class which should be extended. Manages the game loop, input, updating, timing and rendering
    Child game classes can implement the following:

     - init()
     - shutdown()
     - pre_update(button)
     - post_update(button)
     - pre_render()
     - post_render()

    The game instance should be started by running game.run()
    """


    def __init__(self):

        self.running = False
        self.fps = 10

        self.camera = (0, 0)

        self.map = engine.map.Map()

        self.entity_types = {}
        self.entities = []


    def init(self):
        """Initialise the game. Called automatically before the game is started, in run()."""
        pass


    def shutdown(self):
        """Shutdown the game. Called automatically when the game is ended, in run()"""
        pass


    def pre_update(self, key):
        """
        Called before the entities in the game are updated in a game loop tick.
        :param key: The key pressed which caused the game update.
        """
        pass


    def post_update(self, key):
        """
        Called after the entities in the game have been updated in a game loop tick.
        :param key: The key pressed which caused the game update.
        """
        pass


    def pre_render(self):
        """Called before the entities in the game are rendered in the game loop"""
        pass


    def post_render(self):
        """
        Called after the entities in the game have been rendered in the game loop. Is called before
        engine.gfx.flip() is called though, so it is possible to still draw things.
        """
        pass


    def define_entity_type(self, name, entity_type):
        """
        Define an entity type which can be used with Game.spawn()
        :param name: The name of the entity type, to be used later with spawn()
        :param entity_type: The EntityType instance
        """

        entity_type.game = self
        self.entity_types[name] = entity_type


    def spawn(self, name, pos):
        """
        Spawn a new entity at the given location
        :param name: The name of the entity type, previously defined with define_entity_type()
        :param pos: 2 tuple of the entities location on the map
        """

        if name in self.entity_types:

            entity_type = self.entity_types[name]

            self.entities.append(
                entity_type.spawn(pos)
            )


    def run(self):
        """Start running the game. Will not return until the game has been quit / stopped."""

        # try:

        engine.gfx.init()
        self.init()

        self.running = True
        while self.running:
            self._step()

        # except Exception as ex:
        #     sys.stderr.write("%s\n" % str(ex))
            # TODO display trace

        engine.gfx.shutdown()
        self.shutdown()


    def _step(self):
        """Run a single step of the game loop"""

        start_time = time.time()

        # wait for input, then update, then render
        # rinse and repeat, this is the game loop
        key = engine.input.poll()
        self._update(key)
        self._render()

        # enforce maximum framerate limit
        elapsed_time = (time.time() - start_time) / 1000
        delay_time = (1/self.fps) - elapsed_time
        if delay_time > 0:
            time.sleep(delay_time)


    def _update(self, key):
        """Handle updating the game when a key is pressed"""

        self.pre_update(key)

        # update all of the game entities
        for entity in self.entities:
            entity.update(key)

        self.post_update(key)


    def _render(self):
        """Handle rendering when the game has been updated"""

        self.pre_render()

        # draw out of bounds XXX, just in case something fucks up we can see where the map ends
        engine.gfx.cls(('#', engine.gfx.BLACK, engine.gfx.RED))

        # step 1 render the map
        self.map.render(self.camera)

        # step2; render all of the game entities
        for entity in self.entities:
            entity.render(self.camera)

        self.post_render()

        # flip the double buf and render to screen
        engine.gfx.flip()
