import sys, os
import curses
from curses import wrapper
from window import window, menuwindow


def main(stdscr):
    user_input = 0
    curses.curs_set(False)
    cur_window = menuwindow(stdscr, ["aaaaaa", "bbbbbb"])
    pre_window = []
    next_window = menuwindow(stdscr, ["ddd", "ccc"])
    cur_window.add_subwin("aaaaaa", next_window)
    while True:
        status = cur_window.main_loop()
        if status == window.EXIT:
            if pre_window:
                cur_window = pre_window.pop()
            else:
                break
        elif status == window.ENTER:
            sub_window = cur_window.get_subwin()
            if sub_window:
                pre_window.append(cur_window)
                cur_window = sub_window

wrapper(main)
