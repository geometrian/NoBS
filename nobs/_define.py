class Define(object):
    def __init__(self, symbol, value=None):
        if not isinstance(symbol,str):
            raise Exception("Define symbol must be a string!")
        if value is not None and not isinstance(value,str):
            raise Exception("Define value must be either \"None\" or a string!")

        self.symbol = symbol
        self.value = value
        
