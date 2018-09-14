import sys


def poll():
    """Polls stdin and returns which key is being pressed"""

    sys.stdin.seek(0, 2)  # skip any input already in the buffer
    char = sys.stdin.read(1)  # and read the next key pressed
    char = char.lower()

    return char
