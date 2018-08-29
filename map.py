# Map creation, cell controlling and selective rendering

# Taken directly from old cell.py, fix later for ease of debugging
import pygame
from colors import *

from vars_constant import state_dict
import vars_global
# END

# Taken directly from map_generator.py
import map

from vars_constant import section_l
import vars_global

from math import sin
import random
# END

import pygame

import map_generator

from vars_constant import state_dict
import vars_global


class Map(object):
    def __init__(self, display=None):
        self.display = display

        self.generator = self.Generator(self)

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

    class Generator(object):
        def __init__(self, map, seed="3232"):
            self.map = map

            self.display = map.display

            self.cell_list = []

            def set_by_dict(key, digit, value):
                if type(value) is not int:
                    value = int("0x" + value, 0) * (1 if digit == 1 else ((digit - 1) * 16))

                if key is 'x_mod':
                    vars_global.x_length += value
                elif key is 'y_mod':
                    vars_global.y_length += value

            seed_dict = {
                0: (lambda value: set_by_dict('y_mod', 1, value)),
                1: (lambda value: set_by_dict('y_mod', 2, value)),
                2: (lambda value: set_by_dict('x_mod', 1, value)),
                3: (lambda value: set_by_dict('x_mod', 2, value))
            }

            self.seed = seed[::-1].upper()

            for n in range(0, len(self.seed)):
                seed_dict[n](self.seed[n])

            if len(seed) < len(seed_dict):
                for i in range(len(seed_dict) - len(seed), len(seed_dict)):
                    seed_dict[n](random.randint(0, 15))

            # Ensure hard requirements met
            if vars_global.x_length < 40: vars_global.x_length = 40

            if vars_global.y_length < 40: vars_global.y_length = 40

        def generate(self, range_x, range_y):
            for x in range(-vars_global.x_length, vars_global.x_length):
                for y in range(-vars_global.y_length, vars_global.y_length):
                    if (x, y) not in vars_global.pivotals_cached:
                        vars_global.pivotals_cached.add((x, y))
                        vars_global.pivotal_cache.append(map.Map.Cell(self.map, x, y))

            cell_list = [
                [map.Map.Cell(self.map, x, y) for y in range(range_y[0], range_y[1])]
                for x in range(range_x[0], range_x[1])
            ]

            self.cell_list = cell_list
