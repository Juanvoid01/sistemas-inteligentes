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
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

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
            print("Replanificando...")
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
             # Obtenemos la meta más prioritaria según el GoalMonitor
            current_goal = self.goalMonitor.GetCurrentGoal()
            
            # Creamos el nodo inicial basado en la posición actual del agente
            initial_node = self._CreateInitialNode(perception)
            
            # Establecemos la meta actual en el problema
            self.problem.SetGoal(current_goal)
            
            '''# Calculamos el plan usando A*
                self.aStar.Solve(self.problem, initial_node)
                
                # Si encontramos un plan, lo mostramos (opcional)
                if self.aStar.GetPlan():
                    print("Nuevo plan generado:")
                    GoalOrientedAgent.ShowPlan(self.aStar.GetPlan())

            return self.aStar.GetPlan()'''
             # Calcular el plan con A*
            if self.aStar.Solve(self.problem, initial_node):
                self.plan = self.aStar.GetPlan()
                if self.plan:
                    print("Nuevo plan generado:")
                    GoalOrientedAgent.ShowPlan(self.plan)
            else:
                self.plan = []  # No hay camino
            
        return self.plan
        
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
        goal1CommanCenter = None
        goal2Life = self._CreateLifeGoal(perception)
        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor = GoalMonitor(self.problem,[goal1CommanCenter,goal2Life,goal3Player])


        initial_node = self._CreateInitialNode(perception)
        '''goal1 = self._CreateDefaultGoal(perception)
        goal2 = self._CreateLifeGoal(perception)
        goal3 = self._CreatePlayerGoal(perception)'''

        goal_command_center = self._CreateDefaultGoal(perception)  # Meta 0: Centro de comando
        goal_life = self._CreateLifeGoal(perception)               # Meta 1: Vida
        goal_player = self._CreatePlayerGoal(perception)           # Meta 2: Jugador


        # Obtener dimensiones del mapa
        #self.xSize = sqrt(len(map))     # Ancho (columnas)
        #self.ySize = len(map[0])   # Alto (filas)
        #print("GoalOrientedAgent InitAgent Revisar que map es una lista 2D para obtener sus dimensiones")

        # Calcular dimensiones del mapa (asumiendo que es cuadrado)
        map_size = int(len(map)**0.5)  # Si el mapa es 1D y cuadrado (ej: 15x15)
        self.xSize = map_size
        self.ySize = map_size
        
        # Crear el problema BCProblem con la meta inicial (COMMAND_CENTER)
        self.problem = BCProblem(initial_node, goal_command_center, self.xSize, self.ySize)
         # Inicializar el mapa en el problema
        self.problem.InitMap(map)
        # Inicializar A* en base al  mapa
        self.aStar = AStar(self.problem)

        self.goalMonitor = GoalMonitor(self.problem, [goal_command_center, goal_life, goal_player])
        #self.goalMonitor = GoalMonitor(self.problem, [goal1, goal2, goal3])
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