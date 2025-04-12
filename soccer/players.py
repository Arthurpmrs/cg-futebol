from OpenGL.GL import (
    GL_POLYGON,
    GL_QUADS,
    GL_TRIANGLES,
    glBegin,
    glColor3f,
    glEnd,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glTranslatef,
    glVertex2f,
)
from OpenGL.GLUT import glutWireSphere

from soccer.bresenham import bresenham_circle
from soccer.collision import (
    BoundingBox,
    Collidable,
    Collision,
    CollisionSystem,
)


class Player(Collidable):
    position: tuple[float, float]

    def __init__(self, pos: int, size: float = 10.0):
        self.position = pos
        self.side = size

    def draw(self):
        glPushMatrix()

        # glTranslatef(*self.position, 0.0)
        # glRotatef(self.rot_angle, 1.0, 1.0, 1.0)
        # glTranslatef(-self.position[0], -self.position[1], 0.0)
        # glTranslatef(*self.position, 0.0)

        # glColor3f(0.5, 0.5, 0.5)
        bresenham_circle(self.position, 5.0)
        glBegin(GL_QUADS)
        glVertex2f(self.position[0] + 8, self.position[1] + 3)
        glVertex2f(self.position[0] + 8, self.position[1] - 3)
        glVertex2f(self.position[0] - 8, self.position[1] + 3)
        glVertex2f(self.position[0] - 8, self.position[1] - 3)
        glEnd()

        glPopMatrix()

    def update(self):
        # Here goes the code to make the players move
        pass

    def get_bounding_box(self) -> BoundingBox:
        return BoundingBox(
            x_min=self.position[0] - self.size // 2,
            y_min=self.position[0] - self.size // 2,
            x_max=self.position[1] + self.size // 2,
            y_max=self.position[1] + self.size // 2,
        )

    def check_collision(self, bb: BoundingBox) -> Collision:
        if CollisionSystem.aabb_collision(bb, self.get_bounding_box()):
            return Collision.PLAYER
        return Collision.NONE


def get_n_players(positions: list[tuple[float, float]]) -> list[Player]:
    return [Player(pos) for pos in positions]
