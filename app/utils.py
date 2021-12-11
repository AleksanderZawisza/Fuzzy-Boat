import pygame


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
