from BaseAgent import BaseAgent
from StateMachine.StateMachine import StateMachine
from States.ExecutePlan import ExecutePlan
from GoalMonitor import GoalMonitor
from AStar.AStar import AStar
from MyProblem.BCNode import BCNode
from MyProblem.BCProblem import BCProblem
from States.AgentConsts import AgentConsts
from States.Attack import Attack
from States.RandomMovement import RandomMovement

#implementación de un agente básico basado en objetivos.
#disponemos de la clase GoalMonitor que nos monitorea y replanifica cad cierto tiempo
#o cuando se establezca una serie de condiciones.
class GoalOrientedAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        dictionary = {
        "ExecutePlan" : ExecutePlan("ExecutePlan"),
        "Attack" : Attack("Attack"),
        "RandomMovement" : RandomMovement("RandomMovement")
        }
        
        self.stateMachine = StateMachine("GoalOrientedBehavior",dictionary,"ExecutePlan")
        self.problem:BCProblem = None
        self.aStar:AStar = None
        self.plan:list[BCNode] = None
        self.goalMonitor:GoalMonitor = None
        self.agentInit:bool = False

    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        print("Inicio del agente ")
        self.stateMachine.Start(self)
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception, map):
        if perception == True or perception == False:
            return 0,True
        #inicializamos el agente (no lo podemos hacer en el start porque no tenemos el mapa)
        if not self.agentInit:
            self.InitAgent(perception,map)
            self.agentInit = True
 
        #le damos update a la máquina de estados.
        action, shot = self.stateMachine.Update(perception, map, self)

        #Actualizamos el plan refrescando la posición del player (meta 2)
        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor.UpdateGoals(goal3Player,2)
        if self.goalMonitor.NeedReplaning(perception,map,self):
            self.problem.InitMap(map) ## refrescamos el mapa
            self.plan=self._CreatePlan(perception, map)
        return action, shot
    
    #método interno que encapsula la creació nde un plan
    def _CreatePlan(self,perception,map):
        #currentGoal = self.problem.GetGoal()
        if self.goalMonitor != None:
            #TODO creamos un plan, pasos:
            #-con gualMonito, seleccionamos la meta actual (Que será la mas propicia => definir la estrategia a seguir).
            #-le damos el modo inicial _CreateInitialNode
            #-establecer la meta actual al problema para que A* sepa cual es.
            #-Calcular el plan usando A*
            initial_node:BCNode = self._CreateInitialNode(perception)
            goal:BCNode = self.goalMonitor.SelectGoal(perception=perception, map=map, agent=None)
            self.problem.SetInitial(initial_node)
            self.problem.SetGoal(goal)
            
        raw_plan = self.aStar.GetPlan()
        optimized_plan = self._CleanPlan(raw_plan)
        return optimized_plan
    
    @staticmethod
    def CreateNodeByPerception(perception, value, perceptionID_X, perceptionID_Y,ySize):
        xMap, yMap = BCProblem.WorldToMapCoord(perception[perceptionID_X],perception[perceptionID_Y],ySize)
        newNode = BCNode(None,BCProblem.GetCost(value),value,xMap,yMap)
        return newNode

    def _CreatePlayerGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.PLAYER,AgentConsts.PLAYER_X,AgentConsts.PLAYER_Y,15)

    
    def _CreateLifeGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.LIFE,AgentConsts.LIFE_X,AgentConsts.LIFE_Y,15)
    
    def _CreateInitialNode(self, perception):
        node = GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.NOTHING,AgentConsts.AGENT_X,AgentConsts.AGENT_Y,15)
        node.SetG(0)
        return node
    
    def _CreateDefaultGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.COMMAND_CENTER,AgentConsts.COMMAND_CENTER_X,AgentConsts.COMMAND_CENTER_Y,15)
    
    #no podemos iniciarlo en el start porque no conocemos el mapa ni las posiciones de los objetos
    def InitAgent(self,perception,map):
        #creamos el problema
        #TODO inicializamos:
        # - creamos el problema con BCProblem
        # - inicializamos el mapa problem.InitMap
        # - inicializamos A*
        # - creamos un plan inicial
        print("TODO aqui faltan cosas :)")
        goal1CommanCenter = self._CreateDefaultGoal(perception)
        goal2Life = self._CreateLifeGoal(perception)
        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor = GoalMonitor(self.problem,[goal1CommanCenter,goal2Life,goal3Player])

        map_size = int(len(map)**0.5)  # Si el mapa es 1D y cuadrado (ej: 15x15)
        xSize = map_size
        ySize = map_size

        initial_node:BCNode = self._CreateInitialNode(perception)
        self.problem = BCProblem(initial_node, self.goalMonitor.SelectGoal(perception,map,None), xSize, ySize)
        self.problem.InitMap(map)

        self.aStar = AStar(self.problem)
    
        # Generar el plan inicial
        self.plan = self._CreatePlan(perception, map)


    #muestra un plan por consola
    @staticmethod
    def ShowPlan(plan):
        for n in plan:
            print("X: ",n.x,"Y:",n.y,"[",n.value,"]{",n.G(),"} => ")

    def GetPlan(self):
        return self.plan
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        super().End(win)
        self.stateMachine.End()
    
    def _CleanPlan(self, plan: list[BCNode]) -> list[BCNode]:

        if len(plan) == 0:
            return []

        cleaned_list_with_only_turns:list[BCNode] = []
        cleaned_list_with_only_turns.append(plan[0])

        for index_in_plan in range(1, len(plan) - 1):

            previous_node:BCNode = plan[index_in_plan - 1]
            current_node:BCNode = plan[index_in_plan]
            next_node:BCNode = plan[index_in_plan + 1]

            dir_x_before:int = current_node.x - previous_node.x
            dir_y_before:int = current_node.y - previous_node.y

            dir_x_after:int  = next_node.x - current_node.x
            dir_y_after:int  = next_node.y - current_node.y

            # Si cambia la dirección (vector antes != vector después), lo añadimos
            if dir_x_before != dir_x_after or dir_y_before != dir_y_after:
                cleaned_list_with_only_turns.append(current_node)

        cleaned_list_with_only_turns.append(plan[-1])

        return cleaned_list_with_only_turns