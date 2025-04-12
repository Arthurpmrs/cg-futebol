import math
import time

from OpenGL.GL import (
    glColor3f,
    glPopMatrix,
    glPushMatrix,
    glRasterPos2f,
    glScalef,
    glTranslatef,
)
from OpenGL.GLUT import (
    GLUT_BITMAP_HELVETICA_18,
    GLUT_STROKE_ROMAN,
    glutBitmapCharacter,
    glutStrokeCharacter,
)


class Score:
    scoreA: int
    scoreB: int
    goal_start_time: int
    goal_timer: int
    show_goal_text: bool

    def __init__(self):
        self.scoreA = 0
        self.scoreB = 0
        self.goal_timer = 0
        self.goal_start_timer = 0
        self.show_goal_text = False

    def add_points(self, team):
        if team == 'A':
            self.scoreA += 1
        elif team == 'B':
            self.scoreB += 1

    def draw(self):
        string = (
            'Team A   '
            + str(self.scoreA)
            + '   |   Team B   '
            + str(self.scoreB)
        )
        string = string.encode()

        glColor3f(1, 1, 1)
        glRasterPos2f(-500, 320)
        for c in string:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)

    def on_goal(self):
        self.show_goal_text = True
        self.goal_timer = 250
        self.goal_start_time = time.time()

    def draw_goal_text(self):
        if self.show_goal_text:
            elapsed = time.time() - self.goal_start_time
            text = 'GOOOOL!'
            glPushMatrix()
            glTranslatef(-130, 0, 0)
            glColor3f(1, 1, 0)

            for i, c in enumerate(text):
                char_elapsed = elapsed - (i * 0.1)
                scale = 1.0 + 0.3 * math.sin(
                    char_elapsed * 5
                )

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

            self.goal_timer -= 1
            if self.goal_timer <= 0:
                self.show_goal_text = False
