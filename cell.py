# Cell object

import pygame
from colors import *

from vars_constant import state_dict
import vars_global

import map_generator


class Cell(object):
    size = 50

    def __init__(self, display, x, y, state=None):
        self.display = display

        self.x = x
        self.y = y

        self.state = state if state else map_generator.get_state(x, y)

        self.size = Cell.size

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
