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
    x1 = boat.pos_x
    y1 = boat.pos_y
    x2 = goal_pos[0]
    y2 = goal_pos[1]

    angle = math.atan2(y2 - y1, x2 - x1)
    angle = np.rad2deg(angle)
    angle = 360 - angle
    angle = angle % 360

    if angle > 180:
        angle = angle - 360

    target = angle - boat.heading
    target = target % 360
    if target>=180: target = target - 360

    target = -1 * target

    return target

def calculate_goal_distance(boat, goal_pos):
    x1 = boat.pos_x
    y1 = boat.pos_y
    x2 = goal_pos[0]
    y2 = goal_pos[1]

    dist = ((((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5)
    return


