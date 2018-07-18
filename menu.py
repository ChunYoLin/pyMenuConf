import sys, os
import curses
from curses import wrapper
from window import Window, WindowManager, MenuWindow
from window.item import MenuItem, BoolItem, StringItem, EnumItem


def main(stdscr):
    user_input = 0
    curses.curs_set(False)
    main_window = MenuWindow(stdscr)
    main_window.add_item(MenuItem(symbol="simulation_platform", options=["pro", "rtl"], help_str="choose the simulation platform"))
    main_window.add_item(BoolItem(symbol="sim_pattern", default=False, help_str="sim the pattern"))
    main_window.add_item(BoolItem(symbol="pattern", default=False, help_str="choose the pattern"), depend_bool=["sim_pattern"], depend_string=[("simulation_platform", "pro")])
    main_window.add_item(StringItem(symbol="isa", default="00", help_str="set the isa"))
    main_window.add_item(EnumItem(symbol="p_isa", allow_values=["00", "10", "20", "25"], default="10", help_str="choose the p isa"))
    wm = WindowManager(main_window)
    wm.run()
    print(wm.get_all_values())

wrapper(main)

