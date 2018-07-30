import curses
from curses import wrapper
from menuconfig import WindowManager, MenuWindow
from menuconfig.item import MenuItem, BoolItem, StringItem, EnumItem


def main(stdscr):
    curses.curs_set(False)
    main_window = MenuWindow(stdscr, "Buying Option")
    wm = WindowManager(main_window)
    main_window.reset()
    main_window.import_menu("menu.cache")
    main_window.add_item(BoolItem(symbol="buy", default=False, help_str="buy or not"))
    if main_window["buy"] == True:
        item = BoolItem(symbol="sell", default=False, help_str="sell or not")
    main_window.add_item(MenuItem(symbol="colors", options=["red", "blue", "green"], help_str="choose the colors"))
    main_window.add_item(StringItem(symbol="location", default="your home address", help_str="set the shipping location"))
    main_window.add_item(EnumItem(symbol="gift", allow_values=["100$", "beer"], default="beer", help_str="choose your gift"))
    wm.run()
wrapper(main)
