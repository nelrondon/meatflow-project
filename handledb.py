import json, os

class DB:
    @staticmethod
    def getPath(module):
        return f"database/{module}.json"

    @staticmethod
    def exists(module):
        path = DB.getPath(module)
        return os.path.exists(path)

    @staticmethod
    def get(module):
        path = DB.getPath(module)
        data = []
        try:
            with open(path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"No existe el modulo {module}, crealo!")
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
        path = DB.getPath(module)
        data = DB.get(module)
        newdata = [d for d in data if d.get(key) != value]
        with open(path, "w") as file:
            json.dump(newdata, file)

    @staticmethod
    def save(module, newdata):
        path = DB.getPath(module)
        data = DB.get(module)

        data.append(newdata)
        try:
            with open(path, "w") as file:
                json.dump(data, file)
            return True
        except:
            return False

    @staticmethod
    def createMod(module):
        path = DB.getPath(module)
        open(path, "w")


    @staticmethod
    def update(module, key, value, newdata):
        path = DB.getPath(module)
        data = DB.get(module)

        for _ in data:
            if _[key] == value:
                _.update(newdata)

        with open(path, "w") as file:
            json.dump(data, file)