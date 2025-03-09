import json

path = "database/productos.json"

try:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        print("✅ El archivo JSON es válido.")
        print("📂 Contenido:", data)
except json.JSONDecodeError as e:
    print(f"❌ ERROR: El archivo tiene un error de formato JSON: {e}")
except FileNotFoundError:
    print("❌ ERROR: El archivo ventas.json no existe en la carpeta database.")
except Exception as e:
    print(f"❌ ERROR desconocido: {str(e)}")
