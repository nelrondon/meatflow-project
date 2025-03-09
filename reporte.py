from inventario import Inventario
from venta import Venta
import matplotlib.pyplot as plt
import numpy as np
class Reporte:
    
    def __init__(self, inventario, ventas):
        self.inventario = inventario  # Objeto Inventario
        self.ventas = ventas  # Lista de objetos Venta
    
    def generar_reporte_ventas(self):
        """Genera un resumen de ventas totales por producto."""
        resumen = {}
        for venta in self.ventas:
            for item in venta.productos_vendidos:
                producto = item['name']
                cantidad = item['amount']
                resumen[producto] = resumen.get(producto, 0) + cantidad
        return resumen
    
    def analizar_producto_mas_vendido(self):
        """Retorna el producto más vendido."""
        resumen = self.generar_reporte_ventas()
        return max(resumen, key=resumen.get)
    
    def recomendar_despieces(self):
        """Recomienda compras según el producto más vendido."""
        mas_vendido = self.analizar_producto_mas_vendido()
        return f"Se recomienda mantener stock alto de {mas_vendido}."
    
    def calcular_porcentaje_ventas(self):
        """Calcula el porcentaje de ventas de cada producto."""
        resumen = self.generar_reporte_ventas()
        total_ventas = sum(resumen.values())
        return {producto: (cantidad / total_ventas) * 100 for producto, cantidad in resumen.items()}
    
    def graficar_tendencias(self):
        """Genera un gráfico de tendencia de ventas a lo largo del tiempo."""
        fechas = sorted(set(venta.fecha for venta in self.ventas))
        productos = set(item['producto'] for venta in self.ventas for item in venta.productos_vendidos)
        
        tendencias = {producto: [0] * len(fechas) for producto in productos}
        for venta in self.ventas:
            fecha_idx = fechas.index(venta.fecha)
            for item in venta.productos_vendidos:
                tendencias[item['producto']][fecha_idx] += item['cantidad']
        
        for producto, cantidades in tendencias.items():
            plt.plot(fechas, cantidades, label=producto)
        
        plt.xlabel('Fecha')
        plt.ylabel('Cantidad Vendida')
        plt.title('Tendencia de Ventas')
        plt.legend()
        plt.xticks(rotation=45)
        plt.show()
