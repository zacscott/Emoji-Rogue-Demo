import engine
import engine.gfx
import engine.map
import game.entities


class Game(engine.Game):


    def init(self):

        self.define_entity_type('player', game.entities.PlayerEntityType())

        self.spawn('player', (10, 10))

        self.generate_map()
        # self.generate_npcs()


    def pre_update(self, key):

        # exit game if ESC key is pressed
        if ord(key) == 27:
            self.running = False


    def generate_map(self):

        self.map = engine.map.Map(
            perimeter_block=('🌳', None, engine.gfx.GREEN),
            default_block=(' ', None, engine.gfx.GREEN)
        )

        for y in range(1, 10):

            for x in range(1, 10):

                self.map.set(
                    (x, y),
                    ('🌲', None, engine.gfx.GREEN)
                )

        for y in range(10, 20):

            for x in range(10, 20):

                self.map.set(
                    (x, y),
                    ('🌊', None, engine.gfx.BLUE)
                )
