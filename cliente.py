import datetime, uuid
from handledb import DB, FieldDb

class Feedback (FieldDb):
    def __init__(self, msg):
        self.message = msg
        self.date = str(datetime.datetime.now())
    
    def export(self):
        return self.__dict__

class Cliente:
    def __init__(self, data=None, name=None):
        self.id = data["id"] if data != None else str(uuid.uuid4())
        self.name = data["name"] if data != None else name
        self.frec_visit = data["frec_visit"] if data != None else 0
        self.feedback : list[dict] = data["feedback"] if data != None else []

    def addFeedback(self, msg):
        self.feedback.append(Feedback(msg).export())

    def register(self):
        try:
            props = ["id", "name", "frec_visit", "feedback"]
            reg = {prop: getattr(self, prop) for prop in props}
            DB.save("clientes", reg)
            return True
        except:
            return False