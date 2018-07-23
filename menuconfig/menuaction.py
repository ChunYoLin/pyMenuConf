import abc
import curses
from menuconfig import Window


class InputAction(metaclass=abc.ABCMeta):
    @property
    @abc.abstractclassmethod
    def usage(self):
        pass

    @property
    @abc.abstractclassmethod
    def key(self):
        pass

    @abc.abstractclassmethod
    def action(self, window, item):
        pass

class ExitAction(InputAction):
    @property
    def usage(self):
        return "[q/ESC] Exit"

    @property
    def key(self):
        return (ord('q'), 27)

    def action(self, window, item):
        return Window.EXIT

class ToggleAction(InputAction):
    @property
    def usage(self):
        return "[Enter] Toggle/Enter"

    @property
    def key(self):
        return (ord('\n'), )

    def action(self, window, item):
        return item.toggle()

class EnterAction(InputAction):
    @property
    def usage(self):
        return "[->/l] Enter"

    @property
    def key(self):
        return (ord('\n'), curses.KEY_RIGHT, ord('l'))

    def action(self, window, item):
        return Window.ENTER

class BackAction(InputAction):
    @property
    def usage(self):
        return "[<-/h] Back"

    @property
    def key(self):
        return (ord('q'), curses.KEY_LEFT, ord('h'))

    def action(self, window, item):
        return Window.BACK

class ConfigAction(InputAction):
    @property
    def usage(self):
        return "[c] Configure"

    @property
    def key(self):
        return (ord('c'), )

    def action(self, window, item):
        for item in window.items:
            item.config = True

class UpAction(InputAction):
    @property
    def usage(self):
        return "[↑/j] Up"

    @property
    def key(self):
        return (curses.KEY_UP, ord('k'),)

    def action(self, window, item):
        if window.cur_cursor > 0:
            window.cur_cursor -= 1
        else:
            window.cur_cursor = 0

class DownAction(InputAction):
    @property
    def usage(self):
        return "[↓/k] Down"

    @property
    def key(self):
        return (curses.KEY_DOWN, ord('j'),)

    def action(self, window, item):
        if window.cur_cursor < len(window.items)-1:
            window.cur_cursor += 1
        else:
            window.cur_cursor = len(window.items)-1
