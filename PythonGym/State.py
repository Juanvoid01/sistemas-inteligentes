from Perception import Perception

class State:
    def __init__(self, id):
        self.id = id

    #Metodo que se llama al iniciar el estado
    def Start(self):
        print("Inicio del estado ")

    #Metodo que se llama en cada actualización del estado
    #devuelve las acciones (actuadores) que el agente realiza
    def Update(self, perception : Perception) -> tuple[int, bool] :
        return 0,True
    
    #método que se llama para decidir la transición del estado. Devuelve el id del estado nuevo
    def Transit(self,perception : Perception) -> str :
        return self.id
    
    #Metodo que se llama al finalizar el estado
    def End(self):
        print("fin del estado")