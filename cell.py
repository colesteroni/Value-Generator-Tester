# Cell object

import pygame
from colors import *

from vars_constant import state_dict
import vars_global


class Cell(object):
    def __init__(self, display, x, y):
        self.display = display

        self.x = x
        self.y = y

        self.state = 0

        self.size = 50

        self.surface = pygame.Surface((self.size, self.size))

        self.rect = self.surface.get_rect(center=(self.x * self.size + int(self.size / 2), self.y * self.size + int(self.size / 2)))

    def update(self):
        self.state = (4, 6)[(self.x + self.y) % 2]

        self.surface.fill(state_dict[self.state])

        self.rect = self.surface.get_rect(
            center=(
                vars_global.spectator_x - (self.x * self.size) + int(self.size / 2),
                vars_global.spectator_y - (self.y * self.size) + int(self.size / 2)
            )
        )

    def render(self):
        self.update()

        self.display.blit(self.surface, self.rect)
