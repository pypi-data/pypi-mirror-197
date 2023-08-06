import pytest

from curses_toolkit import choose


@pytest.fixture
def mock_curses(mocker):
    mc = mocker.patch('curses_toolkit.chooser.curses')
    mc.COLS = 80
    mc.LINES = 60


@pytest.fixture
def newwin(mocker):
    win = mocker.MagicMock()
    win.getkey = mocker.MagicMock()
    return mocker.patch('curses_toolkit.chooser.curses.newwin',
                        return_value=win)


@pytest.fixture
def blocking_input(mocker):
    return mocker.patch('curses_toolkit.chooser.BlockingInput')


def test_chooser(mock_curses, newwin, blocking_input):
    newwin.return_value.getkey.return_value = '\n'
    assert 'One' == choose(['One', 'Two', 'Three'])
    newwin.assert_called_once_with(5, 7, 27, 36)
    newwin.return_value.getkey.assert_called_once()


def test_chooser_down_one(mock_curses, newwin, blocking_input):
    newwin.return_value.getkey.side_effect = ['j', '\n']
    assert 'Two' == choose(['One', 'Two', 'Three'])


def test_chooser_down_two(mock_curses, newwin, blocking_input):
    newwin.return_value.getkey.side_effect = ['j', 'j', '\n']
    assert 'Three' == choose(['One', 'Two', 'Three'])


def test_chooser_down_four(mock_curses, newwin, blocking_input):
    newwin.return_value.getkey.side_effect = ['j', 'j', 'j', 'j', '\n']
    assert 'Three' == choose(['One', 'Two', 'Three'])


def test_chooser_down_four_up_one(mock_curses, newwin, blocking_input):
    newwin.return_value.getkey.side_effect = ['j', 'j', 'j', 'j', 'k', '\n']
    assert 'Two' == choose(['One', 'Two', 'Three'])


def test_chooser_up_one(mock_curses, newwin, blocking_input):
    newwin.return_value.getkey.side_effect = ['k', '\n']
    assert 'One' == choose(['One', 'Two', 'Three'])


def test_chooser_down_four_up_one_cursor_keys(
        mock_curses, newwin, blocking_input):
    newwin.return_value.getkey.side_effect = [
            'KEY_DOWN',
            'KEY_DOWN',
            'KEY_DOWN',
            'KEY_DOWN',
            'KEY_UP',
            '\n',
            ]
    assert 'Two' == choose(['One', 'Two', 'Three'])


def test_chooser_none(mock_curses, newwin, blocking_input):
    newwin.return_value.getkey.side_effect = ['x']
    assert choose(['One', 'Two', 'Three']) is None


def test_chooser_none_escape(mock_curses, newwin, blocking_input):
    newwin.return_value.getkey.side_effect = ['\x1b']
    assert choose(['One', 'Two', 'Three']) is None
