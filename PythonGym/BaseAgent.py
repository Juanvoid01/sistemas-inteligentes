import random
from StateMachine import StateMachine, State
from states.atacar import AtacarState
from states.esquivar import EsquivarState
from states.explorar import ExplorarState
from states.romper import RomperState

from enum import Enum, auto

NOTHING = 0
UNBREAKABLE = 1
BRICK = 2
COMMAND_CENTER = 3
PLAYER = 4
SHELL = 5
OTHER = 6



def move_to_dir_action(dir):
        return dir+1


State()

class BaseAgent:

    def __init__(self, id, name):
        self.id = id
        self.name = name

        states_dict:dict[str,State] = {
        "AtacarState" : AtacarState("AtacarState"),
        "ExplorarState" : ExplorarState("ExplorarState"),
        "EsquivarState" : EsquivarState("EsquivarState"),
        "RomperState" : RomperState("RomperState")
        }
        self.stateMachine:StateMachine = StateMachine("Basico",states_dict,"GoToCommandCenter")

    #Devuelve el nombre del agente
    def Name(self):
        return self.name
    #Devuelve el id del agente
    def Id(self):
        return self.id
    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        print("Inicio del agente ")

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception):
        print("Toma de decisiones del agente")
        print(perception)
        
        vista_up, dist_up = perception[0], perception[4]
        vista_down, dist_down = perception[1], perception[5]
        vista_right, dist_right = perception[2], perception[6]
        vista_left, dist_left = perception[3], perception[7]
        player_x, player_y = perception[8], perception[9]
        command_x, command_y = perception[10],  perception[11]



        self.analizar(perception)

        if(self.state == self.State.EXPLORANDO):
            return self.accion_explorar(self, perception)
        elif(self.state == self.State.ATACANDO):
            return self.accion_explorar(self, perception)
        elif(self.state == self.State.EXPLORANDO):
            return self.accion_explorar(self, perception)

        action = random.randint(0,4)
        return action, True
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        print("Agente finalizado")
        print("Victoria ",win)

    def analizar(self, perception):

        element_found = False

        for dir in range(0,4):
            if perception[dir] == COMMAND_CENTER :
                element_found = True
                self.command_center_dir = dir


                self.state = self.State.ATACANDO
                break            
            elif perception[dir] == PLAYER:
                element_found = True
                self.state = self.State.ATACANDO
                break           
            elif perception[dir] == SHELL:
                self.state = self.State.ATACANDO
                element_found = True
                break

        if element_found is False:
            self.state = self.State.EXPLORANDO

        return NOTHING, False


    def accion_explorar(self, perception):
        perception
        action = move_to_dir_action(dir_empty)
        return action, False
       

    def accion_disparar_command_centre(self, dir_command_centre):

        action = move_to_dir_action(dir_command_centre)
        return action, True

    def accion_disparar_enemigo(self, dir_enemigo):

        action = move_to_dir_action(dir_enemigo)
        return action, True
    
    def accion_disparar_ladrillo(self, dir_ladrillo):

        action = move_to_dir_action(dir_ladrillo)
        return action, True

