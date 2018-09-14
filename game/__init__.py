import engine
import engine.gfx
import game.entities


class Game(engine.Game):


    def init(self):

        self.define_entity_type('player', game.entities.PlayerEntityType())

        self.spawn('player', (10, 10))


    def pre_update(self, button):

        if button == 'q':
            self.running = False


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
