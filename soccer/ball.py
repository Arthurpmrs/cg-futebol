import pygame
from OpenGL.GL import glPopMatrix, glPushMatrix, glRotatef, glTranslatef
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

        glutWireSphere(10.0, 12, 8)

        glPopMatrix()

    def update(
        self,
        keys: pygame.key.ScancodeWrapper,
        collision_system: CollisionSystem,
    ):
        if keys[pygame.K_LEFT]:
            collision = collision_system.check_collisions(
                self.position[0] - self.SPEED, self.position[1]
            )
            if collision == Collision.NONE:
                self.position[0] -= self.SPEED
                self.rot_angle -= 3
        if keys[pygame.K_RIGHT]:
            collision = collision_system.check_collisions(
                self.position[0] + self.SPEED, self.position[1]
            )
            if collision == Collision.NONE:
                self.position[0] += self.SPEED
                self.rot_angle += 3
        if keys[pygame.K_UP]:
            collision = collision_system.check_collisions(
                self.position[0], self.position[1] + self.SPEED
            )
            if collision == Collision.NONE:
                self.position[1] += self.SPEED
                self.rot_angle += 3
        if keys[pygame.K_DOWN]:
            collision = collision_system.check_collisions(
                self.position[0], self.position[1] - self.SPEED
            )
            if collision == Collision.NONE:
                self.position[1] -= self.SPEED
                self.rot_angle += 3
        if keys[pygame.K_e]:
            self.reset_position()

    def reset_position(self):
        self.position = [*self.INITIAL_POSITION]
