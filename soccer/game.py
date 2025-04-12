import pygame
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_MODELVIEW,
    GL_PROJECTION,
    glClear,
    glClearColor,
    glLoadIdentity,
    glMatrixMode,
    glOrtho,
)
from OpenGL.GLUT import glutInit

from soccer.ball import Ball
from soccer.collision import CollisionSystem
from soccer.field import Field
from soccer.players import get_n_players


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1000, 800), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption('Futebol')

        glutInit()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-500, 500, -400, 400, -1000, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.clock = pygame.time.Clock()
        self.field = Field(size_factor=6)
        self.ball = Ball()
        self.players = get_n_players(
            positions=[
                (85.0, 70.0),
                (-85.0, 70.0),
                (180.0, 150.0),
                (0.0, 150.0),
                (-180.0, 150.0),
                (85.0, 240.0),
                (0.0, 240.0),
                (-85.0, 240.0),
            ],
            size=14.0,
        )
        self.collision_system = CollisionSystem()
        self.collision_system.add_collidable(self.field)
        for player in self.players:
            self.collision_system.add_collidable(player)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.ball.update(keys, self.collision_system)

            glClear(GL_COLOR_BUFFER_BIT)
            glClearColor(0.0, 0.65, 0.075, 1)

            self.field.draw()
            self.ball.draw()
            for player in self.players:
                player.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
