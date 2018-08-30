# A bomb grid engine for PyGame by Cole Dieckhaus
# Meant to show off my programming skills

import pygame

from vars_constant import bg, fps


def main(display, clock, cell_map, player, controller):
    while True:
        #  Updating

        controller.update()  # invokes player.update()

        cell_map.update()

        # Display

        display.fill(bg)

        cell_map.render()

        player.render()

        pygame.display.flip()

        # Frame limiting

        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    import launcher
    launcher.launch()
