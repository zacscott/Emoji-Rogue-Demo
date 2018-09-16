import math
import os
import sys
import tty
import termios


# colour enum, will be automatically mapped to FG / BG colors
BLACK = 0
WHITE = 1
RED = 2
GREEN = 3
YELLOW = 4
BLUE = 5
CYAN = 6
MAGENTA = 7

# terminal escape colour codes
_FG_BLACK = '\u001b[30m'
_BG_BLACK = '\u001b[40m'
_FG_RED = '\u001b[31m'
_BG_RED = '\u001b[41m'
_FG_GREEN = '\u001b[32m'
_BG_GREEN = '\u001b[42m'
_FG_YELLOW = '\u001b[33m'
_BG_YELLOW = '\u001b[43m'
_FG_BLUE = '\u001b[34m'
_BG_BLUE = '\u001b[44m'
_FG_MAGENTA = '\u001b[35m'
_BG_MAGENTA = '\u001b[45m'
_FG_CYAN = '\u001b[36m'
_BG_CYAN = '\u001b[46m'
_FG_WHITE = '\u001b[37m'
_BG_WHITE = '\u001b[47m'


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
    sys.stdout.write("\u001b[?25l")


def _cursor_show():
    """Show the cursor from the terminal"""
    sys.stdout.write("\u001b[?25h")


def _cursor_left(n=1):
    """Move the cursor n chars left"""
    sys.stdout.write("\u001b[%dD" % n)


def _cursor_up(n=1):
    """Move the cursor n lines up"""
    sys.stdout.write("\u001b[%dA" % n)


def _clr_line():
    """Clear the current line"""
    sys.stdout.write("\u001b[OK")


def _bg_code(colour):
    """Returns the escape code for the given background colour"""

    if colour == WHITE:
        code = _BG_WHITE
    elif colour == RED:
        code = _BG_RED
    elif colour == GREEN:
        code = _BG_GREEN
    elif colour == YELLOW:
        code = _BG_YELLOW
    elif colour == BLUE:
        code = _BG_BLUE
    elif colour == CYAN:
        code = _BG_CYAN
    elif colour == MAGENTA:
        code = _BG_MAGENTA
    else:
        code = _BG_BLACK

    return code


def _fg_code(colour):
    """Returns the escape code for the given foreground colour"""

    if colour == WHITE:
        code = _FG_WHITE
    elif colour == RED:
        code = _FG_RED
    elif colour == GREEN:
        code = _FG_GREEN
    elif colour == YELLOW:
        code = _FG_YELLOW
    elif colour == BLUE:
        code = _FG_BLUE
    elif colour == CYAN:
        code = _FG_CYAN
    elif colour == MAGENTA:
        code = _FG_MAGENTA
    else:
        code = _FG_BLACK

    return code


def init():

    global _screenbuf

    _tty_save_state()

    # enable raw input from terminal, not buffered to newlines
    tty.setcbreak(sys.stdin, 0)

    _cursor_hide()

    # initialise the screen buffer

    _screenbuf = []

    (width, height) = _tty_size()
    for y in range(0, height):

        row = []
        for x in range(0, int(math.floor(width/2)-1)):
            row.append((' ', WHITE, BLACK))
        _screenbuf.append(row)

        sys.stdout.write("\n")

    flip()


def shutdown():
    """Shutdown the graphics system and restore the terminal"""

    # reposition cursor to bottom left
    _cursor_up(1)
    if len(_screenbuf):
        _cursor_left(len(_screenbuf[0]))
    sys.stdout.write("\n")

    _tty_restore_state()

    _cursor_show()

    sys.stdout.write("\n")
    sys.stdout.flush()


def size():
    """Returns the terminal size"""

    global _screenbuf

    height, width = (0, 0)

    if _screenbuf:
        height = len(_screenbuf)
        width = int(len(_screenbuf[0]))
            # NOTE we return half width since we double up chars on x axis

    return (width, height)


def plot(pos, block):
    """Set the character at the given position on screen"""

    global _screenbuf

    x, y = pos
    char, fg, bg = block

    if y >= 0 and y < len(_screenbuf):
        row = _screenbuf[y]

        if x >= 0 and x < len(row):

            _, current_fg, current_bg = _screenbuf[y][x]
            if fg is None or fg < 0:
                fg = current_fg
            if bg is None or bg < 0:
                bg = current_bg
            _screenbuf[y][x] = (char, fg, bg)


def get(pos):
    """Get the character at the given position on screen"""

    global _screenbuf

    x, y = pos
    block = (' ', WHITE, BLACK)

    if y >= 0 and y < len(_screenbuf):
        row = _screenbuf[y]

        if x >= 0 and x < len(row):
            block = row[x]

    return block


def cls(block=(' ', None, BLACK)):
    """Clear the screen"""

    global _screenbuf

    for y in range(0, len(_screenbuf)):
        row = _screenbuf[y]

        for x in range(0, len(row)):
            _screenbuf[y][x] = block


def flip():
    """Flip the double buffer and render to screen"""

    global _screenbuf

    # move cursor all the way back to the first line
    width, height = size()
    _cursor_left(width*2)
    _cursor_up(height)

    # render each row in the screenbuf
    for y in range(0, height):
        row = _screenbuf[y]

        # render each cell in the row
        row_string = ""
        for x in range(0, width):
            char, fg, bg = row[x]

            # TODO optimise this rendering
            #      1. output newline instead of spaces at end of line
            #      2. only set bg/fg colours if they have changed, not every time

            if char == ' ':
                # spaces are simple, just a BG colour + "  "
                row_string += "%s  " % _bg_code(bg)
            elif ord(char) > 127:
                # assuming emoji are double width chars
                row_string += "%s%s%s" % (_bg_code(bg), _fg_code(fg), char)
            else:
                # double up on normal ASCII chars
                row_string += "%s%s%s%s" % (_bg_code(bg), _fg_code(fg), char, char)

        # output the line to term
        sys.stdout.write(row_string)
        if y < height-1:  # add newlines for all but the last row
            sys.stdout.write("\n")

    # flush the output buffer so the terminal actually renders the screen
    _reset()
    sys.stdout.flush()
