# A bomb grid engine for PyGame by Cole Dieckhaus
# Meant to show off my programming skills

import launcher

import pygame

from vars_constant import bg, fps


def main(display, clock, map, controller):
    if not controller.control_dictionary: return "Failed to load control dictionary"

    while True:
        #  Updating

        controller.update()

        map.update()

        # Display

        display.fill(bg)

        map.render()

        pygame.display.flip()

        # Clock tick

        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    launcher.launch()
