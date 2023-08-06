import curses


class BlockingInput:
    def __enter__(self):
        curses.cbreak()

    def __exit__(self, *args):
        curses.nocbreak()


class NonblockingInput:
    def __init__(self, tenths_sec):
        self.tenths_sec = tenths_sec

    def __enter__(self):
        curses.halfdelay(self.tenths_sec)

    def __exit__(self, *args):
        curses.nocbreak()


class Echo:
    def __enter__(self):
        curses.echo()

    def __exit__(self, *args):
        curses.noecho()


class Cursor:
    def __init__(self, visibility=2):
        self.visibility = visibility

    def __enter__(self):
        curses.curs_set(self.visibility)

    def __exit__(self, *args):
        curses.curs_set(0)


class Window:
    def __init__(self, row, col, height, width):
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.win = curses.newwin(height, width, row, col)
