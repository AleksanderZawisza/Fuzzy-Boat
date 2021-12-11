import pygame
import numpy as np
import math


def handle_keystroke_event(event, boat):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            boat.rudder += 2
        if event.key == pygame.K_RIGHT:
            boat.rudder += -2
        if event.key == pygame.K_UP:
            boat.vel += 1
        if event.key == pygame.K_DOWN:
            boat.vel += -1


def rotate_pivot(img, angle, pivot):
    # rotate image around the pivot
    image = pygame.transform.rotate(img, angle)
    rect = image.get_rect()
    rect.center = pivot
    return image, rect


def calculate_goal_angle(boat, goal_pos):
    x1 = math.cos(np.deg2rad(boat.heading)+np.pi)
    y1 = math.sin(np.deg2rad(boat.heading)+np.pi)
    x2, y2 = (goal_pos[0]-boat.pos_x, goal_pos[1]-boat.pos_y)

    dot = x1 * x2 + y1 * y2  # dot product
    det = x1 * y2 - y1 * x2  # determinant
    angle = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    angle = np.rad2deg(angle)
    if angle<0: angle += 360
    angle = 360-angle

    return angle


