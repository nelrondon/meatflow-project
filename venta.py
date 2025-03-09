from cliente import Cliente
from handledb import DB
from tkinter import messagebox
import datetime

class Venta:
    def __init__(self, client:Cliente, method, rate, produc):
        result = DB.getOneBy("clientes", "id", client.id)
        self.num_bill = self.num_bill()
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
        try:
            props = ["num_bill", "date", "client", "method_paid", "rate_sell", "productos"]
            reg = {prop: getattr(self, prop) for prop in props}
            DB.save("ventas", reg)
            messagebox.showinfo("Registro", "Venta registrada con exito")
        except:
            messagebox.showinfo("Error", "Venta no registrada")
    
    def num_bill(self):
        num_bill_actual = DB.searchBy("ventas", "num_bill", f"")
        if num_bill_actual != [] and num_bill_actual != None:
            new_num_bill = int(num_bill_actual[-1]["num_bill"]) + 1
            return f"{new_num_bill}".zfill(5)
        else:
            return f"{1}".zfill(5)
        
    def __repr__(self):
        return f"Fecha: {self.date}\nCliente:\n CI: {self.client["id"]}\n Nombre: {self.client["name"]}\nMetodo de pago: {self.method_paid}\nProductos: \n 1:{self.productos[0]}\n 2:{self.productos[1]}\n 3:{self.productos[2]}\nMonto: {self.rate_sell}"

datos = {
    "id": "29554133",
    "name": "Henrry Aguey",
    "frec_visit": 1,
    "feedback": "Hola es la primera vez que vengo esta bonito el lugar"
}

compra = [
        ["Carne de res", "0.200", "500"],
        ["Pata de venado", "1", "900"],
        ["Carne molida", "1.400", "600"]
    ]



cliente = Cliente(datos)


venta = Venta(client=cliente, method="Tarjeta Credito", rate=2000, produc=compra)