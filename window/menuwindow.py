import curses
from window.window import window


class menuwindow(window):
    def __init__(self, win, items):
        super().__init__()
        self.__win = win
        self.__prewin = None
        self.items = items
        self.subwin = {subwin_key: None for subwin_key in items}
        self.cur_cursor = 0

    @property
    def win(self):
        return self.__win

    @property
    def prewin(self):
        return self.__prewin

    @prewin.getter
    def prewin(self):
        return self.__prewin

    @prewin.setter 
    def prewin(self, win):
        self.__prewin = win

    def add_subwin(self, item, win):
        self.subwin[item] = win

    def get_subwin(self):
        subwin_key = self.items[self.cur_cursor]
        subwin = self.subwin[subwin_key]
        return subwin

    def draw(self):
        self.win.clear()
        for idx, item in enumerate(self.items):
            if idx == self.cur_cursor:
                self.win.addstr(idx, 0, item, curses.A_REVERSE)
            else:
                self.win.addstr(idx, 0, item)

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

