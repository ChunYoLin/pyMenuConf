import abc
import curses

import menuconfig
from menuconfig import Window
from menuconfig.item import Item
from menuconfig.item import BoolItem


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
        subwin = menuconfig.MenuWindow(win)
        for option in self.options:
            if self.defaults and option in self.defaults:
                subwin.add_item(BoolItem(option, default=True))
            else:
                subwin.add_item(BoolItem(option, default=False))
        self.subwin = subwin

    @property
    def prefix_str(self):
        return "----->"

    @property
    def symbol_str(self):
        return self.symbol

    @property 
    def help_str(self):
        return self._help_str

    @property  
    def value(self):
        return [item.symbol for item in self.subwin.items if item.value]
