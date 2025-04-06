import pygame
from OpenGL.GL import *
from OpenGL.GLUT import glutInit
from soccer.ball import Ball
from soccer.field import Field

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1000, 800), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Futebol")

        glutInit()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-500, 500, -400, 400, -1000, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.clock = pygame.time.Clock()
        self.field = Field(size_factor=6)
        self.ball = Ball()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.ball.update(keys)

            glClear(GL_COLOR_BUFFER_BIT)
            self.field.draw()
            self.ball.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
