from curses_toolkit.core import BlockingInput
from curses_toolkit.actions import actions, keys_vim_select, keys_vim_up_down


def selector(parent):
    context = {}
    with BlockingInput():
        actions(parent,
                context,
                [keys_vim_select, keys_vim_up_down],
                initial_focus=0)
    parent.set_no_focus()
    parent.show()
    return context['selection']
