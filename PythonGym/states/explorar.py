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
    #cont_stuck = 0         #nº de veces que se mantiene en la misma posicion
    #past_agent_x = -1      #pos de x anterior 
    #past_agent_y = -1      #pos de y anterior
    last_positions = []     # Historial de posiciones(x,y) de las ultimas max_stuck iteraciones
    max_stuck = 6           #nº iteraciones para estar atascado

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception):
 
        command_x, command_y = perception[10],  perception[11]
        agent_x = perception[12]
        agent_y = perception[13]

        #Guardamos la pos en el historial
        self.last_positions.append((agent_x, agent_y))
        if len(self.last_positions) > self.max_stuck: #Eliminar la pos mas vieja
            self.last_positions.pop(0) 

        #Si esta atascado, cambia de direccion
        #if(self.cont_stuck >= 6):
            #dir = random.randint(1,4)
            #print("Se eligio random dir")
            #self.cont_stuck = 0
            #return dir, False
        
        #Si permanece en la misma posicion que antes, se incrementa el
        #contador de atascado
        #if(self.past_agent_x == agent_x and self.past_agent_y == agent_y):
            #self.cont_stuck = self.cont_stuck + 1
        #else:
             #self.cont_stuck = 0
        
        # Si todas las ultimas posiciones son iguales, esta atascado
        if len(set(self.last_positions)) == 1 and len(self.last_positions) == self.max_stuck:
            print("Agente atascado, se eligio random dir")
            print(len(self.last_positions))
            self.last_positions = []
            #comprobamos donde se puede mover, no hay muro en esa dir a dist<=2 
            valid_dirs=[dir for dir in [MOVE_UP,MOVE_DOWN,MOVE_LEFT,MOVE_RIGHT]if(perception[dir-1]!=UNBREAKABLE and perception[dir-1+4]<=2)]
            if valid_dirs:
                dir = random.choice(valid_dirs)
            else:
                dir = random.randint(1, 4)  # Si no, elige aleatorio

            self.dir_moving = dir
            return dir, False
        #else: #Ha cambiado de pos, deja de estar atascado
             #self.last_positions = []  # Reiniciar historial


        #self.past_agent_x = agent_x
        #self.past_agent_y = agent_y
        
        dir = self.dir_moving
        #Nos movemos en direccion al Commmand Centre
        '''dir_selected = False
        if(abs(agent_x - command_x) >= (abs(agent_y - command_y))):
            if agent_x < command_x and perception[MOVE_RIGHT - 1] != UNBREAKABLE:
                dir = MOVE_RIGHT
                dir_selected = True
            elif(agent_x > command_x and perception[MOVE_LEFT - 1] != UNBREAKABLE):
                dir = MOVE_LEFT
                dir_selected = True
        if(not dir_selected):
            if agent_y < command_y and perception[MOVE_UP - 1] != UNBREAKABLE:
                dir = MOVE_UP
            elif agent_y > command_y and perception[MOVE_DOWN - 1] != UNBREAKABLE:
                dir = MOVE_DOWN'''
        
        # Guardamos las direcciones que van hacia el Command Center, siempre que no esten bloqueadas
        preferred_dirs = []  # Array para guardar las dirs viables
        horizontal_first = abs(agent_x - command_x) >= abs(agent_y - command_y)  # Prioridad en x si es mayor o igual

        # Intentar primero en la direccion prioritaria(Donde hay mas dist con el Command Centre)
        if horizontal_first:
            if agent_x < command_x and perception[MOVE_RIGHT - 1] != UNBREAKABLE:
                preferred_dirs.append(MOVE_RIGHT)
            elif agent_x > command_x and perception[MOVE_LEFT - 1] != UNBREAKABLE:
                preferred_dirs.append(MOVE_LEFT)
        else:
            if agent_y < command_y and perception[MOVE_UP - 1] != UNBREAKABLE:
                preferred_dirs.append(MOVE_UP)
            elif agent_y > command_y and perception[MOVE_DOWN - 1] != UNBREAKABLE:
                preferred_dirs.append(MOVE_DOWN)

        # Si no hay direcciones viables, probamos la otra direccion
        if not preferred_dirs:
            if not horizontal_first: # ahora al reves, donde hay menos dist con el Command Centre
                if agent_x < command_x and perception[MOVE_RIGHT - 1] != UNBREAKABLE:
                    preferred_dirs.append(MOVE_RIGHT)
                elif agent_x > command_x and perception[MOVE_LEFT - 1] != UNBREAKABLE:
                    preferred_dirs.append(MOVE_LEFT)
            else:  
                if agent_y < command_y and perception[MOVE_UP - 1] != UNBREAKABLE:
                    preferred_dirs.append(MOVE_UP)
                elif agent_y > command_y and perception[MOVE_DOWN - 1] != UNBREAKABLE:
                    preferred_dirs.append(MOVE_DOWN)

        # Si hay alguna direccion hacia el Command centre a la que se puede ir
        if preferred_dirs:
            dir = preferred_dirs[0]  #  la primera que se podia


        #1Comprobar que no se va amover hacia un muro indestructible
        #while(perception[dir-1] == UNBREAKABLE and perception[dir-1+4] <= 2):
            #dir = random.randint(1,4)

        #2Comprobar que no se va amover hacia un muro indestructible
        #if perception[dir - 1] == UNBREAKABLE and perception[dir-1+4] <= 2:
            #valid_dirs = [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]
            #print("Agente tiene unbreakeable delante, se eligio random dir")
            #for new_dir in valid_dirs:
                 #if perception[new_dir - 1] != UNBREAKABLE:
                    #dir = new_dir 
                    #break
            
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
        print(self.dir_moving)
        vista_moving_dir = perception[self.dir_moving -1]

       
        #Comprobamos si podemos atacar al payer/Command Ctr/Shell, explorar o romper un ladrillo
        if(vista_up == PLAYER or vista_down == PLAYER or vista_left == PLAYER or vista_right == PLAYER):
           return "AtacarState"
        elif(vista_up == COMMAND_CENTER or vista_down == COMMAND_CENTER or vista_left == COMMAND_CENTER or vista_right == COMMAND_CENTER):
           return "AtacarState"
        elif(vista_up == SHELL or vista_down == SHELL or vista_left == SHELL or vista_right == SHELL):
           return "AtacarState"
        elif(vista_moving_dir == BRICK):
           return "RomperState"
        else:
           return "ExplorarState"
    
    
