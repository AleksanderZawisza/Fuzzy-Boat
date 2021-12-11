import pygame.display
from math import pi, sin, cos, radians, copysign


class Boat:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel = 10
        self.heading = 90
        self.rudder = 0
        self.turn = 0

        self.length = 100
        self.width = 38

    def update(self):
        self.heading = self.heading % 360

        if self.rudder > 20:
            self.rudder = 20
        elif self.rudder < -20:
            self.rudder = -20

        if self.vel > 20:
            self.vel = 20
        elif self.vel < 0:
            self.vel = 0

        self.move()

        max_width = pygame.display.Info().current_w
        max_height = pygame.display.Info().current_h
        if self.pos_x > max_width:
            self.pos_x = 0
        if self.pos_x < 0:
            self.pos_x = max_width
        if self.pos_y > max_height:
            self.pos_y = 0
        if self.pos_y < 0:
            self.pos_y = max_height

    def move(self):
        self.turn += copysign(self.rudder ** 2, self.rudder) / 200

        if self.turn > 50:
            self.turn = 50
        elif self.turn < -50:
            self.turn = -50

        self.turn = self.turn * (self.vel / 200 + 0.90)

        if self.vel == 0 and abs(self.turn) < 20:
            self.turn = 0

        self.heading += self.turn / ((self.vel + 9) * 5)
        self.turn = self.turn * 0.99

        self.pos_x = self.pos_x + self.vel * cos(radians(self.heading)) / 10
        self.pos_y = self.pos_y - self.vel * sin(radians(self.heading)) / 10
