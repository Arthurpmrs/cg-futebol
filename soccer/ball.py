import pygame
from OpenGL.GL import (
    glColor3f,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glTranslatef,
)
from OpenGL.GLUT import glutWireSphere

from soccer.collision import BoundingBox, Collision, CollisionSystem
from soccer.score import Score


class Ball:
    INITIAL_POSITION = [0.0, 0.0]
    SPEED = 2.0

    def __init__(self, radius: float = 10):
        self.position = [*self.INITIAL_POSITION]
        self.rot_angle = 0.0
        self.radius = radius

    def draw(self):
        glPushMatrix()

        glTranslatef(*self.position, 0.0)
        glRotatef(self.rot_angle, 1.0, 1.0, 1.0)
        glTranslatef(-self.position[0], -self.position[1], 0.0)
        glTranslatef(*self.position, 0.0)

        glColor3f(0, 0, 0)
        glutWireSphere(self.radius, 12, 8)

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
        elif collision == Collision.GOAL_B:
            score.add_points('B')
            score.on_goal()
            self.position = [0.0, 0.0]
            print('GOAL FROM B')
        elif collision == Collision.NONE:
            self.position = [new_x, new_y]
        elif collision == Collision.PLAYER:
            print('BLOCKED BY PLAYER!')
        else:
            print('OUT!')

    def reset_position(self):
        # Add some pause before can move the ball
        self.position = [*self.INITIAL_POSITION]
