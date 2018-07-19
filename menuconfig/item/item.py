import os
os.environ.setdefault('ESCDELAY', '25')
import abc
import curses
from math import ceil
from curses import textpad

import menuconfig
from menuconfig import Window


class Item(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def toggle(self):
        pass

    @abc.abstractclassmethod
    def prefix_str(self):
        pass

    @property
    @abc.abstractclassmethod
    def symbol_str(self):
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

    @property 
    def prefix_str(self):
        return "[X]" if self.value else "[ ]"

    @property
    def symbol_str(self):
        return self.symbol

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
        text_start = 3, 15-ceil(len(title)/2)
        win.move(text_start[0], text_start[1])
        win.box()
        curses.curs_set(1)
        value = ""
        while(True):
            ch = win.getch()
            if ch in (27, ):
                break
            elif ch in (ord('\n'), ):
                self.value = value
                break
            elif ch in (curses.KEY_BACKSPACE, 127, ):
                value = value[:-1]
                win.addstr(text_start[0], text_start[1], value+" ")
                win.addstr(text_start[0], text_start[1], value)
            else:
                value += chr(ch)
                win.addstr(text_start[0], text_start[1], value)
        curses.curs_set(0)
        curses.noecho()
        
    @property
    def prefix_str(self):
        return self.value

    @property
    def symbol_str(self):
        return self.symbol

    @property 
    def help_str(self):
        return self._help_str

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class EnumItem(StringItem):
    def __init__(self, symbol, allow_values, default="", help_str=""):
        super().__init__(symbol, default, help_str)
        assert type(allow_values) == list
        if default:
            assert default in allow_values
        self._allow_values = [""] + allow_values
        self._cur_value_idx = self._allow_values.index(default)

    def toggle(self):
        if self._cur_value_idx < len(self._allow_values)-1:
            self._cur_value_idx += 1
        else:
            self._cur_value_idx = 0
        self.value = self.allow_values[self._cur_value_idx]

    @property
    def allow_values(self):
        return self._allow_values

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

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
    
    @value.setter
    def value(self, value):
        for item in self.subwin.items:
            if item.symbol == value:
                item.value = True
