import time
import sys
import engine.gfx

# game state
running = True


def the_loop():

    global running

    engine.gfx.cls()
    engine.gfx.set(10, 10, '#')
    engine.gfx.flip()

    char = sys.stdin.read(1)
    running = char != 'q'
    # print(char)

    time.sleep(1/50)


def main():

    global running

    try:

        engine.gfx.init()

        while running:
            the_loop()

    except Exception as ex:
        sys.stderr.write("global exception caught; %s\n" % str(ex))
        # TODO display trace

    engine.gfx.shutdown()


# boot the game
main()
