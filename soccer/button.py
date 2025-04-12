from typing import Callable

from OpenGL.GL import (
    GL_LINE_LOOP,
    GL_QUADS,
    glBegin,
    glColor3f,
    glEnd,
    glLineWidth,
    glPopMatrix,
    glPushMatrix,
    glRasterPos2f,
    glVertex2f,
)
from OpenGL.GLUT import GLUT_BITMAP_9_BY_15, glutBitmapCharacter


class Button:
    def __init__(
        self,
        pos: tuple[float, float],
        width: float,
        height: float,
        text: str,
        callback: Callable,
    ):
        self.position = pos
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback
        self.color = (0.098, 0.541, 0.851)
        self.hover_color = (0.286, 0.694, 0.98)
        self.text_color = (1.0, 1.0, 1.0)
        self.is_hovered = False

    def draw(self):
        x, y = self.position
        if self.is_hovered:
            glColor3f(*self.hover_color)
        else:
            glColor3f(*self.color)

        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + self.width, y)
        glVertex2f(x + self.width, y + self.height)
        glVertex2f(x, y + self.height)
        glEnd()

        # Button border
        glColor3f(0.2, 0.2, 0.2)
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + self.width, y)
        glVertex2f(x + self.width, y + self.height)
        glVertex2f(x, y + self.height)
        glEnd()

        self.draw_text()

    def draw_text(self):
        x, y = self.position
        text_x = x + self.width / 2
        text_y = y + self.height / 2

        glColor3f(*self.text_color)
        glPushMatrix()
        glRasterPos2f(text_x - len(self.text) * 4.5, text_y - 5)

        for char in self.text:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

        glPopMatrix()

    def update(self, mx: float, my: float):
        self.is_hovered = self._is_point_inside(mx, my)

    def is_clicked(self, x, y):
        return self._is_point_inside(x, y)

    def on_click(self):
        if self.callback:
            self.callback()

    def _is_point_inside(self, x: float, y: float):
        btn_x, btn_y = self.position
        return (
            btn_x <= x <= btn_x + self.width
            and btn_y <= y <= btn_y + self.height
        )
