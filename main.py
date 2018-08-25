# A bomb grid engine for PyGame by Cole Dieckhaus
# Meant to show off my programming skills

import pygame

from vars_constant import screen_width, screen_height, bg, fps

from map import Map

from controller import Controller

from file_io import read_startup_file


def main():
    startup_dict = read_startup_file()

    pygame.init()

    display = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption("2d Cell Engine by Cole")

    clock = pygame.time.Clock()

    simulation_map = Map(display)

    controls = Controller(startup_dict['Control Slot'])

    while True:
        controls.update()
        simulation_map.update()

        display.fill(bg)

        simulation_map.render()

        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
