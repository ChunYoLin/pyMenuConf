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
