import re
import abc
import curses
from math import ceil
from menuconfig.window import Window


class MenuWindow(Window):
    def __init__(self, win, name=""):
        super().__init__()
        self.__win = win
        self.__items = []
        self.__item_symbols = []
        self.__callbacks = {}
        self.__cur_cursor = -2
        self.name = name
        self.unload = []
        self.init_action()

    def init_action(self):
        self.actions = []
        for action in InputAction.__subclasses__():
            self.actions.append(action())

    @property
    def cur_cursor(self):
        return self.__cur_cursor + 2

    @cur_cursor.setter
    def cur_cursor(self, value):
        self.__cur_cursor = value - 2

    @property
    def win(self):
        return self.__win

    @property
    def items(self):
        return [item for item in self.__items if item.valid]

    def cur_item(self):
        if self.items:
            return self.items[self.cur_cursor]

    def get_item(self, symbol):
        if self.items and symbol in self.__item_symbols:
            item_index = self.__item_symbols.index(symbol)
            item = self.__items[item_index]
            return item
        else:
            return None

    def add_item(self, item, depend_bool=None, depend_string=None):
        item.valid = True
        item.depends = {}
        if depend_bool:
            assert isinstance(depend_bool, list)
            for depend_symbol in depend_bool:
                item.depends[depend_symbol] = True
        if depend_string:
            assert isinstance(depend_string, list)
            for depend_symbol, depend_val in depend_string:
                item.depends[depend_symbol] = depend_val
        self.__items.append(item)
        self.__item_symbols.append(item.symbol)

    def add_callback(self, symbol, value, f, *fargs, **fkwargs):
        self.__callbacks[symbol] = (value, f, fargs, fkwargs)

    def update_item(self):
        for item in self.__items:
            if item.depends:
                self.check_item_depends(item)
            self.check_callback(item)
        _unload = self.unload[:] 
        for line in _unload:
            if self.load_scons_line(line):
                self.unload.remove(line)

    def check_item_depends(self, check_item):
        check = []
        for depend_symbol, depend_val in check_item.depends.items():
            item = self.get_item(depend_symbol)
            if item:
                if isinstance(depend_val, list):
                    if isinstance(item.value, list) and set(depend_val).issubset(item.value):
                        check.append(True)
                    elif len(depend_val) == 1 and depend_val[0] == item.value:
                        check.append(True)
                    else:
                        check.append(False)
                else:
                    if isinstance(item.value, list) and depend_val in item.value:
                        check.append(True)
                    elif depend_val == item.value:
                        check.append(True)
                    else:
                        check.append(False)
        if check:
            check_item.valid = all(check)

    def check_callback(self, item):
        if item.symbol in self.__callbacks.keys():
            value, f, fargs, fkwargs = self.__callbacks[item.symbol]
            if isinstance(item.value, list):
                if value in item.value:
                    f(*fargs, **fkwargs)
            else:
                if item.value == value:
                    f(*fargs, **fkwargs)

    def draw(self):
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.win.bkgdset(" ", curses.A_BOLD)
        self.win.clear()
        #  show the title string
        max_y, max_x = self.win.getmaxyx()
        self.win.addstr(1, 0, " "*max_x, curses.A_REVERSE+curses.color_pair(1))
        self.win.addstr(1, ceil(max_x/2-len(self.name)/2), f"{self.name}", curses.A_REVERSE+curses.color_pair(1))
        max_type_len = max([len(item.type_str) for item in self.items])
        max_prefix_len = max([len(item.prefix_str) for item in self.items])
        max_symbol_len = max([len(item.symbol_str) for item in self.items])
        for idx, item in enumerate(self.items):
            #  format the option string
            item_str = ""
            item_str += f"({item.type_str})"
            item_str += " "*(max_type_len-len(item.type_str)+5)
            if item.config == False:
                item_str += "*"
            else:
                item_str += " "
            if item.prefix_str:
                item_str += item.prefix_str
            if item.symbol_str:
                item_str += " "*(max_prefix_len-len(item.prefix_str)+5)
                item_str += item.symbol_str
            if item.help_str:
                item_str += " "*(max_symbol_len-len(item.symbol_str)+5)
                item_str += item.help_str
            #  highlight the chosen option
            if idx == self.cur_cursor:
                self.win.addstr(idx+2, 0, item_str, curses.A_REVERSE)
            else:
                self.win.addstr(idx+2, 0, item_str)
        #  draw the usage
        usage_y = max_y - 5
        self.win.addstr(usage_y, 0, " "*max_x, curses.A_REVERSE+curses.color_pair(1))
        self.win.addstr(usage_y, ceil(max_x/2)-3, "Usage", curses.A_REVERSE+curses.color_pair(1))
        offset_y = usage_y+1
        for idx, action in enumerate(self.actions):
            usage = action.usage
            line_num = int(idx/3)
            usage_num = idx%3*30
            if line_num == 0:
                self.win.addstr(line_num+offset_y, usage_num, usage)
            if line_num == 1:
                self.win.addstr(line_num+offset_y, usage_num, usage)
            if line_num == 2:
                self.win.addstr(line_num+offset_y, usage_num, usage)

    def main_loop(self):
        #  update item
        self.update_item()
        #  draw the menu
        self.draw()
        #  process user input
        user_input = self.win.getch()
        for action in self.actions:
            if user_input in action.key:
                cur_item = self.cur_item()
                return action.action(self, cur_item)

    def get_all_values(self):
        value_dict = {}
        for item in self.items:
            value_dict[item.symbol] = item.value
        return value_dict
    
    def get_all_config(self):
        return all([item.config for item in self.items])

    def load_scons_config_file(self, config_file):
        with open(config_file) as conf_file:
            for line in conf_file.read().splitlines():
                if not self.load_scons_line(line):
                    self.unload.append(line)

    def load_scons_line(self, line):
        group = re.match("(.*)=(.*)", line)
        if group:
            symbol, value = group[1], group[2]
            value = value.replace("\"", "")
            value = value.replace("\'", "")
            value = value.split(",")
            item = self.get_item(symbol)
            if item:
                for v in value:
                    if v == "True":
                        v = True
                    if v == "False":
                        v = False
                    if v == "None":
                        v = None
                    item.value = v
                return True
            else:
                return False

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

class QuitAction(InputAction):
    @property
    def usage(self):
        return "[q] Exit/Back"

    @property
    def key(self):
        return (ord('q'), )

    def action(self, window, item):
        if all([_item.config for _item in window.items]):
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
