import curses
from curses import wrapper
from menuconfig import WindowManager, MenuWindow
from menuconfig.item import MenuItem, BoolItem, StringItem, EnumItem


def main(stdscr):
    curses.curs_set(False)
    main_window = MenuWindow(stdscr, "Buying Option")
    main_window.add_item(BoolItem(symbol="buy", default=False, help_str="buy or not"))
    main_window.add_item(MenuItem(symbol="colors", options=["red", "blue", "green"], help_str="choose the colors"), depend_bool=["buy"])
    main_window.add_item(StringItem(symbol="location", default="your home address", help_str="set the shipping location"))
    main_window.add_item(EnumItem(symbol="gift", allow_values=["100$", "beer"], default="beer", help_str="choose your gift"), depend_string=[("colors", ["blue", "red"])])
    conditem = BoolItem(symbol="kobe", default=False, help_str="xxxx")
    main_window.cond("buy", True, main_window.add_item, conditem)
    main_window.cond("buy", False, main_window.remove_item, conditem.symbol)
    wm = WindowManager(main_window)
    wm.run()
wrapper(main)
