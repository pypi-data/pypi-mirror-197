# TODO: context dict as input and return value?
def actions(parent, ctx, key_handlers, initial_focus=None):
    if initial_focus is None:
        parent.set_no_focus()
    else:
        parent.set_focus(initial_focus)
    completed = None
    while not completed:
        parent.show()
        k = parent.pad.getkey()
        for key_handler in key_handlers:
            completed = key_handler(parent, ctx, k)
            if completed is not None:
                break
    parent.focus = None
    parent.show()
    return ctx


def keys_vim_select(ct_list, ctx, key):
    match key:
        case '\x1b':
            return True
        case 'x':
            return True
        case '\n':
            ctx['selection'] = ct_list.focus
            return True


def keys_vim_up_down(ct_list, ctx, key):
    match key:
        case 'k':
            ct_list.set_focus(ct_list.focus - 1)
            return False
        case 'j':
            ct_list.set_focus(ct_list.focus + 1)
            return False
