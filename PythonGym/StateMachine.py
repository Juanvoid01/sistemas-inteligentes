from State import State
from Perception import Perception

class StateMachine(State):
    def __init__(self, id, states, initial):
        super().__init__(id)
        self.states = states
        self.curentState = initial
    
    #Metodo que se llama al iniciar la máquina de estado
    def Start(self):
        print("Inicio de la maquina de estados ")
        self.states[self.curentState].Start()

    #Metodo que se llama en cada actualización del estado
    #devuelve las acciones (actuadores) que el agente realiza
    def Update(self, perception: Perception) -> tuple[int, bool] :
        actions = self.states[self.curentState].Update(perception)
        newState=self.states[self.curentState].Transit(perception)
        if newState != self.curentState:
            self.states[self.curentState].End()
            self.curentState=newState
            self.states[self.curentState].Start()
        return actions
    

    #Metodo que se llama al finalizar la máquina de estado
    #def End(self, win):
        #super().End(win)