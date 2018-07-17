import abc
import curses


class Window(metaclass=abc.ABCMeta):
    EXIT = 0
    ENTER = 1
    STAY = 2

    def __init__(self):
        pass

    @abc.abstractclassmethod
    def main_loop(self):
        pass

class WindowManager():
    def __init__(self, main_window):
        assert isinstance(main_window, Window)
        self.main_window = main_window

    def run(self):
        cur_window = self.main_window
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

    def get_all_values(self):
        return self.main_window.get_all_values()
