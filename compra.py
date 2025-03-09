import datetime

class Compra:
    def __init__(self, supplier, prod_buy, quality):
        self.supplier = supplier
        self.products_buy = prod_buy
        self.quality = quality
        self.date = datetime.datetime.now()