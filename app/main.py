import pygame
from drawing import draw_all, draw_goal
from boat import Boat
from utils import handle_keystroke_event, calculate_goal_angle, calculate_goal_distance, adjust_velocity
from driver import BoatDriver


def main_loop():
    run = True

    pygame.init()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(100)
    size = (1024, 768)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    info = pygame.display.Info()
    # print(info)
    boat = Boat(info.current_w / 2, info.current_h / 2)
    goal_pos = None
    goal_angle = None
    driver = BoatDriver()

    while run:
        boat.update()
        draw_all(screen, boat, goal_pos, goal_angle)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            handle_keystroke_event(event, boat)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left click
                    goal_pos = pygame.mouse.get_pos()
                if event.button == 3:  # right click
                    goal_pos = None
                    goal_angle = None

        if goal_pos:
            goal_angle = calculate_goal_angle(boat, goal_pos)
            dist = calculate_goal_distance(boat, goal_pos)
            adjust_velocity(boat, dist)
            change = driver.rudder_change(goal_angle, -1 * boat.turn)
            boat.rudder -= change

        pygame.display.update()
        clock.tick(100)

    pygame.quit()


if __name__ == "__main__":
    main_loop()
