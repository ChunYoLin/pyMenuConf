import curses
from window.window import Window
from window.item import BoolItem, MenuItem, StringItem, EnumItem


class MenuWindow(Window):
    def __init__(self, win):
        super().__init__()
        self.__win = win
        self.items = []
        self.cur_cursor = 0

    @property
    def win(self):
        return self.__win

    def add_bool(self, symbol, default=False, help_str=""):
        item = BoolItem(symbol, default, help_str)
        self.items.append(item)

    def add_menu(self, symbol, options=None, defaults=None, help_str=""):
        item = MenuItem(symbol, options, defaults, help_str)
        self.items.append(item)

    def add_string(self, symbol, default="", help_str=""):
        item = StringItem(symbol, default, help_str)
        self.items.append(item)

    def add_enum(self, symbol, allow_values, default="", help_str=""):
        item = EnumItem(symbol, allow_values, default, help_str)
        self.items.append(item)

    def cur_item(self):
        if self.items:
            return self.items[self.cur_cursor]

    def draw(self):
        self.win.clear()
        max_y, max_x = self.win.getmaxyx()
        max_prefix_len = max([len(item.prefix_str) for item in self.items])
        max_symbol_len = max([len(item.symbol_str) for item in self.items])
        symbol_pos = max_prefix_len + 5
        help_pos = symbol_pos + max_symbol_len +5
        for idx, item in enumerate(self.items):
            item_str = item.prefix_str + " "*(max_prefix_len-len(item.prefix_str)+5) + item.symbol_str + " "*(max_symbol_len-len(item.symbol_str)+5) + item.help_str
            if idx == self.cur_cursor:
                self.win.addstr(idx, 0, item_str, curses.A_REVERSE)
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
