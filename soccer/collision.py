from abc import ABC, abstractmethod
from enum import Enum, auto


class Collision(Enum):
    NONE = auto()
    GOAL_A = auto()
    GOAL_B = auto()
    LATERAL = auto()
    CORNER_A = auto()
    CORNER_B = auto()
    PLAYER = auto()


class Collidable(ABC):
    @abstractmethod
    def check_collision(self, x: float, y: float) -> Collision: ...


class CollisionSystem:
    collidables: list[Collidable]

    def __init__(self):
        self.collidables = []

    def add_collidable(self, c: Collidable):
        self.collidables.append(c)

    def check_collisions(self, x: float, y: float) -> Collision:
        for collidable in self.collidables:
            result = collidable.check_collision(x, y)
            if result != Collision.NONE:
                return result
        return Collision.NONE
