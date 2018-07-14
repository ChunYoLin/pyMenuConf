import sys, os
import curses
from curses import wrapper
from window import window, menuwindow


def main(stdscr):
    user_input = 0
    curses.curs_set(False)
    cur_window = menuwindow(stdscr, ["aaaaaa", "bbbbbb"])
    next_window = menuwindow(stdscr, ["ddd", "ccc"])
    cur_window.add_subwin("aaaaaa", next_window)
    while True:
        status = cur_window.main_loop()
        if status == window.EXIT:
            pre_window = cur_window.prewin
            if pre_window:
                pre_window.main_loop()
            break
        elif status == window.ENTER:
            sub_window = cur_window.get_subwin()
            if sub_window:
                sub_window.prewin = cur_window
                cur_window = sub_window
wrapper(main)
