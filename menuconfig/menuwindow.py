import re
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
        self.update_item()
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
        
        offset_y = 1
        pre_len = 0
        for idx, usage in enumerate(self.usage):
            self.win.addstr(usage_y+offset_y, pre_len, usage)
            pre_len += len(usage)+3
            if idx % 3 == 0 and idx != 0:
                offset_y += 1
                pre_len = 0
                

    def down(self):
        if self.cur_cursor < len(self.items)-1:
            self.cur_cursor += 1
        else:
            self.cur_cursor = len(self.items)-1

    def up(self):
        if self.cur_cursor > 0:
            self.cur_cursor -= 1
        else:
            self.cur_cursor = 0

    @property
    def usage(self):
        usage_list = []
        exit_usage = "[q] Exit"
        enter_usage = "[ENTER] Toggle/Enter"
        config_usage = "[c] for config"
        usage_list.append(exit_usage)
        usage_list.append(enter_usage)
        usage_list.append(config_usage)
        return usage_list

    def main_loop(self):
        #  draw the menu
        self.draw()
        #  process user input
        user_input = self.win.getch()
        if user_input == ord('q'):
            return self.EXIT
        elif user_input == ord('\n'):
            cur_item = self.cur_item()
            return cur_item.toggle()
        elif user_input == ord('c'):
            for item in self.items:
                item.config = True
            return self.CONFIG
        else:
            if user_input == curses.KEY_DOWN:
                self.down()
            elif user_input == curses.KEY_UP:
                self.up()
            return self.STAY

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

