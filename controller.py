# Object to handle keyboard controls

import sys  # sys.exit()
import pygame

import vars_global

from file_io import access_control_dict

from map import Map

from math import floor

import time


default_control_scheme = {'Left': pygame.K_a, 'Right': pygame.K_d, 'Up': pygame.K_w, 'Down': pygame.K_s}


class Controller(object):
    def __init__(self, slot, player=None):
        self.slot = slot

        self.player = player

        self.control_scheme = access_control_dict(self.slot)

        if not self.control_scheme:
            print("Loading default control scheme")
            self.control_scheme = default_control_scheme

        self.buttons_held = {'Mouse Left': False, 'Left': False, 'Right': False, 'Up': False, 'Down': False}

        self.last_log_time = int(round(time.time() * 1000))

    def update_control_dictionary(self):
        return access_control_dict(self.slot, control_dictionary=self.control_scheme)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    self.buttons_held['Mouse Left'] = True

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = pygame.mouse.get_pressed()
                if not mouse_pressed[0]:
                    self.buttons_held['Mouse Left'] = False

            if event.type == pygame.KEYDOWN:
                if event.key == self.control_scheme['Left']:
                    self.buttons_held['Left'] = True
                if event.key == self.control_scheme['Right']:
                    self.buttons_held['Right'] = True
                if event.key == self.control_scheme['Up']:
                    self.buttons_held['Up'] = True
                if event.key == self.control_scheme['Down']:
                    self.buttons_held['Down'] = True

            if event.type == pygame.KEYUP:
                if event.key == self.control_scheme['Left']:
                    self.buttons_held['Left'] = False
                if event.key == self.control_scheme['Right']:
                    self.buttons_held['Right'] = False
                if event.key == self.control_scheme['Up']:
                    self.buttons_held['Up'] = False
                if event.key == self.control_scheme['Down']:
                    self.buttons_held['Down'] = False

        if self.buttons_held['Mouse Left'] and self.last_log_time + 500 <= int(round(time.time() * 1000)):
            self.last_log_time = int(round(time.time() * 1000))
            mouse_pos = pygame.mouse.get_pos()
            print("(" +
                  str(floor((mouse_pos[0] + vars_global.spectator_x) / Map.Cell.size)) + ", " +
                  str(floor((mouse_pos[1] - vars_global.spectator_y) / Map.Cell.size)) + ")"
                  )

        self.player.update(self.buttons_held)

        if True in self.buttons_held.values() and self.last_log_time + 1000 <= int(round(time.time() * 1000)):
            self.last_log_time = int(round(time.time() * 1000))
            print("Spectator Pos: ({}, {})".format(vars_global.spectator_x, vars_global.spectator_y))
            return True

        return False
