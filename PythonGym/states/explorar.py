from State import State
import random
import math

PLAYER = 4
SHELL = 5
BRICK = 2
UNBREAKABLE = 1


NOTHING = 0
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4


class ExplorarState(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception):
 
        command_x, command_y = perception[10],  perception[11]
        agent_x = perception[12]
        agent_y = perception[12]

        if(abs(agent_x - command_x) > (abs(agent_y - command_y))):
            if(agent_x < command_x):
                dir = MOVE_RIGHT
            elif(agent_x > command_x):
                dir = MOVE_LEFT
        else:
            if(agent_y < command_y):
                dir = MOVE_UP
            elif(agent_y > command_y):
                dir = MOVE_DOWN

        print(dir)
        return dir, False

    #método que se llama para decidir la transición del estado. Devuelve el id del estado nuevo
    def Transit(self,perception):
        vista_up, dist_up = perception[0], perception[4]
        vista_down, dist_down = perception[1], perception[5]
        vista_right, dist_right = perception[2], perception[6]
        vista_left, dist_left = perception[3], perception[7]
        player_x, player_y = perception[8], perception[9]
        command_x, command_y = perception[10],  perception[11]

        #Si despue de huir vemos un enemigo lo atacamos, sino exploramos
        if(vista_up == PLAYER or vista_down == PLAYER or vista_left == PLAYER or vista_right == PLAYER):
           return "AtacarState"
        elif(vista_up == BRICK or vista_down == BRICK or vista_left == BRICK or vista_right == BRICK):
           return "RomperState"
        else:
         return "ExplorarState"
    
        return 0, False
    
