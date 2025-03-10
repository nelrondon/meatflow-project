from handledb import DB

def verificar_ventas():
    if DB.exists("ventas"):
        ventas = DB.get("ventas")
        if ventas:
            print("Ventas registradas:")
            for venta in ventas:
                print(venta)
        else:
            print("El archivo ventas.json está vacío.")
    else:
        print("El archivo ventas.json no existe.")

# Ejecutar la función para verificar ventas
verificar_ventas()
