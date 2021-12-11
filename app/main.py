import pygame
from drawing import draw_all
from boat import Boat
from utils import handle_keystroke_event


def main_loop():
    run = True

    pygame.init()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(100)
    size = (1024, 768)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # Blit objects with trails onto this surface instead of the screen.
    alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    info = pygame.display.Info()
    # print(info)
    boat = Boat(info.current_w / 2, info.current_h / 2)

    while run:
        boat.update()
        draw_all(screen, boat, alpha_surf)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            handle_keystroke_event(event, boat)

        pygame.display.update()
        clock.tick(100)

    pygame.quit()


if __name__ == "__main__":
    main_loop()
