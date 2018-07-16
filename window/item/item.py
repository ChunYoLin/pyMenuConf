import abc
import curses

import window
from window import Window


class Item(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def toggle(self):
        pass

    @abc.abstractclassmethod
    def str(self):
        pass

    @property
    @abc.abstractclassmethod
    def help_str(self):
        pass

class BoolItem(Item):
    def __init__(self, symbol, default=False, help_str=""):
        assert default in [True, False]
        self.symbol = symbol
        self.default = default
        self._help_str = help_str
        self.choice = self.default
    
    def toggle(self):
        self.choice = not self.choice

    def str(self):
        #  option string
        option_str = '[ ]'
        if self.choice == True:
            option_str = '[X]'
        #  symbol string
        symbol_str = self.symbol
        return "{}  {}".format(option_str, symbol_str)

    @property 
    def help_str(self):
        return self._help_str

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
        return "     {} ----->".format(symbol_str)

    @property 
    def help_str(self):
        return self._help_str
    
        
