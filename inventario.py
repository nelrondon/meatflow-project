from handledb import DB

class Inventario:
    def __init__(self):
        self.products = self.load()
        self.products_min_stock = self.verifyMinStock()
    
    def load(self):
        return DB.get("productos")

    def add(self):
        pass

    def search(self):
        pass

    def verifyMinStock(self):
        minStock = 10
        minStockList = []
        for prod in self.products:
            if prod["stock"] < minStock:
                minStockList.append(prod)
        return minStockList

    def alertExpire(self):
        pass

    def trendStock(self):
        pass

