import random
import engine
import engine.gfx
import engine.map
import game.entities


# TODO loading screen
# TODO check can spawn area
# TODO beach for oceans
# TODO forests dont span multiple biomes
# TODO basic NPCs, random movements


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
            perimeter_block=(' ', None, engine.gfx.GREEN),
            default_block=(' ', None, engine.gfx.GREEN)
        )

        for i in range(0, 100):

            which = i % 3
            if which == 0:
                self.generate_biome((' ', None, engine.gfx.YELLOW))
            elif which == 1:
                self.generate_biome((' ', None, engine.gfx.GREEN))
            else:
                self.generate_biome(('🌊', None, engine.gfx.BLUE))

        for i in range(0, 100):
            self.generate_forest()


    def generate_biome(self, grass_block):

        startx = random.randint(0, 1000)
        starty = random.randint(0, 1000)

        start_width = width = random.randint(100, 200)

        y = 0
        while width > 0:

            for x in range(0, width):

                midx = int(startx - width/2)

                self.map.set(
                    (midx + x, starty + y),
                    grass_block
                )

                self.map.set(
                    (midx + x, starty - y),
                    grass_block
                )

            width -= random.randint(-2, 5)
            y += 1


    def generate_forest(self):

        startx = random.randint(0, 1000)
        starty = random.randint(0, 1000)

        start_width = width = random.randint(50, 100)

        y = 0
        while width > 0:

            for x in range(0, width):

                midx = int(startx - width/2)

                self.make_forest((midx + x, starty + y))
                self.make_forest((midx + x, starty - y))

            width -= random.randint(0, 2)
            y += 1


    def make_forest(self, pos):

        char, fg, bg = self.map.get(pos)

        block = None

        if bg == engine.gfx.YELLOW:

            block = ('🌵', None, engine.gfx.YELLOW)

        elif bg == engine.gfx.GREEN:

            if random.randint(0, 1):
                block = ('🌲', None, engine.gfx.GREEN)
            else:
                block = ('🌳', None, engine.gfx.GREEN)

        if random.randint(0, 2) == 0:
            if block is not None:
                self.map.set(pos, block)
