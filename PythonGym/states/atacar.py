from State import State

COMMAND_CENTER = 3
PLAYER = 4

NOTHING = 0
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4

class AtacarState(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception):

        vista_up, dist_up = perception[0], perception[4]
        vista_down, dist_down = perception[1], perception[5]
        vista_right, dist_right = perception[2], perception[6]
        vista_left, dist_left = perception[3], perception[7]
        player_x, player_y = perception[8], perception[9]
        command_x, command_y = perception[10],  perception[11]

        #Si ve a un enemigo, se mueve hacia el
        if(vista_up == COMMAND_CENTER):
            return MOVE_UP, True  
        elif(vista_down == COMMAND_CENTER):
            return MOVE_DOWN, True 
        elif(vista_right == COMMAND_CENTER):
            return MOVE_RIGHT, True 
        elif(vista_left == COMMAND_CENTER):
            return MOVE_LEFT, True
        elif(vista_up == PLAYER):
            return MOVE_UP, True  
        elif(vista_down == PLAYER):
            return MOVE_DOWN, True 
        elif(vista_right == PLAYER):
            return MOVE_RIGHT, True 
        elif(vista_left == PLAYER):
            return MOVE_LEFT, True 

        return NOTHING,True
    

     #método que se llama para decidir la transición del estado. Devuelve el id del estado nuevo
    def Transit(self,perception):

        return "ExplorarState"