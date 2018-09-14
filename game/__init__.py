import engine
import engine.gfx
import game.entities


class Game(engine.Game):


    def init(self):

        self.define_entity_type('player', game.entities.PlayerEntityType())

        # self.spawn('player', (10, 10))
        self.spawn('player', (10, 10))


    def pre_update(self, key):

        if key == 'q':
            self.running = False


    def post_update(self, key):

        term_width, term_height = engine.gfx.size()
        map_width, map_height = self.map.dimensions

        # player_ent = self.find('player')
        player_ent = self.entities[0]

        camx = int(player_ent.x - term_width/2)
        camx = max(camx, 0)
        camx = min(camx, map_width-term_width)

        camy = int(player_ent.y - term_height/2)
        camy = max(camy, 0)
        camy = min(camy, map_height-term_height)

        self.camera = (camx, camy)


    # def render(self):

    #     engine.gfx.cls()

    #     engine.gfx.plot(9, 11, '#')
    #     engine.gfx.plot(9, 10, '#')
    #     engine.gfx.plot(9, 9, '#')
    #     engine.gfx.plot(10, 11, '#')
    #     engine.gfx.plot(10, 10, '#')
    #     engine.gfx.plot(10, 9, '#')
    #     engine.gfx.plot(11, 11, '#')
    #     engine.gfx.plot(11, 10, '#')
    #     engine.gfx.plot(11, 9, '#')

    #     engine.gfx.plot(self.x, self.y, '👨')

    #     engine.gfx.plot(16, 16, '💊')

    #     engine.gfx.plot(20, 20, '🍩')

    #     engine.gfx.plot(6, 6, '🗡')

    #     engine.gfx.flip()
