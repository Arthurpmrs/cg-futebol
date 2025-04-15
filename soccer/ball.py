from typing import Callable

import pygame
from OpenGL.GL import (
    GL_LINEAR,
    GL_RGB,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_UNSIGNED_BYTE,
    glBindTexture,
    glDisable,
    glEnable,
    glGenTextures,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glTexImage2D,
    glTexParameteri,
    glTranslatef,
)
from OpenGL.GLU import gluNewQuadric, gluQuadricTexture, gluSphere

from soccer.collision import BoundingBox, Collision, CollisionSystem
from soccer.field import Field
from soccer.overlay import TextOverlay
from soccer.score import Score


class Ball:
    INITIAL_POSITION = [0.0, 0.0]
    SPEED = 3.0

    def __init__(
        self,
        field: Field,
        radius: float = 10,
        texture_path: str = 'soccer/assets/ball.jpeg',
    ):
        self.position = [*self.INITIAL_POSITION]
        self.rot_angle = 0.0
        self.radius = radius
        self.texture = self.load_texture(texture_path)
        self.field = field

    @staticmethod
    def load_texture(texture_path):
        texture_surface = pygame.image.load(texture_path)
        texture_data = pygame.image.tostring(texture_surface, 'RGB', True)
        width, height = texture_surface.get_size()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            width,
            height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            texture_data,
        )

        return texture_id

    def draw(self):
        glPushMatrix()

        glTranslatef(*self.position, 0.0)
        glRotatef(self.rot_angle, 1.0, 1.0, 1.0)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, True)
        gluSphere(quadric, self.radius, 32, 16)

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    def get_bouding_box(self, pos: tuple = None) -> tuple:
        if not pos:
            pos = self.position

        return BoundingBox(
            x_min=pos[0] - self.radius,
            x_max=pos[0] + self.radius,
            y_min=pos[1] - self.radius,
            y_max=pos[1] + self.radius,
        )

    def update(
        self,
        keys: pygame.key.ScancodeWrapper,
        collision_system: CollisionSystem,
        score: Score,
        set_pause: Callable,
        overlay: TextOverlay,
    ):
        new_x, new_y = self.position
        if keys[pygame.K_LEFT]:
            new_x -= self.SPEED
            self.rot_angle -= 3
        if keys[pygame.K_RIGHT]:
            new_x += self.SPEED
            self.rot_angle += 3
        if keys[pygame.K_UP]:
            new_y += self.SPEED
            self.rot_angle += 2
        if keys[pygame.K_DOWN]:
            new_y -= self.SPEED
            self.rot_angle -= 2
        if keys[pygame.K_e]:
            self.reset_position()
            return

        bb = self.get_bouding_box((new_x, new_y))
        collision = collision_system.check_collisions(bb)
        if collision == Collision.GOAL_A:
            score.add_points('A')
            score.on_goal()
            self.position = [0.0, 0.0]
            print('GOAL FROM A')
            set_pause(3)
        elif collision == Collision.GOAL_B:
            score.add_points('B')
            score.on_goal()
            self.position = [0.0, 0.0]
            print('GOAL FROM B')
            set_pause(3)
        elif collision == Collision.NONE:
            self.position = [new_x, new_y]
        elif collision == Collision.PLAYER:
            print('BLOCKED BY PLAYER!')
        elif collision == Collision.CORNER_A_LEFT:
            self.position = [-self.field.width / 2, self.field.length / 2]
            overlay.show_text('CORNER')
            set_pause(3)
        elif collision == Collision.CORNER_A_RIGHT:
            self.position = [self.field.width / 2, self.field.length / 2]
            overlay.show_text('CORNER')
            set_pause(3)
        elif collision == Collision.CORNER_B_LEFT:
            self.position = [-self.field.width / 2, -self.field.length / 2]
            overlay.show_text('CORNER')
            set_pause(3)
        elif collision == Collision.CORNER_B_RIGHT:
            self.position = [self.field.width / 2, -self.field.length / 2]
            overlay.show_text('CORNER')
            set_pause(3)
        elif collision == Collision.LATERAL_LEFT:
            self.position = [-self.field.width / 2, new_y]
            overlay.show_text('SIDE')
            set_pause(3, reset_players=False)
        elif collision == Collision.LATERAL_RIGHT:
            overlay.show_text('SIDE')
            self.position = [self.field.width / 2, new_y]
            set_pause(3, reset_players=False)
        else:
            print('OUT!')

    def reset_position(self):
        self.position = [*self.INITIAL_POSITION]
