import random
import engine
import engine.gfx
import engine.map
import game.entities


# TODO loading screen
# TODO check can spawn area
# TODO extract fractal generation loop


class Game(engine.Game):
    """The demo game"""


    def init(self):

        self.define_entity_type('player', game.entities.PlayerEntityType())

        self.generate_map()
        # self.generate_npcs()

        self.spawn('player', (10, 10))


    def pre_update(self, key):

        # exit game if ESC key is pressed
        if ord(key) == 27:
            self.running = False


    def generate_map(self):
        """Randomly generate a map"""

        self.map = engine.map.Map(
            dimensions=(1000, 1000),
            perimeter_block=(' ', None, engine.gfx.GREEN),
            default_block=(' ', None, engine.gfx.GREEN)
        )

        # randomly generate a bunch of biomes on the map
        for i in range(0, 200):

            which = i % 2
            if which:
                # dessert
                self.generate_biome((' ', None, engine.gfx.YELLOW))
            else:
                # grass
                self.generate_biome((' ', None, engine.gfx.GREEN))

        # randomly generate some oceans on the map
        for i in range(0, 50):
            self.generate_ocean()

        # randomly generate a bunch of forests on the map
        for i in range(0, 200):
            self.generate_forest()


    def generate_biome(self, block):
        """Generate a biome of the given block type"""

        startx = random.randint(0, 1000)
        starty = random.randint(0, 1000)

        start_width = width = random.randint(100, 200)

        y = 0
        while width > 10:

            midx = int(startx - width/2)

            for x in range(0, width):

                self.map.set(
                    (midx + x, starty + y),
                    block
                )

                self.map.set(
                    (midx + x, starty - y),
                    block
                )

            width -= random.randint(-2, 5)
            y += 1


    def generate_ocean(self):

        startx = random.randint(0, 1000)
        starty = random.randint(0, 1000)

        start_width = width = random.randint(100, 200)

        y = 0
        while width > 10:
            midx = int(startx - width/2)

            for x in range(0, width):
                self.make_ocean((midx + x, starty + y))
                self.make_ocean((midx + x, starty - y))

            width -= random.randint(-2, 5)
            y += 1


    def make_ocean(self, pos):

        x, y = pos

        # set surrounding blocks to be beach
        self.make_beach((x-1, y))
        self.make_beach((x+1, y))
        self.make_beach((x, y-1))
        self.make_beach((x, y+1))

        # set the center block to be the ocean
        self.map.set(
            (x, y),
            ('🌊', None, engine.gfx.BLUE)
        )


    def make_beach(self, pos):

        char, _, _ = self.map.get(pos)
        if char == ' ':

            self.map.set(
                pos,
                (' ', None, engine.gfx.CYAN)
            )

    def generate_forest(self):
        """Generate a forests on the map"""

        startx = random.randint(0, 1000)
        starty = random.randint(0, 1000)

        start_width = width = random.randint(50, 100)

        y = 0
        while width > 10:

            for x in range(0, width):

                midx = int(startx - width/2)

                self.maybe_make_forest((midx + x, starty + y))
                self.maybe_make_forest((midx + x, starty - y))

            width -= random.randint(0, 2)
            y += 1


    def maybe_make_forest(self, pos):
        """Maybe make the given location on the map a forest block"""

        char, fg, bg = self.map.get(pos)

        block = None

        if bg == engine.gfx.YELLOW:

            block = ('🌵', None, engine.gfx.YELLOW)

        elif bg == engine.gfx.GREEN:

            if random.randint(0, 1):
                block = ('🌲', None, engine.gfx.GREEN)
            else:
                block = ('🌳', None, engine.gfx.GREEN)

        if random.randint(0, 3) == 0:
            if block is not None:
                self.map.set(pos, block)
