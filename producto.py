class Producto:
    def __init__(self, data:dict):
        self.name = data["name"]
        self.category = data["category"]
        self.price_buy = data["price_buy"]
        self.price_sell = data["price_sell"]
        self.stock = data["stock"]
        self.type = data["type"]

    def setPriceSell(self):
        pass

    def calcGain(self):
        return self.price_sell - self.price_buy

    