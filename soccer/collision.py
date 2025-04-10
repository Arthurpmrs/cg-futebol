from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto


class Collision(Enum):
    NONE = auto()
    GOAL_A = auto()
    GOAL_B = auto()
    LATERAL_LEFT = auto()
    LATERAL_RIGHT = auto()
    CORNER_A_LEFT = auto()
    CORNER_A_RIGHT = auto()
    CORNER_B_LEFT = auto()
    CORNER_B_RIGHT = auto()
    PLAYER = auto()


@dataclass
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float


class Collidable(ABC):
    @abstractmethod
    def check_collision(self, bb: BoundingBox) -> Collision: ...

    @abstractmethod
    def get_bounding_box(self) -> BoundingBox: ...


class CollisionSystem:
    collidables: list[Collidable]

    def __init__(self):
        self.collidables = []

    def add_collidable(self, c: Collidable):
        self.collidables.append(c)

    def check_collisions(self, bb: BoundingBox) -> Collision:
        for collidable in self.collidables:
            result = collidable.check_collision(bb)
            if result != Collision.NONE:
                return result
        return Collision.NONE

    @staticmethod
    def aabb_collision(a: BoundingBox, b: BoundingBox) -> bool:
        return not (
            a.x_max < b.x_min
            or a.x_min > b.x_max
            or a.y_max < b.y_min
            or a.y_min > b.y_max
        )
