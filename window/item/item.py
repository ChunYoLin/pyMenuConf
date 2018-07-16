import abc
from math import ceil
import curses
from curses import textpad

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

    @property
    @abc.abstractclassmethod
    def value(self):
        pass

class BoolItem(Item):
    def __init__(self, symbol, default=False, help_str=""):
        assert default in [True, False]
        self.symbol = symbol
        self.default = default
        self._help_str = help_str
        self._value = self.default
    
    def toggle(self):
        self.value = not self.value

    def str(self):
        #  option string
        option_str = '[ ]'
        if self.value == True:
            option_str = '[X]'
        #  symbol string
        symbol_str = self.symbol
        return "{}  {}".format(option_str, symbol_str)

    @property 
    def help_str(self):
        return self._help_str

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class StringItem(Item):
    def __init__(self, symbol, default="", help_str=""):
        self.symbol = symbol
        self.default = default
        self._value = self.default
        self._help_str = help_str

    def toggle(self):
        mid_y = int(curses.LINES/2)
        mid_x = int(curses.COLS/2)
        win = curses.newwin(5, 30, mid_y-1, mid_x-15)
        title = "set the {}".format(self.symbol)
        win.keypad(True)
        win.addstr(1, 15-ceil(len(title)/2), title)
        win.move(3, 15-ceil(len(title)/2))
        win.box()
        curses.curs_set(1)
        curses.echo()
        value = win.getstr().decode("utf-8")
        self.value = value
        curses.curs_set(0)
        curses.noecho()
        
    def str(self):
        value_str = self.value
        symbol_str = self.symbol
        return "{}  {}".format(value_str, symbol_str)

    @property 
    def help_str(self):
        return self._help_str

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
