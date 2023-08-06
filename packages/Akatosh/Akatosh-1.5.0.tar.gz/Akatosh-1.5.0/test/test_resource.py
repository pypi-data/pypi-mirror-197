from Akatosh import Mundus, Actor, Resource

res = Resource(capacity=100)


class User(Actor):
    def __init__(self, name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = name

    def action(self):
        if Mundus.now > 10:
            res.release()
            print(
                f"resources releases all claimed units, usage {res.claimed_quantity/res.capacity}."
            )
        else:
            if res.available_quantity >= 50:
                self.request(res, 10)
                print(
                    f"{self.name} requests 10 units of resource, usage {res.claimed_quantity/res.capacity}."
                )
            if res.available_quantity <= 50:
                self.release(res)
                print(
                    f"{self.name} releases current claimed units of resource, usage {res.claimed_quantity/res.capacity}."
                )


u1 = User(name="User1", at=0, step=1, till=15, priority=0)
u2 = User(name="User2", at=0, step=1, till=15, priority=0)
Mundus.simulate(15)
