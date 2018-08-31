# Map creation, cell controlling and selective rendering

import pygame

import map_generator

from vars_constant import state_dict, screen_width, screen_height
import vars_global

from seed import generate_seed


class Map(object):
    def __init__(self, display=None):
        self.display = display

        self.pivotals_cached = set(())
        self.pivotal_cache = []

        self.generator = self.Generator(self)

        self.generator.generate(
            (vars_global.spectator_x - 10, vars_global.spectator_x + 10),
            (vars_global.spectator_y - 10, vars_global.spectator_y + 10)
        )

    def update(self):
        self.generator.generate(
            (
                int(vars_global.spectator_x / 50) - 1,
                int(vars_global.spectator_x / 50) + int(screen_width / self.Cell.size) + 2
            ),
            (
                int(vars_global.spectator_y / 50) - 10,
                int(vars_global.spectator_y / 50) + 2
            )
        )

    def render(self, cell_list=None):
        cell_list = cell_list if cell_list else self.generator.cell_list

        for column in cell_list:
            for row in column:
                row.render()

    class Cell(object):
        size = 50

        def __init__(self, cell_map, x, y, state=None):
            self.cell_map = cell_map

            self.display = self.cell_map.display

            self.x = x
            self.y = y

            self.state = state if state else map_generator.get_state(x, y)

            self.size = self.cell_map.Cell.size

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
        def __init__(self, cell_map, seed="0A0A"):
            self.cell_map = cell_map

            self.cell_list = []

            def set_by_dict(key, digit, value):
                if type(value) is not int:
                    value = int("0x" + value, 0) * (1 if digit == 1 else ((digit - 1) * 16))

                if key is 'x_mod':
                    vars_global.x_pivotal_gap += value
                elif key is 'y_mod':
                    vars_global.y_pivotal_gap += value

            seed_dict = {
                0: (lambda value: set_by_dict('y_mod', 1, value)),
                1: (lambda value: set_by_dict('y_mod', 2, value)),
                2: (lambda value: set_by_dict('x_mod', 1, value)),
                3: (lambda value: set_by_dict('x_mod', 2, value))
            }

            self.seed = seed[::-1].upper()

            if len(seed) < len(seed_dict):
                self.seed += generate_seed(len(seed_dict) - len(seed))

            for n in range(0, len(self.seed)):
                seed_dict[n](self.seed[n])

            # Ensure hard requirements met
            if vars_global.x_pivotal_gap < 10: vars_global.x_pivotal_gap = 10

            if vars_global.y_pivotal_gap < 10: vars_global.y_pivotal_gap = 10

            if vars_global.x_pivotal_gap > 40: vars_global.x_pivotal_gap = 40

            if vars_global.y_pivotal_gap > 40: vars_global.y_pivotal_gap = 40

            print(
                "Generated pivotal lengths - x: " + str(vars_global.x_section_length) + " y: " + str(vars_global.y_section_length)
            )

        def generate(self, range_x, range_y):
            for x in range(-vars_global.x_pivotal_gap, vars_global.x_pivotal_gap):
                for y in range(-vars_global.y_pivotal_gap, vars_global.y_pivotal_gap):
                    if (x, y) not in self.cell_map.pivotals_cached:
                        self.cell_map.pivotals_cached.add((x, y))
                        self.cell_map.pivotal_cache.append(self.cell_map.Cell(self.cell_map, x, y))

            cell_list = [
                [self.cell_map.Cell(self.cell_map, x, y) for y in range(range_y[0], range_y[1])]
                for x in range(range_x[0], range_x[1])
            ]

            self.cell_list = cell_list
