import pygame
from utils import rotate_pivot
from math import cos, sin, radians, pi


def draw_all(screen, boat):
    draw_background(screen)
    # draw_trail(alpha_surf, boat)
    # alpha_surf.fill((255, 255, 255, 248), special_flags=pygame.BLEND_RGBA_MULT)
    # screen.blit(alpha_surf, (0, 0))
    draw_boat(screen, boat)
    draw_rudder(screen, boat)
    draw_info(screen, boat)


def draw_rudder(screen, boat):
    rudder_origin = (boat.pos_x - boat.length / 2.0 * cos(radians(boat.heading) * (-1)),
                     boat.pos_y - boat.length / 2.0 * sin(radians(boat.heading) * (-1)))
    rudder_end = (rudder_origin[0] - boat.length / 6.0 * cos((radians(boat.heading) - radians(boat.rudder)) * (-1)),
                  rudder_origin[1] - boat.length / 6.0 * sin((radians(boat.heading) - radians(boat.rudder)) * (-1)))

    pygame.draw.line(screen, 'white', rudder_origin, rudder_end, 4)


def draw_background(screen):
    width = pygame.display.Info().current_w
    height = pygame.display.Info().current_h
    img_width = 450
    img_height = 450
    water_img = pygame.image.load('assets/water_sprite.jpg')
    water_img = pygame.transform.scale(water_img, (img_width, img_height))
    i = 0
    j = 0
    # screen.fill((0, 0, 0))
    while i < width:
        while j < height:
            screen.blit(water_img, (i, j))
            j += img_height
        j = 0
        i += img_width


def draw_boat(screen, boat):
    boat_img = pygame.image.load('assets/boat_sprite.png')
    boat_img = pygame.transform.smoothscale(boat_img, (boat.length, boat.width))

    boat_img, rect = rotate_pivot(boat_img, boat.heading, (boat.pos_x, boat.pos_y))
    # pygame.draw.rect(screen, 'yellow', rect)
    screen.blit(boat_img, rect)


def draw_trail(alpha_surf, boat):
    splash_img = pygame.image.load('assets/halftrail.png')
    splash_img = pygame.transform.smoothscale(splash_img, (boat.length * 1.2, boat.width * 1.5))

    splash_img, rect = rotate_pivot(splash_img, boat.heading, (boat.pos_x, boat.pos_y))
    alpha_surf.blit(splash_img, rect)


def draw_info(screen, boat):
    font = pygame.font.SysFont("monospace", 18, bold=True)
    text = font.render("Velocity: " + str(boat.vel), True, 'white')
    text_2 = font.render("Turn: " + str(round(boat.turn, 1)), True, 'white')
    text_3 = font.render("Rudder: " + str(boat.rudder), True, 'white')
    screen.blit(text, (60, 30))
    screen.blit(text_2, (60, 50))
    screen.blit(text_3, (60, 70))
