import abc
import curses

import window
from window import Window
from window.item import Item


class SubwinItem(Item):
    def __init__(self):
        pass

    @abc.abstractclassmethod
    def get_subwin(self):
        pass

    def toggle(self):
        return Window.ENTER

class MenuItem(SubwinItem):
    def __init__(self, symbol, options=None, defaults=None, help_str=""):
        self.symbol = symbol
        if defaults:
            assert set(defaults).issubset(set(options))
        self.options = options
        self.defaults = defaults
        self._help_str = help_str
        self.init_subwin()

    def get_subwin(self):
        return self.subwin

    def init_subwin(self):
        win = curses.newwin(curses.LINES, curses.COLS)
        win.keypad(True)
        subwin = window.MenuWindow(win)
        for option in self.options:
            if self.defaults and option in self.defaults:
                subwin.add_bool(option, default=True)
            else:
                subwin.add_bool(option, default=False)
        self.subwin = subwin

    def str(self):
        symbol_str = self.symbol
        return "-->  {}".format(symbol_str)

    @property 
    def help_str(self):
        return self._help_str

    @property  
    def value(self):
        return {item.symbol: item.value for item in self.subwin.items}
