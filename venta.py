from cliente import Cliente
import datetime

class Venta:
    def __init__(self, client:Cliente, method, rate):
        self.date = datetime.datetime.now()
        self.client = client
        self.method_paid = method
        self.rate_sell = rate