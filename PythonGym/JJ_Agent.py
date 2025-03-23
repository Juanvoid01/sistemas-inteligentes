#JJ_Agent.py

from BaseAgent import BaseAgent
from StateMachine import StateMachine, State
from states.MoveToCommandCenter import MoveToCommandCenter
from states.EnemyEncounter import EnemyEncounter
from states.DestroyCommandCenter import DestroyCommandCenter
from Perception import *

class JJ_Agent(BaseAgent):

    def __init__(self, id, name):
        super().__init__(id, name)

        states_dict:dict[str,State] = {
        "EnemyEncounter" : EnemyEncounter("EnemyEncounter"),
        "MoveToCommandCenter" : MoveToCommandCenter("MoveToCommandCenter"),
        "DestroyCommandCenter" : DestroyCommandCenter("DestroyCommandCenter")
        }
       
        self.stateMachine:StateMachine = StateMachine("Basico",states_dict,"MoveToCommandCenter")

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception):

        perception_class:Perception = Perception(perception)
        print(perception_class)
        print(self.stateMachine.curentState)
        decision = self.stateMachine.Update(perception_class)
        print(f"Decision: {decision}")
        return decision
    


