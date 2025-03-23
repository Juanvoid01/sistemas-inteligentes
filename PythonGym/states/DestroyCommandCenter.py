#MoveToCommandCenter.py
import random

from State import State
from Perception import *

class DestroyCommandCenter(State):
    def __init__(self, id):
        super().__init__(id)
        self.last_dir = False

    def Update(self, perception: Perception) -> tuple[int, bool]:
        p: Perception = perception

        # Check if the command center is directly in any direction
        for dir in [DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT]:
            object, dist = perception.object_in_dir(dir)
            if object == Object.COMMAND_CENTER:
                return dir, True  # Move toward the command center and shoot it

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
        if is_destroyable[object_p] or not is_blocker[object_p]:
            return preferred_dir, True 

        # Preferred direction is blocked, try second direction
        object_s, dist_s = perception.object_in_dir(second_dir)
        if is_destroyable[object_s] or not is_blocker[object_s]:
            return second_dir, True

        # Random direction
        random_dir = random.choice([DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT])
        return random_dir, True 

    def Transit(self, perception: Perception) -> str:
        # Switch to EnemyEncounter if a player is detected
        for dir in [DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT]:
            object, dist = perception.object_in_dir(dir)
            if object == Object.PLAYER:
                return "EnemyEncounter"
        return self.id