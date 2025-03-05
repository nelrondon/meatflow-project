from proveedor import Proveedor
import datetime

class Compra:
    def __init__(self, supplier:Proveedor, prod_buy, quality):
        self.supplier = supplier
        self.products_buy = prod_buy
        self.quality = quality
        self.date = datetime.datetime.now()