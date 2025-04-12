from math import cos, pi, sin
from random import choice

from OpenGL.GL import (
    GL_QUADS,
    GL_TRIANGLE_FAN,
    glBegin,
    glColor3f,
    glEnd,
    glVertex2f,
)

from soccer.collision import (
    BoundingBox,
    Collidable,
    Collision,
    CollisionSystem,
)

SKIN_COLORS: list[tuple[float, float, float]] = [
    (0.631, 0.431, 0.294),
    (0.902, 0.737, 0.596),
    (1, 0.906, 0.82),
    (0.231, 0.133, 0.098),
]


class Player(Collidable):
    position: tuple[float, float]
    team_color: tuple[float, float, float]
    skin_color: tuple[float, float, float]
    orientation: float

    def __init__(
        self,
        pos: int,
        size: float = 10.0,
        team_color: tuple[float, float, float] = (0.02, 0.584, 0.98),
    ):
        self.position = pos
        self.size = size
        self.team_color = team_color
        self.skin_color = choice(SKIN_COLORS)

    def draw(self, orientation=0.0):
        x, y = self.position
        radius = self.size / 2
        num_segments = 20
        rect_length = 2 * self.size
        rect_width = 0.7 * self.size

        # Player shoulders
        dx = cos(orientation)
        dy = sin(orientation)
        px = -dy
        py = dx

        glColor3f(*self.team_color)
        glBegin(GL_QUADS)
        glVertex2f(
            x + dx * rect_length / 2 + px * rect_width / 2,
            y + dy * rect_length / 2 + py * rect_width / 2,
        )
        glVertex2f(
            x + dx * rect_length / 2 - px * rect_width / 2,
            y + dy * rect_length / 2 - py * rect_width / 2,
        )
        glVertex2f(
            x - dx * rect_length / 2 - px * rect_width / 2,
            y - dy * rect_length / 2 - py * rect_width / 2,
        )
        glVertex2f(
            x - dx * rect_length / 2 + px * rect_width / 2,
            y - dy * rect_length / 2 + py * rect_width / 2,
        )
        glEnd()

        # Players head
        glColor3f(*self.skin_color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for i in range(num_segments + 1):
            angle = 2 * pi * i / num_segments
            glVertex2f(x + cos(angle) * radius, y + sin(angle) * radius)
        glEnd()

    def update(self):
        # Here goes the code to make the players move
        pass

    def get_bounding_box(self) -> BoundingBox:
        return BoundingBox(
            x_min=self.position[0] - self.size // 2,
            y_min=self.position[1] - self.size // 2,
            x_max=self.position[0] + self.size // 2,
            y_max=self.position[1] + self.size // 2,
        )

    def check_collision(self, bb: BoundingBox) -> Collision:
        if CollisionSystem.aabb_collision(bb, self.get_bounding_box()):
            return Collision.PLAYER
        return Collision.NONE


def get_n_players(
    positions: list[tuple[float, float]], **kwargs
) -> list[Player]:
    return [Player(pos, **kwargs) for pos in positions]
