from cliente import Cliente
from handledb import DB
from tkinter import messagebox
import datetime

class Venta:
    def __init__(self, id_client, method, produc, rate=10):
        result = DB.getOneBy("clientes", "id", id_client)
        self.num_bill = Venta.num_bill()
        self.date = f"{datetime.datetime.now()}"
        self.client = {}
        if result != None:    
            self.client = {
                    "id": result["id"],
                    "name": result["name"]}
        self.method_paid = method
        self.rate_sell = rate
        self.productos = produc
        
    def register(self):
        props = ["num_bill", "date", "client", "method_paid", "rate_sell", "productos"]
        reg = {prop: getattr(self, prop) for prop in props}
        DB.save("ventas", reg)
    
    @staticmethod
    def num_bill():
        num_bill_actual = DB.searchBy("ventas", "num_bill", f"")
        if num_bill_actual != [] and num_bill_actual != None:
            new_num_bill = int(num_bill_actual[-1]["num_bill"]) + 1
            return f"{new_num_bill}".zfill(5)
        else:
            return f"{1}".zfill(5)
        
    def __repr__(self):
        return f"Fecha: {self.date}\nCliente:\n CI: {self.client["id"]}\n Nombre: {self.client["name"]}\nMetodo de pago: {self.method_paid}\nProductos: \n 1:{self.productos[0]}\n 2:{self.productos[1]}\n 3:{self.productos[2]}\nMonto: {self.rate_sell}"
    