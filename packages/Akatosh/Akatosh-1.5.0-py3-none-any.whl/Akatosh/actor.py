from __future__ import annotations
from typing import Generator, List, Optional, Union, Callable, TYPE_CHECKING
from uuid import uuid4
from math import inf
import warnings

from Akatosh import Timeline, Mundus

if TYPE_CHECKING:
    from Akatosh import Resource
    from Akatosh import Producer


class Actor:

    _id: int
    _action: Optional[Callable]
    _timeline: Timeline
    _priority: int
    _at: Union[int, float, Callable]
    _step: Union[int, float, Callable, None]
    _till: Union[int, float, Callable, None]
    _active: bool
    _after: List[Actor]
    _followers: List[Actor]
    _label: Optional[str]

    _time: Union[int, float]
    _status: List[str]

    def __init__(
        self,
        action: Optional[Callable] = None,
        timeline: Optional[Timeline] = None,
        priority: int = 0,
        at: Union[int, float, Callable] = 0,
        step: Optional[int | float | Callable] = None,
        till: Optional[int | float | Callable] = None,
        active: bool = True,
        after: Optional[Actor | List[Actor]] = None,
        label: Optional[str] = None,
    ) -> None:

        # generate a unique id for this actor
        self._id = uuid4().int

        # assign the label to this actor
        self._label = label or str()

        # assign the action to this actor
        self._action = action

        # assign the timeline to this actor
        if timeline is None:
            self._timeline = Mundus.timeline
        else:
            self._timeline = timeline
        self.timeline.actors.append(self)

        # assign the priority to this actor
        self._priority = priority

        # initialize the follower list
        self._followers = list()

        # assign the waiting target to this actor
        if after is not None:
            if isinstance(after, Actor):
                self._after = [after]
                after.followers.append(self)
                if after.priority > self.priority:
                    warnings.warn(
                        message=f"Actor {self.label} has a lower priority than its waiting event {after.label}."
                    )
            elif isinstance(after, list):
                self._after = after
                for actor in after:
                    actor.followers.append(self)
                    if actor.priority > self.priority:
                        warnings.warn(
                            message=f"Actor {self.label} has a lower priority than its waiting event {actor.label}."
                        )
            else:
                raise TypeError(
                    f"Actor {self.label} has a wrong type of waiting event."
                )

        # initialize the time
        if callable(at):
            self._time = round(at(), Mundus.accuracy)
        else:
            self._time = round(at, Mundus.accuracy)

        if callable(step):
            self._step = step
        elif step is not None:
            if step < ((1/pow(10, Mundus.accuracy))/2):
                raise ValueError(f"Current accuracy is {Mundus.accuracy}, step size cannot be smaller than {(1/pow(10, Mundus.accuracy))/2}.")
            self._step = round(step, Mundus.accuracy)
        else:
            self._step = step

        if callable(till):
            self._till = till
        elif till is not None:
            self._till = round(till, Mundus.accuracy)
        else:
            self._till = till

        # initialize the status
        self._status = list()
        if active and after is None:
            self.status.append("active")
        else:
            self.status.append("inactive")
        if after is not None:
            self.status.append("onhold")

        # schedule the actor onto timeline
        if self.onhold is False and self.active is True:
            self.timeline.schedule(self)

    def perform(self):
        # non-continuous actor
        if self.active and self.onhold is False:
            if self.step is None and self.till is None:
                self.action()
                self.status.append("completed")
                self.status.append("terminated")
                for actor in self.followers:
                    if actor.onhold:
                        actor.activate(force=False)
            # continuous actor but misses step size
            elif self.step is None and self.till is not None:
                raise AttributeError(f"Actor {self.label} has no step size defined.")
            # continuous actor with step size but no end time
            elif self.step is not None and self.till is None:
                while True:
                    self.action()
                    if callable(self.step):
                        self._time += round(self.step(), Mundus.accuracy)
                    else:
                        self._time += round(self.step, Mundus.accuracy)
                    yield self.timeline.schedule(self)
            # continuous actor with step size and end time
            elif self.step is not None and self.till is not None:
                if callable(self.till):
                    _till = round(self.till(), Mundus.accuracy)
                    while True:
                        self.action()
                        if callable(self.step):
                            self._time += round(self.step(), Mundus.accuracy)
                        else:
                            self._time += round(self.step, Mundus.accuracy)
                        if self.time <= _till:  # type: ignore
                            yield self.timeline.schedule(self)
                        else:
                            self.status.append("completed")
                            self.status.append("terminated")
                            for actor in self.followers:
                                if actor.onhold:
                                    actor.activate(force=False)
                            break
                else:
                    while True:
                        self.action()
                        if callable(self.step):
                            self._time += round(self.step(), Mundus.accuracy)
                        else:
                            self._time += round(self.step, Mundus.accuracy)
                        if self.time <= self.till:  # type: ignore
                            yield self.timeline.schedule(self)
                        else:
                            # if this is the last step, activate all followers
                            if self.time >= self.till:
                                self.status.append("completed")
                                self.status.append("terminated")
                                for actor in self.followers:
                                    if actor.onhold:
                                        actor.activate(force=False)
                            break

    def deactivate(self, terminate: bool = True):
        # if the actor is already inactive, do nothing
        if self.inactive:
            return
        else:
            # deactivate the actor
            self.status.remove("active")
            self.status.append("inactive")
            if terminate:
                self.status.append("terminated")
            else:
                if self.time == self.till:
                    self.status.append("completed")
                    self.status.append("terminated")
                else:
                    self.status.append("onhold")

            # activate all followers
            for actor in self.followers:
                if actor.onhold:
                    actor.activate(force=False)

            # remove all events associated with this actor
            for event in self.timeline.events[:]:
                if event.actor.id == self.id:
                    self.timeline.events.remove(event)

    def activate(self, force: bool = True):
        # if the actor is already active, do nothing
        if self.terminated:
            warnings.warn(
                message=f"Actor {self.label} is terminated and cannot be activated."
            )
            return
        elif self.active:
            return
        else:
            # activate the actor if force is True
            if force:
                self.status.remove("inactive")
                if self.onhold:
                    self.status.remove("onhold")
                self.status.append("active")
                self._time = round(self.timeline.now, Mundus.accuracy)
                self.timeline.schedule(self)
            else:
                # activate the actor if all waiting targets are completed
                if all([x.terminated for x in self.after]) is True:
                    self.status.remove("inactive")
                    if self.onhold:
                        self.status.remove("onhold")
                    self.status.append("active")
                    self.timeline.schedule(self)

    def request(self, resource: Resource, amount: Union[int, float] = 1) -> bool:
        return resource.distribute(self, amount)

    def release(self, resource: Resource, amount: Optional[int | float] = None) -> bool:
        if amount is None:
            return resource.release(self)
        else:
            return resource.release(self, amount)

    def consume(self, producer: Producer, amount: int = 1):
        return producer.distribute(self, amount)

    @property
    def id(self):
        return self._id

    @property
    def label(self):
        return self._label

    @property
    def priority(self):
        return self._priority

    @property
    def action(self) -> Callable:
        if self._action is not None:
            return self._action
        else:
            raise AttributeError(f"Actor {self.label} has no action defined.")

    @property
    def timeline(self):
        return self._timeline

    @property
    def time(self):
        return round(self._time, Mundus.accuracy)

    @property
    def till(self):
        return self._till

    @property
    def step(self):
        return self._step

    @property
    def status(self):
        return self._status

    @property
    def after(self):
        return self._after

    @property
    def active(self):
        return "active" in self.status

    @property
    def inactive(self):
        return "inactive" in self.status

    @property
    def onhold(self):
        return "onhold" in self.status

    @property
    def scheduled(self):
        return "scheduled" in self.status

    @property
    def completed(self):
        return "completed" in self.status

    @property
    def terminated(self):
        return "terminated" in self.status

    @property
    def followers(self):
        return self._followers
