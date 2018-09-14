import engine.gfx


class Map:
    """Game map / field. A 2D map of the blocks that make up the game field"""


    def __init__(self, **kwargs):
        """

        :param dimensions: 2 tuple of the nmap dimensions. Default = (112, 32)
        :param perimeter_block: Block to insert around the perimeter of the map. Default =
            ('X', engine.gfx.BLACK, engine.gfx.WHITE)
        :param default_block: The default map block which the map is flood filled with to begin with. Default =
            (' ', engine.gfx.WHITE, engine.gfx.BLACK)
        """

        self.map = []
        self.camera = (0, 0)

        # parse kwargs

        self.dimensions = kwargs['dimensions'] if 'dimensions' in kwargs else (112, 32)

        if 'perimeter_block' in kwargs:
            self.perimeter_block = kwargs['perimeter_block']
        else:
            self.perimeter_block = ('X', engine.gfx.BLACK, engine.gfx.WHITE)

        if 'default_block' in kwargs:
            self.default_block = kwargs['default_block']
        else:
            self.default_block = (' ', engine.gfx.WHITE, engine.gfx.BLACK)

        # generate the basic map

        width, height = self.dimensions

        # fill map with the default block
        for y in range(0, height):
            row = []

            for x in range(0, width):
                row.append(self.default_block)
            self.map.append(row)

        # draw the perimeter fence blocks

        # top & bottom
        for x in range(0, width):
            self.set((x, 0), self.perimeter_block)
            self.set((x, height-1), self.perimeter_block)

        # left & right
        for y in range(0, height):
            self.set((0, y), self.perimeter_block)
            self.set((width-1, y), self.perimeter_block)


    def set(self, pos, block):
        """
        Set the block at the given position on the map
        :param pos: 2 tuple of the position on the map
        :param block: 3 tuple of the block to set (char, fg, bg)
        """

        x, y = pos

        if self.is_in_bounds(pos):
            self.map[y][x] = block


    def get(self, pos):
        """
        Get the block at the given position on the map
        :param pos: 2 tuple of the position on the map
        """

        x, y = pos
        block = self.default_block

        if self.is_in_bounds(pos):
            block = self.map[y][x]

        return block


    def is_empty(self, pos):
        """
        Returns whether the given spot on the map is empty and an entity can occupy it.
        :param pos: 2 tuple of the position on the map to check
        """

        char, _, _ = self.get(pos)
        is_empty = char == ' '

        return is_empty


    def is_in_bounds(self, pos):
        """
        Returns whether the given position is within the bounds of the map
        :param pos: 2 tuple of the position on the map to check
        """

        x, y = pos
        mapw, maph = self.dimensions

        in_bounds = x >= 0 and x < mapw
        in_bounds = in_bounds and y >= 0 and y < maph

        return in_bounds


    def render(self, offset):
        """Render the map to the screen"""

        map_width, map_height = self.dimensions
        term_width, term_height = engine.gfx.size()

        offset_x, offset_y = offset

        for x in range(offset_x, map_width):
            for y in range(offset_y, map_height):
                if x >= 0 and y >= 0:
                    block = self.map[y][x]
                    engine.gfx.plot((x-offset_x, y-offset_y), block)
