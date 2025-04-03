from LGymClient import agentLoop
#from BaseAgent import BaseAgent
#from PythonGym_v1_2.ReactiveAgent import ReactiveAgent
from GoalOrientedAgent import GoalOrientedAgent


agent = GoalOrientedAgent("1","MiniJuan")
agentLoop(agent,True)

 