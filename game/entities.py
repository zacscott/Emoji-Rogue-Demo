import engine.entity
import engine.gfx


class PlayerEntityType(engine.entity.EntityType):


    def __init__(self):

        self.block = ('👨', None, None)


    def update(self, entity, key):

        new_x, new_y = entity.x, entity.y

        # handle WASD player movement
        if key == 'w':
            new_y -= 1
        elif key == 's':
            new_y += 1
        elif key == 'a':
            new_x -= 1
        elif key == 'd':
            new_x += 1

        # move the player to the new location if there is nothing on the map blocking them
        themap = self.game.map
        if themap.is_in_bounds((new_x, new_y)) and themap.is_empty((new_x, new_y)):
            entity.x = new_x
            entity.y = new_y

        self.camera_track(entity)


    def camera_track(self, entity):
        """Have the camera follow/track the given entity"""

        term_width, term_height = engine.gfx.size()
        map_width, map_height = self.game.map.dimensions

        camx = int(entity.x - term_width/2)
        camx = max(camx, 0)
        camx = min(camx, map_width-term_width)

        camy = int(entity.y - term_height/2)
        camy = max(camy, 0)
        camy = min(camy, map_height-term_height)

        self.game.camera = (camx, camy)
