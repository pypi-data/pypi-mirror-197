import curses
import math

from curses_toolkit.core import BlockingInput


def choose(choices, title=None):
    with BlockingInput():
        max_len = max([len(choice) for choice in choices])
        if title:
            max_len = max(max_len, len(title))
        win = curses.newwin(
                len(choices) + 2, max_len + 2,
                math.trunc((curses.LINES - (len(choices) + 2)) / 2),
                math.trunc((curses.COLS - (max_len + 2)) / 2))
        win.keypad(1)
        win.border()
        if title:
            win.addstr(0, 0, title)
        selected = 0
        choice = None
        while choice is None:
            for i, name in enumerate(choices):
                win.addstr(i + 1, 1, name,
                           curses.A_REVERSE if i == selected
                           else curses.A_NORMAL)
            win.refresh()
            match win.getkey():
                case '\n':
                    choice = choices[selected]
                case k if k in ('j', 'KEY_DOWN'):
                    selected = min(len(choices) - 1, selected + 1)
                case k if k in ('k', 'KEY_UP'):
                    selected = max(0, selected - 1)
                case k if k in ('x', '\x1b'):
                    break
        win.clear()
        win.refresh()
        return choice
