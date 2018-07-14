import sys, os
import curses
from curses import wrapper

class window():
    def __init__(self, win, items):
        self.win = win
        self.items = items
        self.cur_cursor = 0

    def draw(self):
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


def main(stdscr):
    user_input = 0
    curses.curs_set(False)
    cur_window = window(stdscr, ["aaaaaa", "bbbbbb"])
    cur_window.draw()
    while user_input != ord('q'):
        user_input = cur_window.win.getch()
        if user_input == curses.KEY_DOWN:
            cur_window.down()
        elif user_input == curses.KEY_UP:
            cur_window.up()
        elif user_input == curses.KEY_ENTER:
            cur_window.win.clear()
        cur_window.draw()
            
wrapper(main)
