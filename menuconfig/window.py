import abc
import curses


class Window(metaclass=abc.ABCMeta):
    EXIT = 0
    ENTER = 1
    STAY = 2
    CONFIG = 3
    BACK = 4

    def __init__(self):
        pass

    @abc.abstractclassmethod
    def main_loop(self):
        pass

class WindowManager():
    def __init__(self, main_window, cachepath="menu.cache"):
        assert isinstance(main_window, Window)
        self.main_window = main_window
        self.cachepath = cachepath

    def run(self):
        cur_window = self.main_window
        pre_window = []
        while True:
            status = cur_window.main_loop()
            if status == Window.EXIT:
                break
            elif status == Window.ENTER:
                if hasattr(cur_window.cur_item(), "get_subwin"):
                    sub_window = cur_window.cur_item().get_subwin()
                    if sub_window:
                        pre_window.append(cur_window)
                        cur_window = sub_window
                        cur_window.set_prewin(pre_window[-1])
            elif status == Window.CONFIG:
                for item in cur_window.items:
                    item.config = True
                for win in pre_window:
                    for item in win.items:
                        item.config = True
                self.main_window.export_menu(self.cachepath)
            elif status == Window.BACK:
                if pre_window:
                    cur_window = pre_window.pop()
        curses.endwin()

    def get_all_values(self):
        return self.main_window.get_all_values()
