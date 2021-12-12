import pygame
from drawing import draw_all, draw_goal
from boat import Boat
from utils import handle_keystroke_event, calculate_goal_angle, calculate_goal_distance, adjust_velocity
from driver import BoatDriver


def main_loop():
    run = True

    pygame.init()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200)
    size = (1024, 768)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    info = pygame.display.Info()
    # print(info)
    boat = Boat(info.current_w / 2, info.current_h / 2)
    goal_pos = None
    goal_angle = None
    manual_goal_pos = None
    driver = BoatDriver()

    while run:
        boat.update()
        draw_all(screen, boat, goal_pos, goal_angle, manual_goal_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            handle_keystroke_event(event, boat)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    goal_pos = pygame.mouse.get_pos()
                    manual_goal_pos = None
                if event.button == 3:  # right click
                    goal_pos = None
                    goal_angle = None
                    manual_goal_pos = None
                if event.button == 2:  # middle click
                    goal_pos = None
                    manual_goal_pos = pygame.mouse.get_pos()

        if goal_pos:
            goal_angle = calculate_goal_angle(boat, goal_pos)
            dist = calculate_goal_distance(boat, goal_pos)
            adjust_velocity(boat, dist, goal_angle)
            change = driver.rudder_change(goal_angle, -1 * boat.turn)
            boat.rudder -= max(min(change, 2), -2)  # plynnejsze obracanie sie steru

        pygame.display.update()
        clock.tick(100)

    pygame.quit()


if __name__ == "__main__":
    main_loop()
