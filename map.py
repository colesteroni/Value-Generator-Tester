# Map creation, cell controlling and selective rendering

import pygame

import generators

from vars_constant import state_dict
import vars_global


class Map(object):
    def __init__(self, display=None, gen_slot="Demo"):
        self.gen_slot = gen_slot

        self.display = display

        self.generator = self.Generator(self)

    def update(self):
        self.generator.generate()

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

            generators.generator_dict[self.gen_slot].seed_interpreter(
                seed, generators.generator_dict[self.gen_slot].var_dict
            )

        def get_state(self, x=None, y=None, cell=None):
            if x is None:
                x = cell.x

            if y is None:
                y = cell.y

            return generators.generator_dict[self.gen_slot].get_state(
                x, y, generators.generator_dict[self.gen_slot].var_dict
            )

        def generate(self):
            self.cell_list = generators.generator_dict[self.gen_slot].base_gen(
                self.cell_map, generators.generator_dict[self.gen_slot].var_dict
            )

