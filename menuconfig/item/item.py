import os
os.environ.setdefault('ESCDELAY', '25')
import abc
import curses
from math import ceil
from curses import textpad

import menuconfig
from menuconfig import Window


class Item(metaclass=abc.ABCMeta):
    def __init__(self, symbol, default, help_str):
        self.__symbol = symbol
        self.__default = default
        self.__value = default
        self.__help_str = help_str
        self.__config = False
        self.__callbacks = []

    @abc.abstractclassmethod
    def toggle(self):
        pass

    @property
    @abc.abstractclassmethod
    def prefix_str(self):
        pass

    @property
    def symbol_str(self):
        return self.__symbol

    @property
    def help_str(self):
        return self.__help_str

    @property
    def default(self):
        return self.__default

    @property
    def symbol(self):
        return self.__symbol

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.config = False
        self.check_callback(self.__value)

    def add_callback(self, value, f, *fargs, **fkwargs):
        self.__callbacks.append((value, f, fargs, fkwargs))

    def check_callback(self, value):
        for v, f, fargs, fkwargs in self.__callbacks:
            if isinstance(v, list):
                if value in v:
                    f(*fargs, **fkwargs)
            else:
                if v == value:
                    f(*fargs, **fkwargs)

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        self.__config = value

    @property
    @abc.abstractclassmethod
    def type_str(self):
        pass

class BoolItem(Item):
    def __init__(self, symbol, default=False, help_str=""):
        assert default in [True, False]
        super().__init__(symbol, default, help_str)
    
    def toggle(self):
        self.value = not self.value

    @property 
    def prefix_str(self):
        return "[X]" if self.value else "[ ]"

    @property 
    def type_str(self):
        return "BOOL"

class StringItem(Item):
    def __init__(self, symbol, default="", help_str=""):
        super().__init__(symbol, default, help_str)

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
    def type_str(self):
        return "STRING"

class EnumItem(StringItem):
    def __init__(self, symbol, allow_values, default="", help_str=""):
        assert type(allow_values) == list
        super().__init__(symbol, default, help_str)
        if default:
            assert default in allow_values
        self.__allow_values = [""] + allow_values
        self._cur_value_idx = self.__allow_values.index(default)

    def toggle(self):
        if self._cur_value_idx < len(self.__allow_values)-1:
            self._cur_value_idx += 1
        else:
            self._cur_value_idx = 0
        self.value = self.allow_values[self._cur_value_idx]

    @property
    def allow_values(self):
        return self.__allow_values

    @property 
    def type_str(self):
        return "ENUM"

class SubwinItem(Item):
    @abc.abstractclassmethod
    def get_subwin(self):
        pass

    def toggle(self):
        return Window.ENTER

class MenuItem(SubwinItem):
    def __init__(self, symbol, options=None, default=None, help_str=""):
        super().__init__(symbol, default, help_str)
        if default:
            assert set(default).issubset(set(options))
        self.__options = options
        self.init_subwin()

    def get_subwin(self):
        return self.subwin

    def init_subwin(self):
        win = curses.newwin(curses.LINES, curses.COLS)
        win.keypad(True)
        subwin = menuconfig.MenuWindow(win)
        for option in self.options:
            if self.default and option in self.default:
                subwin.add_item(BoolItem(option, default=True))
            else:
                subwin.add_item(BoolItem(option, default=False))
        self.subwin = subwin

    @property
    def options(self):
        return self.__options

    @property
    def prefix_str(self):
        return "----->"

    @property  
    def value(self):
        return [item.symbol for item in self.subwin.items if item.value]
    
    @value.setter
    def value(self, value):
        for item in self.subwin.items:
            if item.symbol == value:
                item.value = True

    #  overwrite the value setter, must set the config property as well
    @property
    def config(self):
        return all([item.config for item in self.subwin.items])

    @config.setter
    def config(self, value):
        for item in self.subwin.items:
            item.config = value

    @property 
    def type_str(self):
        return "MENU"
