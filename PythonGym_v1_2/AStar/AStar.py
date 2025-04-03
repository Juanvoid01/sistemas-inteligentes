

#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node
class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem #problema a resolver
        '''self.solution = [] # Camino solución'''

    def GetPlan(self):
        findGoal = False
        #TODO implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        self.open.clear()
        self.precessed.clear()
        self.open.append(self.problem.Initial())
        path = []
        #mientras no encontremos la meta y haya elementos en open....
        #TODO implementar el bucle de búsqueda del algoritmo A*

        '''self.Solve(self, self.problem, self.problem.Initial())
        return self.solution[::-1]  # Devuelve el camino invertido'''

        return path

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found


    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        #TODO: devuelve el path invertido desde la meta hasta que el padre sea None.
        return path




    #bucle principal de A*
''' def Solve(self, problem, initial_node):
        self.problem = problem
        self.open = []
        self.processed = set()
        
        initial_node.SetH(self.problem.Heuristic(initial_node))
        self.open.append(initial_node)
        
        while len(self.open) > 0:
            current = self._GetLowestFNode()
            
            if self.problem.IsASolution(current):
                self.solution = self.ReconstructPath(current)
                return True
                
            self.processed.add(current)
            
            successors = self.problem.GetSucessors(current)
            for successor in successors:
                self._ProcessSuccessor(successor, current)
        
        return False  # No se encontró solución


        def GetPlan(self):
        return self.solution[::-1]  # Devuelve el camino invertido

    def _GetLowestFNode(self):
        self.open.sort(key=lambda x: x.F())
        return self.open.pop(0)

    def _ProcessSuccessor(self, successor, parent):
        new_g = parent.G() + self.problem.GetGCost(parent, successor)
        
        # Si ya está en procesados
        if successor in self.processed:
            if new_g < successor.G():
                self.processed.remove(successor)
                self.open.append(successor)
            else:
                return
                
        # Si ya está en abiertos
        in_open = next((n for n in self.open if n == successor), None)
        if in_open:
            if new_g < in_open.G():
                self._ConfigureNode(in_open, parent, new_g)
        else:
            self._ConfigureNode(successor, parent, new_g)
            successor.SetH(self.problem.Heuristic(successor))
            self.open.append(successor)

    def _ConfigureNode(self, node, parent, new_g):
        node.SetParent(parent)
        node.SetG(new_g)

    def ReconstructPath(self, goal):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = current.GetParent()
        return path


        '''
