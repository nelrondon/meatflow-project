class Proveedor:
    def __init__(self, name, supplied_prod, delivery_time, confiabilidad):
        self.name = name
        self.supplied_prod = supplied_prod
        self.delivery_time = delivery_time
        self.confiabilidad = confiabilidad

    def updateData(self):
        pass
    
    def calcPriority(self):
        pass