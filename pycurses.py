import sys, os
import curses
from curses import wrapper
from window import Window, MenuWindow


def main(stdscr):
    user_input = 0
    curses.curs_set(False)
    cur_window = MenuWindow(stdscr)
    cur_window.add_bool(symbol="simulation_platform", default=True, help_str="choose the simulation platform")
    cur_window.add_bool(symbol="pattern", default=False, help_str="choose the pattern")
    pre_window = []
    while True:
        status = cur_window.main_loop()
        if status == Window.EXIT:
            if pre_window:
                cur_window = pre_window.pop()
            else:
                break
        elif status == Window.ENTER:
            sub_window = cur_window.get_subwin()
            if sub_window:
                pre_window.append(cur_window)
                cur_window = sub_window

wrapper(main)
