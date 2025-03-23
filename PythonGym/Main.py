from LGymClient import agentLoop
from JJ_Agent import JJ_Agent

#agent = BaseAgent("1","Isma")
agent = JJ_Agent("1","JJ_agent")
agentLoop(agent,True)
