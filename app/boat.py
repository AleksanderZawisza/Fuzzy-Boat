import pygame.display
from math import sin, cos, radians, copysign


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

        max_rudder = 50
        max_vel = 40

        if self.rudder > max_rudder:
            self.rudder = max_rudder
        elif self.rudder < -max_rudder:
            self.rudder = -max_rudder

        if self.vel > max_vel:
            self.vel = max_vel
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

        self.turn = self.turn * min((self.vel / 200 + 0.90), 0.95)

        if self.vel == 0:
            self.turn = 0

        self.heading += self.turn / ((self.vel + 10) * 4)
        self.turn = self.turn * 0.95

        self.pos_x = self.pos_x + self.vel * cos(radians(self.heading)) / 10
        self.pos_y = self.pos_y - self.vel * sin(radians(self.heading)) / 10
