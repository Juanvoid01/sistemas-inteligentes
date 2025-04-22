#import sys
#sys.path.insert(1, '../AStar')
from AStar.Problem import Problem
from MyProblem.BCNode import BCNode
from States.AgentConsts import AgentConsts
import sys
import numpy as np

#Clase que implementa el problema especifico que queremos resolver y que hereda de la calse
#Problema genérico.
class BCProblem(Problem):
    

    def __init__(self, initial:BCNode, goal:BCNode, xSize, ySize):
        super().__init__(initial, goal)
        self.map = np.zeros((xSize,ySize),dtype=int)
        self.xSize = xSize
        self.ySize = ySize
    
    #inicializa un mapa con el mapa proveniente del entorno Vector => Matriz
    def InitMap(self,m):
        for i in range(len(m)):
            x,y = BCProblem.Vector2MatrixCoord(i,self.xSize,self.ySize)
            self.map[x][y] = m[i]

    #Muestra el mapa por consola
    def ShowMap(self):
        for j in range(self.ySize):
            s = ""
            for i in range(self.xSize):
                s += ("[" + str(i) + "," + str(j) + "," + str(self.map[i][j]) +"]")
            print(s)

    #Calcula la heuristica del nodo en base al problema planteado (Se necesita reimplementar)
    def Heuristic(self, node:BCNode) -> float:
        #TODO: heurística del nodo
        # usamos la heurística de distancia manhattan hasta el nodo goal
        return abs(self.goal.x - node.x) + abs(self.goal.y - node.y)

    #Genera la lista de sucesores del nodo (Se necesita reimplementar)
    def GetSucessors(self, node:BCNode) -> list[BCNode]:
        successors: list[BCNode] = []
        #TODO: sucesores de un nodo dado
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dir_x, dir_y in directions:
            successor_x = node.x + dir_x
            successor_y = node.y + dir_y
            if 0 <= successor_x < self.xSize and 0 <= successor_y < self.ySize:
                successor:AgentConsts = self.map[successor_x][successor_y]
                if BCProblem.CanMove(successor):
                    self.CreateNode(successors, node, successor_x, successor_y)
        return successors
    
    #métodos estáticos
    #nos dice si podemos movernos hacia una casilla, se debe poner el valor de la casilla como
    #parámetro
    @staticmethod
    def CanMove(value):
        return value != AgentConsts.UNBREAKABLE and value != AgentConsts.SEMI_UNBREKABLE and value != AgentConsts.SEMI_UNBREKABLE
    
    #convierte coordenadas mapa en formato vector a matriz
    @staticmethod
    def Vector2MatrixCoord(pos,xSize,ySize):
        x = pos % xSize
        y = pos // ySize #division entera
        return x,y

    #convierte coordenadas mapa en formato matriz a vector
    @staticmethod
    def Matrix2VectorCoord(x,y,xSize):
        return y * xSize + x
    
    #convierte coordenadas del mapa en coordenadas del entorno (World) (nótese que la Y está invertida)
    @staticmethod
    def MapToWorldCoord(x,y,ySize):
        xW = x * 2
        yW = (ySize - y - 1) * 2
        return xW, yW

    #convierte coordenadas del entorno (World) en coordenadas mapa (nótese que la Y está invertida)
    @staticmethod
    def WorldToMapCoord(xW,yW,ySize):
        x = xW // 2
        y = yW // 2
        y = ySize - y - 1
        return x, y
    
    #versión real del método anterior, que nos ayuda a buscar los centros de las celdas.
    #aqui nos dirá los decimales, es decir como de cerca estamos de la esquina superior derecha
    #un valor de 1.9,1.9 nos dice que estamos en la casilla 1,1 muy cerca de la 2,2
    #en realidad, lo que buscamos es el punto medio de la casilla, es decir la 1.5, 1.5 en el caso
    #de la casilla 1,1
    @staticmethod
    def WorldToMapCoordFloat(xW,yW,ySize):
        x = xW / 2
        invY = (ySize*2) - yW
        invY = invY / 2
        return x, invY

    # Costes por tipo de casilla
    COST_OBJECT_TABLE: dict[AgentConsts, int] = {
        AgentConsts.NOTHING: 1,       # Nada, coste mas bajo
        AgentConsts.BRICK: 10,        # Obstáculo destructible
        AgentConsts.PLAYER: 40,       # Prioridad alta
        AgentConsts.LIFE: 2,          # Recompensa
        AgentConsts.COMMAND_CENTER: 1, # Meta
        AgentConsts.UNBREAKABLE: 100,
        AgentConsts.SHELL: 60 ,
        AgentConsts.OTHER: 50,
        AgentConsts.SEMI_BREKABLE: 100,
        AgentConsts.SEMI_UNBREKABLE: 100
    }

    #se utiliza para calcular el coste de cada elemento del mapa 
    @staticmethod
    def GetCost(value:AgentConsts) -> int:
        #TODO: debes darle un coste a cada tipo de casilla del mapa.
        return BCProblem.COST_OBJECT_TABLE.get(value, sys.maxsize)

    
    #crea un nodo y lo añade a successors (lista) con el padre indicado y la posición x,y en coordenadas mapa 
    def CreateNode(self,successors,parent,x,y):
        value=self.map[x][y]
        g=BCProblem.GetCost(value)
        rightNode = BCNode(parent,g,value,x,y)
        rightNode.SetH(self.Heuristic(rightNode))
        successors.append(rightNode)

    #Calcula el coste de ir del nodo from al nodo to (Se necesita reimplementar)
    def GetGCost(self, nodeTo):
        return BCProblem.GetCost(nodeTo.value)