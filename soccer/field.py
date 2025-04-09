import numpy as np
from OpenGL.GL import glPopMatrix, glPushMatrix, glRotatef

from soccer.bresenham import bresenham_circle, bresenham_line
from OpenGL.GL import glBegin, glEnd, glVertex2f, GL_TRIANGLE_FAN


class Field:
    def __init__(self, size_factor: int = 1):
        self.width = size_factor * 90.0
        self.length = size_factor * 120.0
        self.center_radius = size_factor * 14.15
        self.big_area_width = size_factor * 60
        self.big_area_length = size_factor * 40
        self.small_area_length = size_factor * 15.5
        self.small_area_width = size_factor * 27.3
        self.goal_length = size_factor * 8.5
        self.goal_width = size_factor * 18.3

    def draw(self):
        glPushMatrix()

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

        self._draw_mark(0, 0)
        self._draw_mark(0, -3 * self.small_area_length)
        self._draw_mark(0, 3 * self.small_area_length)

        glPopMatrix()

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
            dtype=np.float32
        )
        B = np.array(
            [
                self.goal_width // 2,
                self.length // 2 + self.goal_length // 2,
            ],
            dtype=np.float32
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

    def _draw_mark(self, x, y):
        CENTER = np.array([x, y], dtype=np.float32)
        radius = 5
        num_segments = 100

        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(CENTER[0], CENTER[1])
        for i in range(num_segments + 1):
            angle = 2.0 * np.pi * i / num_segments
            glVertex2f(
            CENTER[0] + (radius * np.cos(angle)),
            CENTER[1] + (radius * np.sin(angle))
            )
        glEnd()