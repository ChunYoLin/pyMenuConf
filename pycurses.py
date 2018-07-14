import sys, os
import curses
from curses import wrapper
from window import menuwindow


def main(stdscr):
    user_input = 0
    curses.curs_set(False)
    cur_window = menuwindow(stdscr, ["aaaaaa", "bbbbbb"])
    next_window = menuwindow(stdscr, ["ddd", "ccc"])
    cur_window.add_subwin("aaaaaa", next_window)
    cur_window.draw()
    while True:
        user_input = cur_window.win.getch()
        if user_input == ord('q'):
             cur_window = cur_window.get_prewin()
        elif user_input == curses.KEY_DOWN:
            cur_window.down()
        elif user_input == curses.KEY_UP:
            cur_window.up()
        elif user_input == 10:
            sub_window = cur_window.get_subwin()
            if sub_window != None:
                sub_window.prewin = cur_window 
                cur_window = sub_window
        if cur_window == None:
            break
        cur_window.draw()
            
wrapper(main)
