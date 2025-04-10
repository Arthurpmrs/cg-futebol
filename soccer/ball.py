import pygame
from OpenGL.GL import (
    glColor3f,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glTranslatef,
)
from OpenGL.GLUT import glutWireSphere

from soccer.collision import Collision, CollisionSystem


class Ball:
    INITIAL_POSITION = [0.0, 0.0]
    SPEED = 2.0

    def __init__(self):
        self.position = [*self.INITIAL_POSITION]
        self.rot_angle = 0.0

    def draw(self):
        glPushMatrix()

        glTranslatef(*self.position, 0.0)
        glRotatef(self.rot_angle, 1.0, 1.0, 1.0)
        glTranslatef(-self.position[0], -self.position[1], 0.0)
        glTranslatef(*self.position, 0.0)

        glColor3f(0, 0, 0)
        glutWireSphere(10.0, 12, 8)

        glPopMatrix()

    def update(
        self,
        keys: pygame.key.ScancodeWrapper,
        collision_system: CollisionSystem,
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

        collision = collision_system.check_collisions(new_x, new_y)
        if collision == Collision.GOAL_A:
            # Add here the goal rendering text and mode
            # Add here the score board increase for team A
            self.position = [0.0, 0.0]
            print('GOAL FROM A')
        elif collision == Collision.GOAL_B:
            # Add here the goal rendering text and mode
            # Add here the score board increase for team B
            self.position = [0.0, 0.0]
            print('GOAL FROM B')
        elif collision == Collision.NONE:
            self.position = [new_x, new_y]
        elif collision == Collision.PLAYER:
            print('BLOCKED BY PLAYER!')
        else:
            print('OUT!')

    def reset_position(self):
        self.position = [*self.INITIAL_POSITION]
