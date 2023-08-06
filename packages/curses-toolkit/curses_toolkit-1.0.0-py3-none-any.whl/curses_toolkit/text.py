import curses
from .core import Window


class Text(Window):
    def __init__(self, row, col, height, width,
                 text='', attrs=curses.A_NORMAL):
        super().__init__(row, col, height, width)
        self.text = text
        self.attrs = attrs

    def show(self):
        self.win.clear()
        self.win.addstr(0, 0, self.text, self.attrs)
        self.win.refresh()

    def set_text(self, text):
        self.text = text
