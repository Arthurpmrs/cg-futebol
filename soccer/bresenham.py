import numpy as np
from OpenGL.GL import *

def bresenham_line(A: np.ndarray, B: np.ndarray):
    """
    Draws a line between two points using adapted Bresenham's algorithm.
    Reference: https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    """
    dx = abs(A[0] - B[0])
    sx = 1 if A[0] < B[0] else -1
    dy = -abs(A[1] - B[1])
    sy = 1 if A[1] < B[1] else -1
    error = dx + dy

    x = A[0]
    y = A[1]

    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    while True:
        # print(x, y)
        glVertex2f(x, y)
        e = 2 * error
        if e >= dy:
            if x == B[0]:
                break
            error += dy
            x += sx
        
        if e <= dx:
            if y == B[1]:
                break
            error += dx
            y += sy
    glEnd()


def bresenham_circle(C: np.ndarray, r: float):
    """
    Draws a circle centered at C using Bresenham's algorithm for circles.
    Reference: https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
    """
    t1 = r / 16
    t2 = 0
    x = r
    y = 0

    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)

    while x >= y:
        _draw_simetric_points(C[0], C[1], x, y)
        y += 1
        t1 = t1 + y
        t2 = t1 - x
        if t2 >= 0:
            t1 = t2
            x -= 1

    glEnd()


def _draw_simetric_points(xc: float, yc: float, x: float, y: float):
    glVertex2f(xc + x, yc + y)
    glVertex2f(xc - x, yc + y)
    glVertex2f(xc + x, yc - y)
    glVertex2f(xc - x, yc - y)
    glVertex2f(xc + y, yc + x)
    glVertex2f(xc - y, yc + x)
    glVertex2f(xc + y, yc - x)
    glVertex2f(xc - y, yc - x)