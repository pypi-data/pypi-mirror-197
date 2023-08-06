import pytest
from curses_toolkit import List


@pytest.fixture
def list_curses(mocker):
    return mocker.patch('curses_toolkit.list.curses')


@pytest.fixture
def core_curses(mocker):
    return mocker.patch('curses_toolkit.core.curses')


@pytest.fixture
def list_pad(mocker, list_curses):
    lp = mocker.MagicMock()
    list_curses.newpad.return_value = lp
    return lp


@pytest.fixture
def list_days(list_pad):
    return List(3, 5,
                10, 6,
                ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
