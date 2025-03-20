from LGymClient import agentLoop
from BaseAgent import BaseAgent
from ReactiveAgent import ReactiveAgent
from GoalOrientedAgent import GoalOrientedAgent


agent = GoalOrientedAgent("1","Isma")
agentLoop(agent,True)

 