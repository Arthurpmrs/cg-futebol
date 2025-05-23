import numpy as np
import pygame
from OpenGL.GL import (
    GL_LINEAR,
    GL_QUADS,
    GL_REPEAT,
    GL_RGBA,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_TRIANGLE_FAN,
    GL_UNSIGNED_BYTE,
    glBegin,
    glBindTexture,
    glDisable,
    glEnable,
    glEnd,
    glGenTextures,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glTexCoord2f,
    glTexImage2D,
    glTexParameteri,
    glVertex2f,
    glVertex3f,
)

from soccer.bresenham import bresenham_circle, bresenham_line
from soccer.collision import (
    BoundingBox,
    Collidable,
    Collision,
    CollisionSystem,
)


class Field(Collidable):
    def __init__(
        self,
        size_factor: int = 1,
        texture_path: str = 'soccer/assets/grass3.jpg',
    ):
        self.width = size_factor * 90.0
        self.length = size_factor * 120.0
        self.center_radius = size_factor * 14.15
        self.big_area_width = size_factor * 60
        self.big_area_length = size_factor * 40
        self.small_area_length = size_factor * 15.5
        self.small_area_width = size_factor * 27.3
        self.goal_length = size_factor * 8.5
        self.goal_width = size_factor * 18.3
        self.bounding_boxes = self.get_bounding_box()
        self.texture = self.load_texture(texture_path)
        

    @staticmethod
    def load_texture(texture_path):
        texture_surface = pygame.image.load(texture_path)
        texture_data = pygame.image.tostring(texture_surface, 'RGBA', True)
        width, height = texture_surface.get_size()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            texture_data,
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        return texture_id

    def draw(self):
        glPushMatrix()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-self.width / 2, -self.length / 2, 0.0)

        glTexCoord2f(5.0, 0.0)
        glVertex3f(self.width / 2, -self.length / 2, 0.0)

        glTexCoord2f(5.0, 5.0)
        glVertex3f(self.width / 2, self.length / 2, 0.0)

        glTexCoord2f(0.0, 5.0)
        glVertex3f(-self.width / 2, self.length / 2, 0.0)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        self._draw_field()
        self._draw_center()

        self._draw_big_area()
        glRotatef(180, 1, 0, 0)
        self._draw_big_area()

        self._draw_small_area()
        glRotatef(180, 1, 0, 0)
        self._draw_small_area()

        self._draw_goal()
        glRotatef(180, 1, 0, 0)
        self._draw_goal()

        Field._draw_mark(0, 0)
        Field._draw_mark(0, -3 * self.small_area_length)
        Field._draw_mark(0, 3 * self.small_area_length)

        glPopMatrix()

    def check_collision(self, bb: BoundingBox) -> Collision:
        for section_bb, collision_type in self.bounding_boxes:
            if CollisionSystem.aabb_collision(bb, section_bb):
                return collision_type
        return Collision.NONE

    def _draw_field(self):
        A = np.array([-self.width / 2, -self.length / 2], dtype=np.float32)
        B = np.array([-self.width / 2, self.length / 2], dtype=np.float32)
        C = np.array([self.width / 2, self.length / 2], dtype=np.float32)
        D = np.array([self.width / 2, -self.length / 2], dtype=np.float32)
        E = np.array([-self.width / 2, 0.0], dtype=np.float32)
        F = np.array([self.width / 2, 0.0], dtype=np.float32)

        bresenham_line(A, B)
        bresenham_line(B, C)
        bresenham_line(C, D)
        bresenham_line(D, A)
        bresenham_line(E, F)

    def _draw_center(self):
        CENTER = np.array([0.0, 0.0], dtype=np.float32)
        bresenham_circle(CENTER, self.center_radius)

    def _draw_big_area(self):
        A = np.array(
            [
                -self.big_area_width // 2,
                self.length // 2 - self.big_area_length // 2,
            ],
            dtype=np.float32,
        )
        B = np.array(
            [
                self.big_area_width // 2,
                self.length // 2 - self.big_area_length // 2,
            ],
            dtype=np.float32,
        )
        C = np.array(
            [-self.big_area_width // 2, self.length // 2], dtype=np.float32
        )
        D = np.array(
            [self.big_area_width // 2, self.length // 2], dtype=np.float32
        )

        bresenham_line(A, C)
        bresenham_line(A, B)
        bresenham_line(B, D)

    def _draw_small_area(self):
        A = np.array(
            [
                -self.small_area_width // 2,
                self.length // 2 - self.small_area_length // 2,
            ],
            dtype=np.float32,
        )
        B = np.array(
            [
                self.small_area_width // 2,
                self.length // 2 - self.small_area_length // 2,
            ],
            dtype=np.float32,
        )
        C = np.array(
            [-self.small_area_width // 2, self.length // 2], dtype=np.float32
        )
        D = np.array(
            [self.small_area_width // 2, self.length // 2], dtype=np.float32
        )

        bresenham_line(A, C)
        bresenham_line(A, B)
        bresenham_line(B, D)

    def _draw_goal(self):
        A = np.array(
            [
                -self.goal_width // 2,
                self.length // 2 + self.goal_length // 2,
            ],
            dtype=np.float32,
        )
        B = np.array(
            [
                self.goal_width // 2,
                self.length // 2 + self.goal_length // 2,
            ],
            dtype=np.float32,
        )
        C = np.array(
            [-self.goal_width // 2, self.length // 2], dtype=np.float32
        )
        D = np.array(
            [self.goal_width // 2, self.length // 2], dtype=np.float32
        )

        bresenham_line(A, B)
        bresenham_line(A, C)
        bresenham_line(B, D)

    @staticmethod
    def _draw_mark(x, y):
        CENTER = np.array([x, y], dtype=np.float32)
        radius = 5
        num_segments = 100

        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(CENTER[0], CENTER[1])
        for i in range(num_segments + 1):
            angle = 2.0 * np.pi * i / num_segments
            glVertex2f(
                CENTER[0] + (radius * np.cos(angle)),
                CENTER[1] + (radius * np.sin(angle)),
            )
        glEnd()

    def get_bounding_box(self) -> tuple[BoundingBox, Collision]:
        tol = 25.0
        return [
            (
                BoundingBox(
                    -self.width / 2 - tol,
                    -self.length / 2 - tol,
                    -self.width / 2 - tol,
                    self.length / 2 + tol,
                ),
                Collision.LATERAL_LEFT,
            ),
            (
                BoundingBox(
                    self.width / 2 + tol,
                    -self.length / 2 - tol,
                    self.width / 2 + tol,
                    self.length / 2 + tol,
                ),
                Collision.LATERAL_RIGHT,
            ),
            (
                BoundingBox(
                    -self.width / 2 - tol,
                    self.length / 2 + tol,
                    -self.goal_width / 2,
                    self.length / 2 + tol,
                ),
                Collision.CORNER_A_LEFT,
            ),
            (
                BoundingBox(
                    self.goal_width / 2,
                    self.length / 2 + tol,
                    self.width / 2 + tol,
                    self.length / 2 + tol,
                ),
                Collision.CORNER_A_RIGHT,
            ),
            (
                BoundingBox(
                    -self.goal_width / 2,
                    self.length / 2 + tol,
                    self.goal_width / 2,
                    self.length / 2 + tol,
                ),
                Collision.GOAL_A,
            ),
            (
                # Goal Left Internal Lateral
                BoundingBox(
                    -self.goal_width / 2,
                    self.length / 2,
                    -self.goal_width / 2,
                    self.length / 2 + tol,
                ),
                Collision.GOAL_A,
            ),
            (
                # Goal Right Internal Lateral
                BoundingBox(
                    self.goal_width / 2,
                    self.length / 2,
                    self.goal_width / 2,
                    self.length / 2 + tol,
                ),
                Collision.GOAL_A,
            ),
            (
                # Goal Left External Lateral
                BoundingBox(
                    -self.goal_width / 2 - 2,
                    self.length / 2,
                    -self.goal_width / 2 - 2,
                    self.length / 2 + tol,
                ),
                Collision.CORNER_A_LEFT,
            ),
            (
                # Goal Right External Lateral
                BoundingBox(
                    self.goal_width / 2 + 2,
                    self.length / 2,
                    self.goal_width / 2 + 2,
                    self.length / 2 + tol,
                ),
                Collision.CORNER_A_RIGHT,
            ),
            (
                BoundingBox(
                    -self.width / 2 - tol,
                    -self.length / 2 - tol,
                    -self.goal_width / 2,
                    -self.length / 2 - tol,
                ),
                Collision.CORNER_B_LEFT,
            ),
            (
                BoundingBox(
                    self.goal_width / 2,
                    -self.length / 2 - tol,
                    self.width / 2 + tol,
                    -self.length / 2 - tol,
                ),
                Collision.CORNER_B_RIGHT,
            ),
            (
                BoundingBox(
                    -self.goal_width / 2,
                    -self.length / 2 - tol,
                    self.goal_width / 2,
                    -self.length / 2 - tol,
                ),
                Collision.GOAL_B,
            ),
            (
                # Goal Left Internal Lateral
                BoundingBox(
                    -self.goal_width / 2,
                    -self.length / 2 - tol,
                    -self.goal_width / 2,
                    -self.length / 2,
                ),
                Collision.GOAL_B,
            ),
            (
                # Goal Right Internal Lateral
                BoundingBox(
                    self.goal_width / 2,
                    -self.length / 2 - tol,
                    self.goal_width / 2,
                    -self.length / 2,
                ),
                Collision.GOAL_B,
            ),
            (
                # Goal Left External Lateral
                BoundingBox(
                    -self.goal_width / 2 - 2,
                    -self.length / 2 - tol,
                    -self.goal_width / 2 - 2,
                    -self.length / 2,
                ),
                Collision.CORNER_B_LEFT,
            ),
            (
                # Goal Right External Lateral
                BoundingBox(
                    self.goal_width / 2 + 2,
                    -self.length / 2 - tol,
                    self.goal_width / 2 + 2,
                    -self.length / 2,
                ),
                Collision.CORNER_A_RIGHT,
            ),
        ]
