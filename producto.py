class Producto:
    def __init__(self, name, cat, p_buy, p_sell, exp_date, stock, tipo):
        self.name = name
        self.category = cat
        self.price_buy = p_buy
        self.price_sell = p_sell
        self.exp_date = exp_date
        self.stock = stock

        self.type = tipo

    def setPriceSell(self):
        pass

    def calcGain(self):
        pass

    