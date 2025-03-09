import json
from datetime import datetime, timedelta

# Datos de ventas existentes
ventas_data = [
    {
        "fecha": "2025-03-01",
        "productos_vendidos": [
            {"producto": "Asado de Ternera", "cantidad": 3},
            {"producto": "Lomo", "cantidad": 2}
        ],
        "metodo_pago": "Tarjeta",
        "puntuacion_atencion": 4
    },
    {
        "fecha": "2025-03-02",
        "productos_vendidos": [
            {"producto": "Pechuga de Pollo", "cantidad": 5},
            {"producto": "Costillas de Cerdo", "cantidad": 4}
        ],
        "metodo_pago": "Efectivo",
        "puntuacion_atencion": 5
    }
]

# Añadiendo nuevas ventas en fechas cercanas
nuevas_ventas = [
    {
        "fecha": "2025-03-03",
        "productos_vendidos": [
            {"producto": "Milanesa de Ternera", "cantidad": 4},
            {"producto": "Chorizo", "cantidad": 3}
        ],
        "metodo_pago": "Tarjeta",
        "puntuacion_atencion": 5
    },
    {
        "fecha": "2025-03-04",
        "productos_vendidos": [
            {"producto": "Bondiola", "cantidad": 2},
            {"producto": "Punta de Anca", "cantidad": 1}
        ],
        "metodo_pago": "Efectivo",
        "puntuacion_atencion": 4
    },
    {
        "fecha": "2025-03-05",
        "productos_vendidos": [
            {"producto": "Bife de Chorizo", "cantidad": 3},
            {"producto": "Tapa de Anca", "cantidad": 2}
        ],
        "metodo_pago": "Tarjeta",
        "puntuacion_atencion": 5
    },
    {
        "fecha": "2025-03-06",
        "productos_vendidos": [
            {"producto": "Lomo de Res", "cantidad": 5},
            {"producto": "Carne Molida", "cantidad": 6}
        ],
        "metodo_pago": "Efectivo",
        "puntuacion_atencion": 4
    },
    {
        "fecha": "2025-03-07",
        "productos_vendidos": [
            {"producto": "Tapa de Lomo", "cantidad": 2},
            {"producto": "Cuadril", "cantidad": 3}
        ],
        "metodo_pago": "Tarjeta",
        "puntuacion_atencion": 4
    },
    {
        "fecha": "2025-03-08",
        "productos_vendidos": [
            {"producto": "Punta de Cuadril", "cantidad": 2},
            {"producto": "Tapa de Lomo de Cerdo", "cantidad": 1}
        ],
        "metodo_pago": "Efectivo",
        "puntuacion_atencion": 5
    }
]

# Añadiendo las nuevas ventas a las ventas existentes
ventas_data.extend(nuevas_ventas)

# Guardar las ventas actualizadas en el archivo JSON
with open("database/ventas.json", "w", encoding="utf-8") as file:
    json.dump(ventas_data, file, indent=4, ensure_ascii=False)

print("✅ Nuevas ventas agregadas correctamente.")
