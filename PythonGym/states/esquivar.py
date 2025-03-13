from State import State

PLAYER = 4
SHELL = 5

NOTHING = 0
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4

class EsquivarState(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception):

        vista_up, dist_up = perception[0], perception[4]
        vista_down, dist_down = perception[1], perception[5]
        vista_right, dist_right = perception[2], perception[6]
        vista_left, dist_left = perception[3], perception[7]
        player_x, player_y = perception[8], perception[9]
        command_x, command_y = perception[10],  perception[11]

        if(vista_up == PLAYER or vista_up == SHELL or vista_down == PLAYER or vista_down == SHELL):
            dir = MOVE_RIGHT if dist_right > dist_left else  MOVE_LEFT
            return dir, False
        elif(vista_left == PLAYER or vista_left == SHELL or vista_right == PLAYER or vista_right == SHELL):
            dir = MOVE_UP if dist_up > dist_down else  MOVE_DOWN
            return dir, False
        
        return 0,True
    
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
        return "ExplorarState"