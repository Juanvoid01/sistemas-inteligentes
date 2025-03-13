from State import State

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


        return 0,True