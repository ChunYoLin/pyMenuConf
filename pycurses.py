import sys, os
import curses
from curses import wrapper
from window import Window, MenuWindow
from window.item import BoolItem


def main(stdscr):
    user_input = 0
    curses.curs_set(False)
    main_window = MenuWindow(stdscr)
    main_window.add_menu(symbol="simulation_platform", options=["prosim", "rtl"], help_str="choose the simulation platform")
    main_window.add_bool(symbol="pattern", default=False, help_str="choose the pattern")
    cur_window = main_window
    pre_window = []
    while True:
        status = cur_window.main_loop()
        if status == Window.EXIT:
            if pre_window:
                cur_window = pre_window.pop()
            else:
                break
        elif status == Window.ENTER:
            sub_window = cur_window.cur_item().get_subwin()
            if sub_window:
                pre_window.append(cur_window)
                cur_window = sub_window
    curses.endwin()
    print(main_window.get_all_values())
wrapper(main)

