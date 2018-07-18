import sys, os
import curses
from curses import wrapper
from window import Window, WindowManager, MenuWindow
from window.item import MenuItem, BoolItem, StringItem, EnumItem


def main(stdscr):
    user_input = 0
    curses.curs_set(False)
    main_window = MenuWindow(stdscr)
    main_window.add_item(BoolItem(symbol="buy", default=False, help_str="buy or not"))
    main_window.add_item(MenuItem(symbol="colors", options=["red", "blue", "green"], help_str="choose the colors"), depend_bool=["buy"])
    main_window.add_item(StringItem(symbol="location", default="your home address", help_str="set the shipping location"))
    main_window.add_item(EnumItem(symbol="gift", allow_values=["100$", "beer"], default="beer", help_str="choose your gift"))
    wm = WindowManager(main_window)
    wm.run()
    print(wm.get_all_values())

wrapper(main)

