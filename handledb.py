import json, os

class FieldDb:
    def export(self):
        return self.__dict__

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
            if str(_[key]).lower() == str(value).lower():
                return _
    @staticmethod
    def searchBy(module, key, value):
        data = DB.get(module)
        result = []
        for _ in data:
            if str(value).lower() in str(_[key]).lower():
                result.append(_)
        return result
                
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
            if str(_[key]).lower() == str(value).lower():
                _.update(newdata)

        with open(path, "w") as file:
            json.dump(data, file)