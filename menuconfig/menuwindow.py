import re
import curses
from menuconfig.window import Window


class MenuWindow(Window):
    def __init__(self, win):
        super().__init__()
        self.__win = win
        self.__items = []
        self.__item_symbols = []
        self.__callbacks = {}
        self.cur_cursor = 0

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
        if self.items:
            item_index = self.__item_symbols.index(symbol)
            item = self.__items[item_index]
            return item

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
        self.update_item()
        self.win.clear()
        max_prefix_len = max([len(item.prefix_str) for item in self.items])
        max_symbol_len = max([len(item.symbol_str) for item in self.items])
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        for idx, item in enumerate(self.items):
            #  format the option string
            item_str = ""
            if item.config == False:
                item_str += "*"
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
                self.win.addstr(idx, 0, item_str, curses.A_REVERSE+curses.color_pair(1))
            else:
                self.win.addstr(idx, 0, item_str)

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
                group = re.match("(.*)=(.*)", line)
                if group:
                    symbol, value = group[1], group[2]
                    value = value.replace("\"", "")
                    value = value.replace("\'", "")
                    value = value.split()
                    item = self.get_item(symbol)
                    if item and item.symbol == symbol:
                        for v in value:
                            if v == "True":
                                v = True
                            if v == "False":
                                v = False
                            if v == "None":
                                v = None
                            item.value = v
