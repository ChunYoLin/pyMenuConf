import sys, os
import curses
from curses import wrapper
from window import Window, WindowManager, MenuWindow
from window.item import BoolItem


def main(stdscr):
    user_input = 0
    curses.curs_set(False)
    main_window = MenuWindow(stdscr)
    main_window.add_menu(symbol="simulation_platform", options=["pro", "rtl"], help_str="choose the simulation platform")
    main_window.add_bool(symbol="pattern", default=False, help_str="choose the pattern")
    main_window.add_string(symbol="isa", default="00", help_str="set the isa")
    main_window.add_enum(symbol="p_isa", allow_values=["00", "10", "20", "25"], default="10", help_str="choose the p isa")
    wm = WindowManager(main_window)
    wm.run()
    print(wm.get_all_values())

wrapper(main)

