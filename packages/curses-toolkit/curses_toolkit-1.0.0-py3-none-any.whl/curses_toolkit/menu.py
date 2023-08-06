import curses

from .core import Window, BlockingInput


class Menu(Window):
    def __init__(self, row, col, height, width, items):
        super().__init__(row, col, height, width)
        self.items = items
        self.win = curses.newwin(height, width, row, col)
        self.win.keypad(1)

    def show(self):
        self.win.clear()
        col = 0
        for i in self.items:
            self.win.addstr(0, col, f'{i} ')
            col += len(i) + 1
        self.win.refresh()

    def get_selection(self):
        with BlockingInput():
            selected = None
            focus = 0
            while selected is None:
                self.win.clear()
                col = 0
                for i, item in enumerate(self.items):
                    if i == focus:
                        self.win.addstr(0, col, f'{item} ', curses.A_REVERSE)
                    else:
                        self.win.addstr(0, col, f'{item} ')
                    col += len(item) + 1
                self.win.refresh()
                match self.win.getkey():
                    case '\n':
                        selected = focus
                    case k if k in ('h', 'KEY_LEFT'):
                        focus = max(0, focus - 1)
                    case k if k in ('l', 'KEY_RIGHT'):
                        focus = min(len(self.items) - 1, focus + 1)
            return self.items[selected]
