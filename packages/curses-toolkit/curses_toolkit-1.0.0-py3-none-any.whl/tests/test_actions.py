from curses_toolkit import actions
from curses_toolkit.actions import keys_vim_select, keys_vim_up_down


def test_list_exit_actions(mocker, list_pad, core_curses, list_days):
    list_pad.getkey.return_value = 'd'
    action_sink = mocker.MagicMock()

    def key_handler(ct_list, ctx, key):
        match key:
            case 'd':
                action_sink.action_d(ct_list.focus, ct_list)
                return True

    actions(list_days, {}, [key_handler])
    action_sink.action_d.assert_called_once_with(None, list_days)


def test_list_loop_actions(mocker, list_pad, core_curses, list_days):
    list_pad.getkey.side_effect = ['k', 'k', 'd', 'j']
    action_sink = mocker.MagicMock()

    def key_handler(ct_list, ctx, key):
        match key:
            case 'd':
                action_sink.action_d(ct_list.focus, ct_list)
                return True
            case 'j':
                action_sink.action_j(ct_list.focus, ct_list)
                return False
            case 'k':
                action_sink.action_k(ct_list.focus, ct_list)
                return False

    actions(list_days, {}, [key_handler], initial_focus=0)
    action_sink.action_j.assert_not_called()
    assert 2 == len(action_sink.action_k.mock_calls)
    action_sink.action_d.assert_called_once_with(0, list_days)


def test_vim_keys_select(core_curses, list_pad, list_days):
    list_pad.getkey.side_effect = ('j', 'j', 'k', '\n')
    context = {}
    actions(list_days,
            context,
            [keys_vim_select, keys_vim_up_down],
            initial_focus=0)
    assert 1 == context['selection']


def test_vim_keys_cancel(core_curses, list_pad, list_days):
    list_pad.getkey.side_effect = ('j', 'j', 'k', '\x1b')
    context = {}
    actions(list_days,
            context,
            [keys_vim_select, keys_vim_up_down],
            initial_focus=0)
    assert 'selected' not in context
