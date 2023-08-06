from Akatosh import Actor, Mundus
from random import random

Mundus.accuracy = 4

# first two with step size and till
test_actor = Actor(at=0, step=0.01, till=0.06, priority=0, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor.priority}:\tTest Actor 1 is running."))
test_actor2 = Actor(at=0, step=0.01, priority=-1, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor2.priority}:\tTest Actor 2 is running."))
test_actor3 = Actor(at=0.9, step=0.01, after=[test_actor, test_actor2], priority=1, action=lambda: print(f"Time: {Mundus.now}\tEvent Priority: {test_actor3.priority}:\tTest Actor 3 is running."))

Mundus.simulate(1.5)
print(test_actor.status)
