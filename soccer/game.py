import time

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
from soccer.button import Button
from soccer.collision import CollisionSystem
from soccer.field import Field
from soccer.overlay import TextOverlay
from soccer.players import get_n_players
from soccer.score import Score


class Game:
    def __init__(self):
        self.win_width = 1000
        self.win_height = 800
        pygame.init()
        pygame.display.set_mode(
            (self.win_width, self.win_height), pygame.OPENGL | pygame.DOUBLEBUF
        )
        pygame.display.set_caption('Futebol')

        glutInit()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-500, 500, -400, 400, -1000, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.pause = 0.0
        self.clock = pygame.time.Clock()
        self.field = Field(size_factor=6)
        self.ball = Ball(field=self.field)
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

        self.button = Button(
            (-450, 240), 120, 50, 'Reset', self.on_reset_button_click
        )
        self.collision_system = CollisionSystem()
        self.collision_system.add_collidable(self.field)
        self.score = Score()
        for player in self.players:
            self.collision_system.add_collidable(player)
        self.overlay = TextOverlay()

    def convert_mouse_pos(self, mx: float, my: float):
        normalized_x = mx / self.win_width
        normalized_y = my / self.win_height

        opengl_x = -500 + normalized_x * 1000
        opengl_y = 400 - normalized_y * 800

        return opengl_x, opengl_y

    def on_reset_button_click(self):
        self.ball.reset_position()
        self.score.reset_score()

        for player in self.players:
            player.reset_position()

    def set_pause(self, t: float, reset_players: bool = True):
        self.pause = time.time() + t

        if reset_players:
            for player in self.players:
                player.reset_position()

    def run(self):
        running = True
        while running:
            # Handle forced pause. No entity should move
            if self.pause == 0.0:
                running = self._update_entities()
            elif time.time() > self.pause:
                self.pause = 0.0

            glClear(GL_COLOR_BUFFER_BIT)
            glClearColor(0.0, 0.65, 0.075, 1)

            self.field.draw()
            self.ball.draw()
            self.score.draw()
            self.score.draw_goal_text()
            for player in self.players:
                player.draw()
            self.button.draw()
            self.overlay.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def _update_entities(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = self.convert_mouse_pos(*pygame.mouse.get_pos())
                if self.button.is_clicked(mx, my):
                    self.on_reset_button_click()
            elif event.type == pygame.MOUSEMOTION:
                mx, my = self.convert_mouse_pos(*pygame.mouse.get_pos())
                self.button.update(mx, my)

        keys = pygame.key.get_pressed()
        self.ball.update(
            keys,
            self.collision_system,
            self.score,
            self.set_pause,
            self.overlay,
        )
        for player in self.players:
            player.update(*self.ball.position)

        return True
