#EnemyEncounter.py

from State import State
from Perception import *

class EnemyEncounter(State):
    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception: Perception) -> tuple[int, bool]:
        # Find and attack the enemy player
        if perception.can_fire:
            for dir in [DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT]:
                object, dist = perception.object_in_dir(dir)
                if object == Object.PLAYER or object == Object.SHELL:
                    return dir, True
        else:
            for dir in [DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT]:
                object, dist = perception.object_in_dir(dir)
                if not is_blocker[object]:
                    return dir, False
                
        return DIR_NOTHING, False

    def Transit(self, perception: Perception) -> str:
        # Stay in EnemyEncounter if a player or shell is still detected
        for dir in [DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT]:
            object, dist = perception.object_in_dir(dir)
            if object == Object.PLAYER or object == Object.SHELL:
                return self.id

        return "MoveToCommandCenter"