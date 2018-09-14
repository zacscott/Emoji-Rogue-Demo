import engine.entity
import engine.gfx


class PlayerEntityType(engine.entity.EntityType):


    def __init__(self):

        self.char = '👨'
        self.fg = engine.gfx.WHITE
        # dont draw background colour
        self.bg = -1


    def update(self, entity, key):

        # handle player movement
        if key == 'w':
            entity.y -= 1
        elif key == 's':
            entity.y += 1
        elif key == 'a':
            entity.x -= 2
        elif key == 'd':
            entity.x += 2
