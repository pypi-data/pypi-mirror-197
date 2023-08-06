from curses_toolkit import List, selector


def test_list_select_first(list_pad, core_curses):
    list_pad.getkey.return_value = '\n'
    a_list = List(3, 5,
                  10, 6,
                  [
                      'Monday',
                      'Tuesday',
                      'Wednesday',
                      'Thursday',
                      'Friday',
                      ])
    assert 0 == selector(a_list)
    list_pad.getkey.assert_called_once()


def test_list_select_down_two(list_pad, core_curses):
    list_pad.getkey.side_effect = ['j', 'j', '\n']
    a_list = List(3, 5,
                  10, 6,
                  [
                      'Monday',
                      'Tuesday',
                      'Wednesday',
                      'Thursday',
                      'Friday',
                      ])
    assert 2 == selector(a_list)


def test_list_select_ten_down_one_up(list_pad, core_curses):
    list_pad.getkey.side_effect = ['j'] * 10 + ['k', '\n']
    a_list = List(3, 5,
                  10, 6,
                  [
                      'Monday',
                      'Tuesday',
                      'Wednesday',
                      'Thursday',
                      'Friday',
                      ])
    assert 3 == selector(a_list)


def test_list_select_ten_up_one_down(list_pad, core_curses):
    list_pad.getkey.side_effect = ['k'] * 10 + ['j', '\n']
    a_list = List(3, 5,
                  10, 6,
                  [
                      'Monday',
                      'Tuesday',
                      'Wednesday',
                      'Thursday',
                      'Friday',
                      ])
    assert 1 == selector(a_list)
