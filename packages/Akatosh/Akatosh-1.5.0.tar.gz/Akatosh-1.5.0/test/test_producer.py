from typing import List
from Akatosh import Actor, Producer, Mundus


class Milk(Actor):
    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(at=Mundus.now, step=1, priority=1, **kwargs)
        self._life_time = 0
        self._expired = False

    def action(self):
        if self.expired:
            return
        self._life_time +=1
        if self._life_time > 5:
            self._expired = True
            print(f"Milk {self.id} expired")
            if self in milkfarm.inventory:
                milkfarm.inventory.remove(self)

    @property
    def expired(self) -> bool:
        return self._expired
    
class Buyer(Actor):

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(at=0, step=1, priority=1, **kwargs)

    def action(self):
        if len(milkfarm.inventory)>=1:
            milk:List[Milk] = milkfarm.distribute(self, 1)
            milk[0].deactivate()
            print(f"Buyer {self.id} bought one milk {milk[0].id}")


milkfarm = Producer(product=Milk, production_period=1, production_rate=3, priority=0, capacity=10)
customer = Buyer()


Mundus.simulate(20)
