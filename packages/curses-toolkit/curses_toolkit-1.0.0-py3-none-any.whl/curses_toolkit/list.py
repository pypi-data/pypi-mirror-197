import curses


class List:
    def __init__(self, row, col, height, width, rows=None):
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.rows = rows if rows else []
        max_width = max((len(row) for row in self.rows)) if rows else 0
        self.pad = curses.newpad(len(self.rows) + 1,
                                 max_width + 1)
        self.focus = None
        self.first_visible_row = 0
        self.show_listeners = []

    def add_show_listener(self, listener):
        self.show_listeners.append(listener)

    def show(self, ensure_visible=None):
        visible = (self.focus
                   if ensure_visible is None
                   else min(len(self.rows), ensure_visible))
        self.pad.clear()
        for i, row in enumerate(self.rows):
            self.pad.addstr(
                    i, 0, row,
                    curses.A_REVERSE if self.focus == i else curses.A_NORMAL)
        if visible is not None:
            self.first_visible_row = max(0,
                                         min(visible - int(self.height / 2),
                                             len(self.rows) - self.height))
        self.pad.refresh(self.first_visible_row, 0,
                         self.row, self.col,
                         self.row + self.height - 1, self.col + self.width - 1)
        for listener in self.show_listeners:
            listener.show()

    def set_focus(self, focus):
        self.focus = min(max(0, focus), len(self.rows) - 1)
        return self.focus

    def set_no_focus(self):
        self.focus = None

    def add_row(self, row):
        self.rows.append(row)
        height, width = self.pad.getmaxyx()
        if len(self.rows) > height or len(row) > width:
            del self.pad
            self.pad = curses.newpad(max(height, len(self.rows) + 1),
                                     max(width, len(row) + 1))

    def clear(self):
        self.rows = []


class ColumnList(List):
    def __init__(self, row, col, height, width, column_count, rows=None):
        super().__init__(row, col, height, width, rows=None)
        self.column_count = column_count
        self.raw_rows = []
        self.widths = []
        if rows:
            for row in rows:
                self.add_row(row)

    def add_row(self, row):
        self.raw_rows.append(row)
        self.widths = [0] * len(self.raw_rows[0])
        for r in self.raw_rows:
            self.widths = [max(ls) for ls in zip(self.widths,
                                                 [len(c) for c in r])]
        self.rows = []
        for raw_row in self.raw_rows:
            super().add_row('  '.join([col + ' ' * (width - len(col))
                                       for width, col
                                       in zip(self.widths, raw_row)]))

    def clear(self):
        self.raw_rows = []
        self.widths = []
        super().clear()


#############
# listeners #
#############

class Scrollbar:
    def __init__(self, parent):
        self.parent = parent
        self.parent.add_show_listener(self)
        self.win = curses.newwin(self.parent.height, 2,
                                 self.parent.row,
                                 self.parent.col + self.parent.width)

    def show(self):
        self.win.clear()
        if self.parent.first_visible_row > 0:
            self.win.addstr(0, 0, '▲')
        if (len(self.parent.rows) - self.parent.first_visible_row
                > self.parent.height):
            self.win.addstr(self.parent.height - 1, 0, '▼')
        # TODO: bounds check the row calculation
        if len(self.parent.rows) - (self.parent.height - 1) > 0:
            bar_row = min(self.parent.height - 1,
                          max(0,
                              int(self.parent.first_visible_row
                                  / (len(self.parent.rows)
                                     - (self.parent.height - 1))
                                  * (self.parent.height - 2)) + 1))
        else:
            bar_row = 0
        self.win.addstr(bar_row, 0, '◼︎')
        self.win.refresh()


class Header:
    def __init__(self, parent, headers, attrs=curses.A_NORMAL):
        self.parent = parent
        self.headers = headers
        self.attrs = attrs
        self.parent.add_show_listener(self)
        self.win = curses.newwin(1, parent.width,
                                 parent.row - 1, parent.col)

    def show(self):
        self.win.clear()
        c = 0
        for header, offset, width in zip(self.headers,
                                         [0] + self.parent.widths,
                                         self.parent.widths):
            c += offset
            self.win.addstr(0, c, header, self.attrs)
            c += 2
        self.win.refresh()
