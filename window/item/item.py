import abc


class Item(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def toggle(self):
        pass

    @abc.abstractclassmethod
    def str(self):
        pass

    @abc.abstractclassmethod
    def help_str(self):
        pass

class BoolItem(Item):
    def __init__(self, symbol, default=False, help_str=""):
        assert default in [True, False]
        self.symbol = symbol
        self.default = default
        self._help_str = help_str
        self.choice = self.default
    
    def toggle(self):
        self.choice = not self.choice

    def str(self):
        #  option string
        option_str = '[ ]'
        if self.choice == True:
            option_str = '[X]'
        #  symbol string
        symbol_str = self.symbol
        return "{}  {}".format(option_str, symbol_str)

    def help_str(self):
        return self._help_str
