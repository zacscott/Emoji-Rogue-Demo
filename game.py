import engine
import engine.gfx


class Game(engine.Game):

    def init(self):

        self.y = 0
        self.x = 0

    def update(self, button):

        if button == 'q':
            self.running = False

        if button == 'w':
            self.y -= 1
        elif button == 's':
            self.y += 1
        elif button == 'a':
            self.x -= 2
        elif button == 'd':
            self.x += 2


    def render(self):

        engine.gfx.cls()

        engine.gfx.plot(9, 11, '#')
        engine.gfx.plot(9, 10, '#')
        engine.gfx.plot(9, 9, '#')
        engine.gfx.plot(10, 11, '#')
        engine.gfx.plot(10, 10, '#')
        engine.gfx.plot(10, 9, '#')
        engine.gfx.plot(11, 11, '#')
        engine.gfx.plot(11, 10, '#')
        engine.gfx.plot(11, 9, '#')

        engine.gfx.plot(self.x, self.y, '👨')

        engine.gfx.plot(16, 16, '💊')

        engine.gfx.plot(20, 20, '🍩')

        engine.gfx.plot(6, 6, '🗡')

        engine.gfx.flip()
