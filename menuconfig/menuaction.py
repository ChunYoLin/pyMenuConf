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
        return "[ESC] Exit"

    @property
    def key(self):
        return (27,)

    def action(self, window, item):
        return Window.EXIT

class EnterAction(InputAction):
    @property
    def usage(self):
        return "[Enter] Toggle/Enter"

    @property
    def key(self):
        return (ord('\n'), )

    def action(self, window, item):
        return item.toggle()

class RightAction(InputAction):
    @property
    def usage(self):
        return "[->/l] Enter/Next"

    @property
    def key(self):
        return (curses.KEY_RIGHT, ord('l'))

    def action(self, window, item):
        return item.toggle_right()

class ToggleLeftAction(InputAction):
    @property
    def usage(self):
        return "[<-/h] Back/Pre"

    @property
    def key(self):
        return (curses.KEY_LEFT, ord('h'))

    def action(self, window, item):
        item_ret = item.toggle_left()
        if item_ret:
            return item_ret
        elif hasattr(window, "prewin"):
            return Window.BACK

class ConfigAction(InputAction):
    @property
    def usage(self):
        return "[c] Configure"

    @property
    def key(self):
        return (ord('c'), )

    def action(self, window, item):
        return Window.CONFIG

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
        return Window.STAY

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
        return Window.STAY
