import random
from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    def __init__(self, problem, goals):
        self.goals = goals # [goal1CommanCenter = 0,goal2Life = 1,goal3Player = 2]
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        self.recalculate = True

    #determina si necesitamos replanificar
    def NeedReplaning(self, perception, map, agent):

        #TODO definir la estrategia de cuando queremos recalcular
        #puede ser , por ejemplo cada cierto tiempo o cuanod tenemos poca vida.

        # Condición 1: Replanificación forzada (ej: obstáculo bloqueó el camino)
        if self.recalculate:
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True

        # Condición 2: Salud baja (< 50%)
        current_health = perception[AgentConsts.HEALTH]
        if current_health <= 50.0:
            return True

        # Condición 3: Tiempo transcurrido desde la última replanificación
        elapsed_time = perception[AgentConsts.TIME] - self.lastTime
        if elapsed_time >= self.replan_interval:
            return True

        # Condición 4: Meta actual fue destruida o inalcanzable
        if self.current_goal and not self._IsGoalReachable(self.current_goal, map):
            return True

        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        #TODO definir la estrategia del cambio de meta
        health = perception[AgentConsts.HEALTH]

        # Centro de comando cerca
        if self._IsCommandCenterNear(perception):
            return self.goals[self.GOAL_COMMAND_CENTER]
        # Jugador cerca (prioridad sobre centro de comando)
        elif self._IsPlayerNear(perception):
            return self.goals[self.GOAL_PLAYER]
        # Salud crítica y vida cerca
        elif health <= 50.0 and self._IsLifeNear(perception):
            return self.goals[self.GOAL_LIFE]
        else:
            return self.goals[self.GOAL_COMMAND_CENTER]
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal

    def _IsCommandCenterNear(self, perception):
        command_x = perception[AgentConsts.COMMAND_CENTER_X]
        command_y = perception[AgentConsts.COMMAND_CENTER_Y]
        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]
        
        distance =  abs(command_x - agent_x) + abs(command_y - agent_y)
        return distance <= 5.0  

    def _IsPlayerNear(self, perception):
        player_x = perception[AgentConsts.PLAYER_X]
        player_y = perception[AgentConsts.PLAYER_Y]
        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]
        
        distance =  abs(player_x - agent_x) + abs(player_y - agent_y)
        return distance <= 15.0  

    def _IsLifeNear(self, perception):
        # Obtener coordenadas del power-up de vida y del agente
        life_x = perception[AgentConsts.LIFE_X]
        life_y = perception[AgentConsts.LIFE_Y]
        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]
        
        distance =  abs(life_x - agent_x) + abs(life_y - agent_y)
        return distance <= 20.0  