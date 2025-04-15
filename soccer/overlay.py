import math
import time

from OpenGL.GL import (
    glColor3f,
    glPopMatrix,
    glPushMatrix,
    glScalef,
    glTranslatef,
)
from OpenGL.GLUT import (
    GLUT_STROKE_ROMAN,
    glutStrokeCharacter,
)


class TextOverlay:
    def __init__(self):
        self.show = False
        self.text = ''
        self.start_time = 0.0
        self.timer = 0

    def show_text(self, text: str):
        self.text = text
        self.show = True
        self.timer = 150
        self.start_time = time.time()

    def draw(self):
        if self.show:
            elapsed = time.time() - self.start_time
            glPushMatrix()
            glTranslatef(-130, 0, 0)
            glColor3f(1, 1, 0)

            for i, c in enumerate(self.text):
                char_elapsed = elapsed - (i * 0.1)
                scale = 1.0 + 0.3 * math.sin(char_elapsed * 5)

                glPushMatrix()
                glTranslatef(i * 40, 0, 0)
                glScalef(scale * 0.6, scale * 0.6, 1)

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        glPushMatrix()
                        glTranslatef(dx * 1, dy * 1, 0)
                        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
                        glPopMatrix()

                glPopMatrix()

            glPopMatrix()

            self.timer -= 1
            if self.timer <= 0:
                self.show = False
