import sys, os
import curses
from curses import wrapper

class menuwindow():
    def __init__(self, win, items):
        self.win = win
        self.items = items
        self.prewin = None
        self.subwin = {subwin_key: None for subwin_key in items}
        self.cur_cursor = 0

    def add_subwin(self, item, win):
        self.subwin[item] = win

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

    def get_prewin(self):
        return self.prewin

    def get_subwin(self):
        subwin_key = self.items[self.cur_cursor]
        subwin = self.subwin[subwin_key]
        return subwin

def main(stdscr):
    user_input = 0
    curses.curs_set(False)
    cur_window = menuwindow(stdscr, ["aaaaaa", "bbbbbb"])
    next_window = menuwindow(stdscr, ["ddd", "ccc"])
    cur_window.add_subwin("aaaaaa", next_window)
    cur_window.draw()
    while True:
        user_input = cur_window.win.getch()
        if user_input == ord('q'):
             cur_window = cur_window.get_prewin()
        elif user_input == curses.KEY_DOWN:
            cur_window.down()
        elif user_input == curses.KEY_UP:
            cur_window.up()
        elif user_input == 10:
            sub_window = cur_window.get_subwin()
            if sub_window != None:
                sub_window.prewin = cur_window 
                cur_window = sub_window
        if cur_window == None:
            break
        cur_window.draw()
            
wrapper(main)
