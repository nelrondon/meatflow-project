import json

class DB:
    @staticmethod
    def get(module):
        path = f"database/{module}.json"
        data = []
        try:
            with open(path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"No existe el archivo {path}")
        except:
            pass
        return data
    
    @staticmethod
    def getOneBy(module, key, value):
        data = DB.get(module)
        for _ in data:
            if _[key] == value:
                return _
                
    @staticmethod
    def getAllBy(module, key, value):
        data = DB.get(module)
        filtered = [d for d in data if d.get(key) == value]
        return filtered
    
    @staticmethod
    def delete(module, key, value):
        path = f"database/{module}.json"
        data = DB.get(module)
        newdata = [d for d in data if d.get(key) != value]
        with open(path, "w") as file:
            json.dump(newdata, file)

    @staticmethod
    def save(module, newdata):
        path = f"database/{module}.json"
        data = DB.get(module)

        data.append(newdata)

        with open(path, "w") as file:
            json.dump(data, file)

    @staticmethod
    def update(module, key, value, newdata):
        path = f"database/{module}.json"
        data = DB.get(module)

        for _ in data:
            if _[key] == value:
                _.update(newdata)

        with open(path, "w") as file:
            json.dump(data, file)
        
