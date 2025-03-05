import datetime

class Feedback:
    def __init__(self, msg):
        self.msg = msg
        self.date = datetime.datetime.now()

class Cliente:
    def __init__(self, name):
        self.id = 0
        self.name = name
        self.frec_visit = 0
        self.feedback : list[Feedback] = []

fb = Feedback("Prueba")

print(fb.date)