# Map creation, cell controlling and selective rendering

import pygame

import generators

from vars_constant import state_dict, screen_width, screen_height
import vars_global


class Map(object):
    def __init__(self, display=None, gen_slot="Demo"):
        self.gen_slot = gen_slot

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
                int(vars_global.spectator_y / 50) - int(screen_height / self.Cell.size),
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

            self.gen_slot = cell_map.gen_slot

            self.x = x
            self.y = y

            self.state = state if state else self.cell_map.generator.get_state(x, y)

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

            self.gen_slot = cell_map.gen_slot

            self.cell_list = []

            generators.generator_dict[self.gen_slot].seed_interpreter(seed)

            print(
                "Generated pivotal lengths - x: " + str(vars_global.x_section_length) + " y: " + str(vars_global.y_section_length)
            )

        def get_state(self, x=None, y=None, cell=None):
            if x is None:
                x = cell.x

            if y is None:
                y = cell.y

            if not x % vars_global.x_pivotal_gap and not y % vars_global.y_pivotal_gap:  # is pivotal block
                xx = x / vars_global.x_pivotal_gap
                yy = y / vars_global.y_pivotal_gap

                state = generators.generator_dict[self.gen_slot].pivotal_state(xx, yy)

            else:  # is filler block
                state = generators.generator_dict[self.gen_slot].filler_chooser(x, y)

            return state

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
