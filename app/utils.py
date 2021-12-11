import pygame
import numpy as np


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
    v1 = [1, 0]
    v2 = [goal_pos[0]-boat.pos_x, goal_pos[1]-boat.pos_y]

    unit_vector_1 = v1 / np.linalg.norm(v1)
    unit_vector_2 = v2 / np.linalg.norm(v2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    angle = angle - boat.heading
    return angle


