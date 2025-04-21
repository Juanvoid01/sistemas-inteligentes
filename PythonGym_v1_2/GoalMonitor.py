import random
import math
from States.AgentConsts import AgentConsts

class GoalMonitor:
    GOAL_COMMAND_CENTER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2

    def __init__(self, problem, goals):
        self.goals = goals
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False
        self.current_goal = goals[0] if goals else None
        self.replan_interval = 5.0  # Replanificar cada 5 segundos

    def ForceToRecalculate(self):
        self.recalculate = True

    def NeedReplaning(self, perception, map, agent):
        # Condición 1: Replanificación forzada (ej: obstáculo bloqueó el camino)
        if self.recalculate:
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True

        # Condición 2: Salud baja (< 30%)
        current_health = perception[AgentConsts.HEALTH]
        if current_health < 30.0:
            return True

        # Condición 3: Tiempo transcurrido desde la última replanificación
        elapsed_time = perception[AgentConsts.TIME] - self.lastTime
        if elapsed_time >= self.replan_interval:
            return True

        # Condición 4: Meta actual fue destruida o inalcanzable
        if self.current_goal and not self._IsGoalReachable(self.current_goal, map):
            return True

        return False

    def SelectGoal(self, perception, map, agent):
        health = perception[AgentConsts.HEALTH]
        player_near = self._IsPlayerNear(perception)
        life_near = self._IsLifeNear(perception)

        # Estrategia priorizada:
        # 1. Si la salud es crítica (< 25%), buscar vida
        # 2. Si el jugador enemigo está cerca (< 3 unidades), atacarlo
        # 3. Si el centro de comando está cerca, priorizarlo
        # 4. Default: Comando central
        if health < 25.0 and self._IsGoalValid(self.goals[self.GOAL_LIFE]):
            self.current_goal = self.goals[self.GOAL_LIFE]
        elif player_near and self._IsGoalValid(self.goals[self.GOAL_PLAYER]):
            self.current_goal = self.goals[self.GOAL_PLAYER]
        #elif self._IsGoalValid(self.goals[self.GOAL_COMMAND_CENTER]):
            #self.current_goal = self.goals[self.GOAL_COMMAND_CENTER]
        else:
            self.current_goal = self.goals[self.GOAL_COMMAND_CENTER]
        #else:
            #self.current_goal = self.goals[0]  # Fallback

        return self.current_goal
    

    '''def SelectGoal(self, perception, map, agent):
        health = perception[AgentConsts.HEALTH]
        player_near = self._IsPlayerNear(perception)
        life_near = self._IsLifeNear(perception)

        # Estrategia priorizada (actualizada con las nuevas distancias):
        if health < 25.0 and life_near:
            self.current_goal = self.goals[self.GOAL_LIFE]
        elif player_near:
            self.current_goal = self.goals[self.GOAL_PLAYER]
        else:
            self.current_goal = self.goals[self.GOAL_COMMAND_CENTER]  # Default
        
        return self.current_goal'''

    def UpdateGoals(self, goal, goalId):
        self.goals[goalId] = goal

    def GetCurrentGoal(self):
        return self.current_goal
    


    # ------------------- Métodos auxiliares -------------------
    def _IsPlayerNear(self, perception):
        # Obtener coordenadas del jugador y del agente
        player_x = perception[AgentConsts.PLAYER_X]
        player_y = perception[AgentConsts.PLAYER_Y]
        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]
        
        # Calcular distancia Euclidiana
        distance = math.sqrt((player_x - agent_x)**2 + (player_y - agent_y)**2)
        return distance < 4.0  # Considerar "cerca" si está a menos de 4 unidades

    def _IsLifeNear(self, perception):
        # Obtener coordenadas del power-up de vida y del agente
        life_x = perception[AgentConsts.LIFE_X]
        life_y = perception[AgentConsts.LIFE_Y]
        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]
        
        # Calcular distancia Euclidiana (si LIFE_X/Y son -1, no hay power-up)
        if life_x == -1 or life_y == -1:
            return False  # No hay power-up en el mapa
        
        distance = math.sqrt((life_x - agent_x)**2 + (life_y - agent_y)**2)
        return distance < 6.0  # Considerar "cerca" si está a menos de 6 unidades

    def _IsGoalValid(self, goal):
        # Verifica si la meta existe y es alcanzable
        return goal is not None and goal.value != AgentConsts.DESTROYED

    def _IsGoalReachable(self, goal, map):
        # Verifica si hay un camino válido al objetivo (usando el mapa)
        # Implementación simplificada: asume que el valor del nodo es transitable
        return self.problem.CanMove(goal.value)