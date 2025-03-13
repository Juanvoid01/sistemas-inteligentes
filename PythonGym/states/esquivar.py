from State import State

class EsquivarState(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception):
        return 0,True