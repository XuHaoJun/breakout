#!/usr/bin/python

# -*- coding: utf-8 -*-


import sys
import pygame
from pygame.locals import *

pygame.init()

surface = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

pygame.display.set_caption("Breakout!")

game_over = False

class Point(object):
    __slots__ = ('x', 'y')  # Coordinates
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __setattr__(self, attr, value):
        object.__setattr__(self, attr, float(value))
    def __getitem__(self, index):
        return self.__getattribute__(self.__slots__[index])
    def __setitem__(self, index, value):
        self.__setattr__(self.__slots__[index], value)  # converted to float automatically by __setattr__

class Geometry:
    def __init__(self):
        self.visible = True

    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

    def update(self, delta):
        if self.visible == False:
            return

        self.draw()
        vdelta_x = delta / 1000.0 * self.velocity.x
        vdelta_y = delta / 1000.0 * self.velocity.y
        self.position = [self.position[0]+vdelta_x,
                         self.position[1]+vdelta_y]


class Circle(Geometry):
    def __init__(self, position, radius):
        Geometry.__init__(self)
        self.velocity = Point(0, 0)
        self.position = position
        self.radius = radius
        self.color = (0, 255, 0)

    def draw(self):
        self.position = [int(self.position[0]), int(self.position[1])]
        pygame.draw.circle(surface,
                           self.color,
                           self.position, 10)

class Rectangle(Geometry):
    def __init__(self, position, width, height):
        Geometry.__init__(self)
        self.velocity = Point(0, 0)
        self.position = position
        self.width = width
        self.height = height
        self.color = (255, 255, 255)

    def draw(self):
        pygame.draw.rect(surface,
                         self.color,
                         self.position+[self.width, self.height])

class Overlap:
    def intersects(self, circle, rect):
        if not (circle.visible and rect.visible):
            return False
        circleDistance_x = abs(circle.x() - rect.x());
        circleDistance_y = abs(circle.y() - rect.y());

        if (circleDistance_x > (rect.width/2 + circle.radius)):
            return False

        if (circleDistance_y > (rect.height/2 + circle.radius)):
            return False

        if (circleDistance_x <= (rect.width/2)):
            return True

        if (circleDistance_y <= (rect.height/2)):
            return True

        cornerDistance_sq = pow((circleDistance_x - rect.width/2),2) + pow((circleDistance_y - (rect.height/2)),2)

        return (cornerDistance_sq <= (pow(circle.radius, 2)));




overlap = Overlap()
plank = Rectangle([640/2-45, 430],90, 20)

ball = Circle([320, 400], 20)
ball.velocity.y = -150
ball.velocity.x = -20

bricks = (Rectangle([90, 90], 20, 20),
          Rectangle([120, 90], 20, 20),
          Rectangle([150, 90], 20, 20),
          Rectangle([180, 90], 20, 20),)

game_objects = (plank, ball) + bricks



def update():
    for obj in game_objects:
        obj.update(1000.0 / clock.get_fps())

    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True
            return
        elif event.type == KEYDOWN and event.key == K_q:
            sys.exit()

    key = pygame.key.get_pressed()
    if key[K_l]:
        plank.velocity.x = 150
    elif key[K_h]:
        plank.velocity.x = -150
    else :
        plank.velocity.x = 0

    for brick in bricks:
        if overlap.intersects(ball, brick) :
            brick.visible = False
            ball.velocity.x = -ball.velocity.x
            ball.velocity.y = -ball.velocity.y

    if overlap.intersects(ball, plank) :
        # ball.velocity.x = -ball.velocity.x
        ball.velocity.y = -ball.velocity.y

    if ball.x()-ball.radius > 640:
        ball.position[0] = 639
        ball.velocity.x = -ball.velocity.x
    elif ball.x()+ball.radius < 0:
        ball.position[0] = 1
        ball.velocity.x = -ball.velocity.x

    if ball.y()-ball.radius > 480:
        ball.position[1] = 479
        ball.velocity.y = -ball.velocity.y
    elif ball.y()+ball.radius < 0:
        ball.position[1] = 1
        ball.velocity.y = -ball.velocity.y

    pygame.display.flip()


def game_loop():
    while (not game_over):
        clock.tick(50)
        surface.fill([0, 0, 0])
        if clock.get_fps() != 0:
            update()

    pygame.quit()

if __name__ == '__main__':
    game_loop()
