from StateMachine.State import State
from States.AgentConsts import AgentConsts
from MyProblem.BCProblem import BCProblem


#Sigue el path calculado
class ExecutePlan(State):

    def __init__(self, id):
        super().__init__(id)
        self.nextNode = 0
        self.lastMove = 0
        self.transition = ""

    def Start(self,agent):
        self.transition = ""

    def Update(self, perception, map, agent):
        shot = False
        move = self.lastMove
        xW = perception[AgentConsts.AGENT_X]
        yW = perception[AgentConsts.AGENT_Y]
        x,y = BCProblem.WorldToMapCoordFloat(xW,yW,agent.problem.ySize)
        # si estas en el nodo = lo elimino para poder seguir con el siguiente, si me quedo sin nodos, es que he llegado ahora me puede interesar quedarme a 2 nodos.
        plan = agent.GetPlan()
        if len(plan) == 0 : # no tengo un plan para conseguir mis objetivos, me quedo quieto.
            agent.goalMonitor.ForceToRecalculate()
            return AgentConsts.NO_MOVE,False
        
        nextNode = plan[0]
        if self.IsInNode(nextNode,x,y,0.17) and len(plan) > 1:
            plan.pop(0) #este nodo ya no me vale
            if len(plan) == 0: # si al llegar al punto ya no hay nada mas que hacer me paro e indico que se recalcule
                agent.goalMonitor.ForceToRecalculate()
                return AgentConsts.NO_MOVE,False
            nextNode = plan[0]
        goal = agent.problem.GetGoal()
        ## si estoy a distancia 1 del objetivo me paro
        if  len(plan) <= 1 and (goal.value == AgentConsts.PLAYER or goal.value == AgentConsts.COMMAND_CENTER): 
            self.transition = "Attack"
            move = self.GetDirection(nextNode,x,y)
            agent.directionToLook = move-1 ## la percepción es igual que el movimiento pero restando 1                
            shot = self.lastMove == move and perception[AgentConsts.CAN_FIRE] == 1
        else:
            move = self.GetDirection(nextNode,x,y)
            shot = nextNode.value == AgentConsts.BRICK or nextNode.value == AgentConsts.COMMAND_CENTER
        self.lastMove = move
        return move, shot

    def Transit(self,perception, map):
        if self.transition != None and self.transition != "":
            return self.transition 
        return self.id

    @staticmethod
    def MoveDown(node,x,y):
        return abs(node.x+0.5 - x) <= abs(node.y+0.5 - y) and (node.y+0.5) >= y #+0.5 por el centro del nodo
    

    @staticmethod
    def MoveUp(node,x,y):
        return abs(node.x+0.5 - x) <= abs(node.y+0.5 - y) and (node.y+0.5) <= y #+0.5 por el centro del nodo
    

    @staticmethod
    def MoveRight(node,x,y):
        return abs(node.x+0.5 - x) >= abs(node.y+0.5 - y) and (node.x+0.5) >= x #+0.5 por el centro del nodo
    

    @staticmethod
    def MoveLeft(node,x,y):
        return abs(node.x+0.5 - x) >= abs(node.y+0.5 - y) and (node.x +0.5) <= x #+0.5 por el centro del nodo
    
    @staticmethod
    def IsInNode(node, x,y, threshold):
        return abs(node.x+0.5 - x) < threshold and abs(node.y+0.5 - y)< threshold #+0.5 porque es el centro del nodo
    
    def GetDirection(self, node, x, y):
        if ExecutePlan.MoveDown(node,x,y):# me muevo hacia abajo
            return AgentConsts.MOVE_DOWN
        elif ExecutePlan.MoveUp(node,x,y):# me muevo hacia abajo
            return AgentConsts.MOVE_UP
        elif ExecutePlan.MoveRight(node,x,y):# me muevo hacia abajo
            return AgentConsts.MOVE_RIGHT
        elif ExecutePlan.MoveLeft(node,x,y):# me muevo hacia abajo
            return AgentConsts.MOVE_LEFT
        else:
            return AgentConsts.NO_MOVE
            #me muevo en la dirección donde haya mas diferencia

