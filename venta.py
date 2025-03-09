from cliente import Cliente
import datetime

class Venta:
    def __init__(self, fecha, productos_vendidos, metodo_pago, puntuacion_atencion):
        self.fecha = fecha
        self.productos_vendidos = productos_vendidos
        self.metodo_pago = metodo_pago
        self.puntuacion_atencion = puntuacion_atencion

    def __repr__(self):
        return f"Venta({self.fecha}, {self.productos_vendidos})"