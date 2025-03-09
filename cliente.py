import datetime, uuid
from handledb import DB
from tkinter import messagebox

class Feedback:
    def __init__(self, msg):
        self.msg = msg
        self.date = datetime.datetime.now()

class Cliente:
    def __init__(self, data, name=None):
        self.id = data["id"] if data != None else str(uuid.uuid4())
        self.name = data["name"] if data != None else name
        self.frec_visit = data["frec_visit"] if data != None else 0
        self.feedback : list[dict] = data["feedback"] if data != None else []
    
    def register(self):
        try:
            props = ["id", "name", "frec_visit", "feedback"]
            reg = {prop: getattr(self, prop) for prop in props}
            DB.save("clientes", reg)
            messagebox.showinfo("Registro", "Cleinte registrado con exito")
        except:
            messagebox.showinfo("Error", "Cliente no registrado")
        
    def __repr__(self):
        return f" Id: {self.id}\n Nombre: {self.name}\n visitas: {self.frec_visit}\n comentario: {self.feedback}"