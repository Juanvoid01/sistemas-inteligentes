from State import State
import random
import math

PLAYER = 4
SHELL = 5
BRICK = 2
UNBREAKABLE = 1
COMMAND_CENTER = 3


NOTHING = 0
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4


class ExplorarState(State):

    dir_moving = None
    cont_stuck = 0
    past_agent_x = -1
    past_agent_y = -1

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception):
 
        command_x, command_y = perception[10],  perception[11]
        agent_x = perception[12]
        agent_y = perception[13]

        if(self.cont_stuck >= 6):
            dir = random.randint(1,4)
            print("Se eligio random dir")
            return dir, False
            
        if(self.past_agent_x == agent_x and self.past_agent_y == agent_y):
            self.cont_stuck = self.cont_stuck + 1
        else:
             self.cont_stuck = 0
        self.past_agent_x = agent_x
        self.past_agent_y = agent_y
        

        #Nos movemos en direccion al Commmand Centre
        if(abs(agent_x - command_x) >= (abs(agent_y - command_y))):
            if(agent_x < command_x):
                dir = MOVE_RIGHT
            elif(agent_x > command_x):
                dir = MOVE_LEFT
        else:
            if(agent_y < command_y):
                dir = MOVE_UP
            elif(agent_y > command_y):
                dir = MOVE_DOWN

        while(perception[dir-1] == UNBREAKABLE and perception[dir-1+4] <= 2):
            dir = random.randint(1,4)

            
        self.dir_moving = dir
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
        agent_x, agent_y = perception[12],  perception[13]
         
        
        #Si despue de huir vemos un enemigo lo atacamos, sino exploramos
        vista_moving_dir = perception[self.dir_moving -1]

       
        if(vista_up == PLAYER or vista_down == PLAYER or vista_left == PLAYER or vista_right == PLAYER):
           return "AtacarState"
        elif(vista_moving_dir == BRICK): #si hay un ladrillo en su dir y esta en
           return "RomperState"
        elif(vista_up == COMMAND_CENTER or vista_down == COMMAND_CENTER or vista_left == COMMAND_CENTER or vista_right == COMMAND_CENTER):
           return "AtacarState"
        else:
           return "ExplorarState"
    
    
