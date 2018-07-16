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
