import sys


def poll():
    """Polls stdin and returns which key is being pressed"""

    sys.stdin.seek(0, 2)
    char = sys.stdin.read(1)

    return char
