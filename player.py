# The player/spectator

from pygame import Surface

import colors

from vars_constant import screen_width, screen_height
import vars_global

import time


class Player(object):
    def __init__(self, cell_map):
        self.cell_map = cell_map

        self.display = self.cell_map.display

        self.size = 25

        self.x = screen_width / 2
        self.y = screen_height / 2

        self.surface = Surface((self.size, self.size))
        self.surface.fill(colors.red)

        self.rect = self.surface.get_rect(
            center=(self.x, self.y)
        )

        self.last_log_time = int(round(time.time() * 1000))

    def update(self, buttons_held):
        speed = vars_global.spectator_speed

        if buttons_held['Left']:
            vars_global.spectator_x -= speed
        if buttons_held['Right']:
            vars_global.spectator_x += speed
        if buttons_held['Up']:
            vars_global.spectator_y += speed
        if buttons_held['Down']:
            vars_global.spectator_y -= speed

        self.surface.fill(colors.light_green)

        self.rect = self.surface.get_rect(center=(self.x, self.y))

    def render(self):
        self.display.blit(self.surface, self.rect)
