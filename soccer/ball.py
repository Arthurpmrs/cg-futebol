import pygame
from OpenGL.GL import *
from OpenGL.GLUT import glutWireSphere

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

    def update(self, keys: pygame.key.ScancodeWrapper):
        if keys[pygame.K_LEFT]:
            self.position[0] -= self.SPEED
            self.rot_angle -= 3
        if keys[pygame.K_RIGHT]:
            self.position[0] += self.SPEED
            self.rot_angle += 3
        if keys[pygame.K_UP]:
            self.position[1] += self.SPEED
            self.rot_angle += 3
        if keys[pygame.K_DOWN]:
            self.position[1] -= self.SPEED
            self.rot_angle -= 3
        if keys[pygame.K_e]:
            self.reset_position()
    
    def reset_position(self):
        self.position = [*self.INITIAL_POSITION]