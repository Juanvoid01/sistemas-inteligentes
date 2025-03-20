from State import State

BRICK = 2
NOTHING = 0
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4

class RomperState(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception):

        vista_up, dist_up = perception[0], perception[4]
        vista_down, dist_down = perception[1], perception[5]
        vista_right, dist_right = perception[2], perception[6]
        vista_left, dist_left = perception[3], perception[7]
        player_x, player_y = perception[8], perception[9]
        command_x, command_y = perception[10],  perception[11]

        if(vista_up == BRICK):
            return MOVE_UP, True  
        elif(vista_down == BRICK):
            return MOVE_DOWN, True 
        elif(vista_right == BRICK):
            return MOVE_RIGHT, True 
        elif(vista_left == BRICK):
            return MOVE_LEFT, True 
        else:
            return NOTHING, False

    #método que se llama para decidir la transición del estado. Devuelve el id del estado nuevo
    def Transit(self,perception):

        vista_up, dist_up = perception[0], perception[4]
        vista_down, dist_down = perception[1], perception[5]
        vista_right, dist_right = perception[2], perception[6]
        vista_left, dist_left = perception[3], perception[7]

        '''if(vista_up == BRICK and dist_up <= 2):
            print("Detectado brick up")
            return "RomperState"
        elif(vista_down == BRICK and dist_down <= 2):
            print("Detectado brick down")
            return "RomperState"
        elif(vista_right == BRICK and dist_right <= 2):
            print("Detectado right")
            return "RomperState"
        elif(vista_left == BRICK and dist_left <= 2):
            print("Detectado left")
            return "RomperState"'''
        return "ExplorarState"
