import os
import sys
import tty
import termios

# TODO optimise rendering, so can be played efficiently over ssh
#  - clear row with escape code
#  - only draw chars needed on line

# ASCII escape colours
_ESCAPE_BLACK = '\u001b[30m'
_ESCAPE_DARK_GREY = '\u001b[30;1m'
_ESCAPE_DARK_RED = '\u001b[31m'
_ESCAPE_RED = '\u001b[31;1m'
_ESCAPE_DARK_GREEN = '\u001b[32m'
_ESCAPE_GREEN = '\u001b[32;1m'
_ESCAPE_DARK_YELLOW = '\u001b[33m'
_ESCAPE_YELLOW = '\u001b[33;1m'
_ESCAPE_DARK_BLUE = '\u001b[34m'
_ESCAPE_BLUE = '\u001b[34;1m'
_ESCAPE_DARK_MAGENTA = '\u001b[35m'
_ESCAPE_MAGENTA = '\u001b[35;1m'
_ESCAPE_DARK_CYAN = '\u001b[36m'
_ESCAPE_CYAN = '\u001b[36;1m'
_ESCAPE_GREY = '\u001b[37m'
_ESCAPE_WHITE = '\u001b[37;1m'


# off screen double buffer
_screenbuf = []




def _tty_size():
    """Returns the size of the terminal (width, height)"""
    rows, columns = os.popen('stty size', 'r').read().split()
    return (int(columns), int(rows))


_tty_saved_state = None
def _tty_save_state():
    """Save the TTY state so it can be restored later"""

    global _tty_saved_state
    _tty_saved_state = termios.tcgetattr(sys.stdin)


def _tty_restore_state():
    """Restore the previous TTY saved state"""

    global _tty_saved_state
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _tty_saved_state)


def _reset():
    """Send reset escape code to terminal"""
    sys.stdout.write("\u001b[0m")


def _cursor_hide():
    """Hide the cursor from the terminal"""
    sys.stdout.write("\033[?25l")


def _cursor_show():
    """Show the cursor from the terminal"""
    sys.stdout.write("\033[?25h")


def _cursor_left(n=1):
    """Move the cursor n chars left"""
    sys.stdout.write("\u001b[%dD" % n)


def _cursor_up(n=1):
    """Move the cursor n lines up"""
    sys.stdout.write("\u001b[%dA" % n)


def _clr_line():
    """Clear the current line"""
    sys.stdout.write("\u001b[OK")


def init():

    global _screenbuf

    _tty_save_state()

    # enable raw input from terminal, not buffered to newlines
    tty.setcbreak(sys.stdin, 0)

    _cursor_hide()

    # clear the terminal ready for rendering
    cls()
    for i in range(0, len(_screenbuf)):
        sys.stdout.write("\n")


def shutdown():
    """Shutdown the graphics system and restore the terminal"""

    # reposition cursor to bottom left
    _cursor_up(1)
    if len(_screenbuf):
        _cursor_left(len(_screenbuf[0]))
    sys.stdout.write("\n")

    _tty_restore_state()

    _cursor_show()

    sys.stdout.flush()


def set(x, y, char):
    """Set the character at the given position on screen"""

    global _screenbuf

    _screenbuf[y][x] = char


def get(x, y):
    """Get the character at the given position on screen"""

    global _screenbuf

    value = ' '

    if len(_screenbuf) >= y:
        row = _screenbuf[y]
        if len(row) >= x:
            value = row[x]

    return value


def cls():
    """Clear the screen"""

    global _screenbuf

    _screenbuf = []

    (width, height) = _tty_size()
    for y in range(0, height):

        row = []
        for x in range(0, width):
            row.append(' ')

        _screenbuf.append(row)


def flip():
    """Flip the double buffer and render to screen"""

    global _screenbuf

    # move cursor all the way back to the first line
    _cursor_up(len(_screenbuf))
    if len(_screenbuf):
        _cursor_left(len(_screenbuf[0]))

    # render each row in the screenbuf
    count = 1
    for row in _screenbuf:
        count += 1

        # render each cell in the row
        for char in row:
            if char == ' ':
                string = "%s%s" % ("\u001b[40;1m", ' ')
                sys.stdout.write(string)
            else:
                string = "%s%s%s" % ("\u001b[42m", _ESCAPE_DARK_RED, char)
                sys.stdout.write(string)

        # add newlines for all but the last row
        if count < len(_screenbuf):
            sys.stdout.write("\n")

    # flush the output buffer so the terminal actually renders the screen
    _reset()
    sys.stdout.flush()
