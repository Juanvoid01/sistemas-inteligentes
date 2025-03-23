#MoveToCommandCenter.py
import random
from State import State
from Perception import *

class MoveToCommandCenter(State):
    def __init__(self, id):
        super().__init__(id)
        self.last_dir = False

    def Update(self, perception: Perception) -> tuple[int, bool]:
        p: Perception = perception

        # Calculate deltas to the command center
        delta_x = p.command_center_x - p.agent_x
        delta_y = p.command_center_y - p.agent_y

        # Determine movement directions based on deltas
        move_dir_x = DIR_RIGHT if delta_x > 0 else DIR_LEFT
        move_dir_y = DIR_UP if delta_y > 0 else DIR_DOWN

        # Prioritize the direction with the larger delta
        if abs(delta_x) > abs(delta_y):
            preferred_dir = move_dir_x
            second_dir = move_dir_y
        else:
            preferred_dir = move_dir_y
            second_dir = move_dir_x

        # Check preferred direction
        object_p, dist_p = perception.object_in_dir(preferred_dir)
        if not (is_blocker[object_p] and dist_p <= 1.0):
            return preferred_dir, False 

        # Preferred direction is blocked, try second direction
        object_s, dist_s = perception.object_in_dir(second_dir)
        if not (is_blocker[object_s] and dist_s <= 1.0):
            return second_dir, False 

        # Both directions blocked, try to destroy obstacle in preferred direction
        if is_destroyable[object_p] and dist_p <= 1.0:
            return preferred_dir, True

        # Preferred direction not destroyable, try second direction
        if is_destroyable[object_s] and dist_s <= 1.0:
            return second_dir, True 

        # Choose a random direction
        random_dir = random.choice([DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT])
        object_r, dist_r = perception.object_in_dir(random_dir)
        shoot = is_destroyable[object_r] and dist_r <= 1.0
        return random_dir, shoot 

    def Transit(self, perception: Perception) -> str:
        # Switch to EnemyEncounter if a player or shell is detected
        for dir in [DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT]:
            object, dist = perception.object_in_dir(dir)
            if object == Object.PLAYER or object == Object.SHELL:
                return "EnemyEncounter"
        delta_x = perception.command_center_x - perception.agent_x
        delta_y = perception.command_center_y - perception.agent_y

        if (abs(delta_x) + abs(delta_y)) <= 4.0:
            return "DestroyCommandCenter" # aproximation, if distance to command center < 8 

        return self.id