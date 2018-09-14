import random
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
            dimensions=(1000, 1000),
            perimeter_block=('🌳', None, engine.gfx.GREEN),
            default_block=(' ', None, engine.gfx.GREEN)
        )

        for i in range(0, 10):

            which = i % 3
            if which == 0:
                self.generate_biome(
                    (' ', None, engine.gfx.YELLOW),
                    ('🌵', None, engine.gfx.YELLOW)
                )

            elif which == 1:
                self.generate_biome(
                    (' ', None, engine.gfx.GREEN),
                    ('🌲', None, engine.gfx.GREEN)
                )

            else:
                self.generate_biome(
                    ('🌊', None, engine.gfx.BLUE),
                    ('🌊', None, engine.gfx.BLUE)
                )


    def generate_biome(self, grass_block, forest_block):

        startx = random.randint(0, 100)
        starty = random.randint(0, 100)

        start_height = height = random.randint(100, 200)
        start_width = width = random.randint(100, 200)

        for y in range(0, height):

            for x in range(0, width):

                midx = int(startx - width/2)
                midy = int(starty - start_height/2)

                self.map.set(
                    (midx + x, midy + y),
                    grass_block
                )

            width -= random.randint(0, int(width/height)+1)
