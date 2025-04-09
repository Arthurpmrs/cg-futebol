import numpy as np
from OpenGL.GL import glPopMatrix, glPushMatrix, glRotatef

from soccer.bresenham import bresenham_circle, bresenham_line
from soccer.collision import Collidable, Collision


class Field(Collidable):
    def __init__(self, size_factor: int = 1):
        self.width = size_factor * 90.0
        self.length = size_factor * 120.0
        self.center_radius = size_factor * 9.15
        self.big_area_width = size_factor * 50
        self.big_area_length = size_factor * 40
        self.small_area_length = size_factor * 5.5
        self.small_area_width = size_factor * 18.3
        self.goal_length = size_factor * 2.4
        self.goal_width = size_factor * 7.3

    def draw(self):
        glPushMatrix()

        self._draw_field()
        self._draw_center()
        self._draw_big_area()

        glRotatef(180, 1, 0, 0)
        self._draw_big_area()

        glPopMatrix()

    def check_collision(self, x: float, y: float) -> Collision:
        if y >= -self.length / 2 and y <= self.length / 2:
            if x < -self.width / 2 or x > self.width / 2:
                return Collision.LATERAL
        if y < -self.length / 2:
            if x > -self.goal_width / 2 and x < self.goal_width / 2:
                return Collision.GOAL_B
            else:
                return Collision.CORNER_B
        if y > self.length / 2:
            if x > -self.goal_width / 2 and x < self.goal_width / 2:
                return Collision.GOAL_A
            else:
                return Collision.CORNER_A
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
