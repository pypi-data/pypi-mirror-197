from curses_toolkit import BlockingInput, NonblockingInput


def test_BlockingInput(core_curses):
    with BlockingInput():
        core_curses.cbreak.assert_called_once_with()
    core_curses.nocbreak.assert_called_once_with()


def test_NonblockingInput(core_curses):
    with NonblockingInput(5):
        core_curses.halfdelay.assert_called_once_with(5)
    core_curses.nocbreak.assert_called_once_with()
