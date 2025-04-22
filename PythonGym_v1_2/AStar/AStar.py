#AStar.py

from AStar.Node import Node
from AStar.Problem import Problem

#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node
class AStar:

    def __init__(self, problem:Problem):
        self.open:list[Node] = [] # lista de abiertos o frontera de exploración, lista ordenada por F
        self.processed:set = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem:Problem = problem #problema a resolver

    def GetPlan(self):
        #TODO implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        self.open.clear()
        self.processed.clear()
        self.InsertNode(self.problem.Initial())
        #mientras no encontremos la meta y haya elementos en open....
        #TODO implementar el bucle de búsqueda del algoritmo A*
        # Configurar nodo inicial
        start = self.problem.Initial()
        start.SetG(0.0)
        start.SetH(self.problem.Heuristic(start))
        self.InsertNode(start)

        while self.open:
            # Seleccionar nodo con f más bajo, tenemos una lista ordenada
            current = self.open.pop(0)

            if self.problem.IsASolution(current):
                return self.ReconstructPath(current) # solucion encontrada

            self.processed.add(current) # Marcar como procesado

            # Expandir sucesores
            for successor in self.problem.GetSucessors(current):
                
                if successor in self.processed:
                    continue    # Ignorar si ya procesado

                # Calcular coste
                tentativeG = current.G() + self.problem.GetGCost(successor)

                # miramos si el nodo ya ha sido explorado
                existing = self.GetSucesorInOpen(successor)
                if existing is None:
                    # Nuevo nodo en encontrado
                    self._ConfigureNode(successor, current, tentativeG)
                    self.InsertNode(successor)
                elif tentativeG < existing.G():
                    # El nodo ha sido reencontrado, recalculamos el coste
                    self._ConfigureNode(successor, current, tentativeG)
                    self.open.remove(successor)
                    self.InsertNode(successor)

        return []

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)
        node.SetH(self.problem.Heuristic(node))

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor) -> Node:
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found


    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal:Node) -> list[Node]:
        path:list[Node] = []
        #TODO: devuelve el path invertido desde la meta hasta que el padre sea None.
        node:Node = goal
        while node is not None:
            path.append(node)
            node = node.GetParent()
        return path[::-1]

    def InsertNode(self, node: Node):
        """Inserta 'node' en self.open de forma que la lista siga ordenada por F() ascending."""
        lo, hi = 0, len(self.open)
        f_new = node.F()
        # búsqueda binaria
        while lo < hi:
            mid = (lo + hi) // 2
            if self.open[mid].F() < f_new:
                lo = mid + 1
            else:
                hi = mid
        self.open.insert(lo, node)