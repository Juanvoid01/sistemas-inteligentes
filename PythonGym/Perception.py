#Perception.py

from enum import Enum

DIR_NOTHING = 0
DIR_UP = 1
DIR_DOWN = 2
DIR_RIGHT = 3
DIR_LEFT = 4

class Object(Enum):
    NOTHING = 0
    UNBREAKABLE = 1
    BRICK = 2
    COMMAND_CENTER = 3
    PLAYER = 4
    SHELL = 5
    OTHER = 6

is_destroyable:dict[Object, bool] = {
    Object.NOTHING: False,
    Object.UNBREAKABLE: False,
    Object.BRICK: True,
    Object.COMMAND_CENTER: True,
    Object.PLAYER: True,
    Object.SHELL: True,
    Object.OTHER: False
}

is_blocker:dict[Object, bool] = {
    Object.NOTHING: False,
    Object.UNBREAKABLE: True,
    Object.BRICK: True,
    Object.COMMAND_CENTER: True,
    Object.PLAYER: True,
    Object.SHELL: True,
    Object.OTHER: True
}
class Perception:
    def __init__(self, perception_array: list[int]) -> None:
        
        self.neighborhood_up:Object = Object(perception_array[0])
        self.neighborhood_down:Object = Object(perception_array[1])
        self.neighborhood_right:Object = Object(perception_array[2])
        self.neighborhood_left:Object = Object(perception_array[3])
        
        self.neighborhood_dist_up:float = perception_array[4]
        self.neighborhood_dist_down:float = perception_array[5]
        self.neighborhood_dist_right:float = perception_array[6]
        self.neighborhood_dist_left:float = perception_array[7]
        
        self.player_x:float = perception_array[8]
        self.player_y:float = perception_array[9]
        self.command_center_x:float = perception_array[10]
        self.command_center_y:float = perception_array[11]
        
        self.agent_x:float = perception_array[12]
        self.agent_y:float = perception_array[13]
        
        self.can_fire:bool = bool(perception_array[14])
        self.health:float = perception_array[15]
    
    def object_in_dir(self, dir:int) -> tuple[Object,float]:
        ''' return the object and its distance in the specified direction'''
        if dir==DIR_UP:
            return self.neighborhood_up, self.neighborhood_dist_up
        elif dir==DIR_DOWN:
            return self.neighborhood_down, self.neighborhood_dist_down
        elif dir==DIR_RIGHT:
            return self.neighborhood_right, self.neighborhood_dist_right
        elif dir==DIR_LEFT:
            return self.neighborhood_left, self.neighborhood_dist_left
        else: return Object.NOTHING, 0.0

    def __repr__(self):
        return (f"Perception(Up={self.neighborhood_up}, Down={self.neighborhood_down}, "
                f"Right={self.neighborhood_right}, Left={self.neighborhood_left}, "
                f"DistUp={self.neighborhood_dist_up}, DistDown={self.neighborhood_dist_down}, "
                f"DistRight={self.neighborhood_dist_right}, DistLeft={self.neighborhood_dist_left}, "
                f"Player=({self.player_x}, {self.player_y}), "
                f"CommandCenter=({self.command_center_x}, {self.command_center_y}), "
                f"Agent=({self.agent_x}, {self.agent_y}), "
                f"CanFire={self.can_fire}, Health={self.health})")
