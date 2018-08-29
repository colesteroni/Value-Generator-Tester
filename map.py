# Map creation, cell controlling and selective rendering

# Taken directly from old cell.py, fix later for ease of debugging

import pygame
from colors import *

from vars_constant import state_dict
import vars_global
# END


import pygame

import map_generator

from vars_constant import state_dict
import vars_global


class Map(object):
    def __init__(self, display, generator=None):
        self.display = display
        self.wakka = 'cool as a cucumber man'
        self.generator = generator if generator else map_generator.Generator(self)

        self.generator.generate(
            (vars_global.spectator_x - 10, vars_global.spectator_x + 10),
            (vars_global.spectator_y - 10, vars_global.spectator_y + 10)
        )

    def update(self):
        self.generator.generate(
            (int(vars_global.spectator_x / 50) - 1, int(vars_global.spectator_x / 50) + 14),
            (int(vars_global.spectator_y / 50) - 10, int(vars_global.spectator_y / 50) + 2)
        )

    def render(self, cell_list=None):
        cell_list = cell_list if cell_list else self.generator.cell_list

        for column in cell_list:
            for row in column:
                row.render()

    class Cell(object):
        size = 50

        def __init__(self, map, x, y, state=None):
            self.map = map

            self.display = map.display

            self.x = x
            self.y = y

            self.state = state if state else map_generator.get_state(x, y)

            self.size = Map.Cell.size

            self.surface = pygame.Surface((self.size, self.size))

            self.rect = self.surface.get_rect(
                center=(self.x * self.size + int(self.size / 2), self.y * self.size + int(self.size / 2))
            )

        def update(self):
            self.surface.fill(state_dict[self.state])

            self.rect = self.surface.get_rect(
                center=(
                    -1 * vars_global.spectator_x + (self.x * self.size) + int(self.size / 2),
                    vars_global.spectator_y - (self.y * self.size) + int(self.size / 2)
                )
            )

        def render(self):
            self.update()

            self.display.blit(self.surface, self.rect)
