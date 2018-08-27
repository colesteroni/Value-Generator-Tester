# Object to handle keyboard controls

import sys  # sys.exit()
import pygame

import vars_global

from file_io import access_control_dict

from cell import Cell

from math import floor

import time


class Controller(object):
    def __init__(self, slot):
        self.slot = slot

        self.control_dictionary = access_control_dict(self.slot)

        self.buttons_held = {'Mouse Left': False, 'Left': False, 'Right': False, 'Up': False, 'Down': False}

        self.last_output = int(round(time.time() * 1000))

    def update_control_dictionary(self):
        return access_control_dict(self.slot, control_dictionary=self.control_dictionary)

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
                if event.key == self.control_dictionary['Left']:
                    self.buttons_held['Left'] = True
                if event.key == self.control_dictionary['Right']:
                    self.buttons_held['Right'] = True
                if event.key == self.control_dictionary['Up']:
                    self.buttons_held['Up'] = True
                if event.key == self.control_dictionary['Down']:
                    self.buttons_held['Down'] = True

            if event.type == pygame.KEYUP:
                if event.key == self.control_dictionary['Left']:
                    self.buttons_held['Left'] = False
                if event.key == self.control_dictionary['Right']:
                    self.buttons_held['Right'] = False
                if event.key == self.control_dictionary['Up']:
                    self.buttons_held['Up'] = False
                if event.key == self.control_dictionary['Down']:
                    self.buttons_held['Down'] = False

        if self.buttons_held['Mouse Left'] and self.last_output + 500 <= int(round(time.time() * 1000)):
            self.last_output = int(round(time.time() * 1000))
            mouse_pos = pygame.mouse.get_pos()
            print("(" +
                  str(floor((mouse_pos[0] + vars_global.spectator_x) / Cell.size)) + ", " +
                  str(floor((mouse_pos[1] + vars_global.spectator_y) / Cell.size)) + ")"
                  )

        speed = vars_global.spectator_speed

        if self.buttons_held['Left']:
            vars_global.spectator_x -= speed
            vars_global.spectator_x -= 1
        if self.buttons_held['Right']:
            vars_global.spectator_x += speed
            vars_global.spectator_x += 1
        if self.buttons_held['Up']:
            vars_global.spectator_y += speed
            vars_global.spectator_y += 1
        if self.buttons_held['Down']:
            vars_global.spectator_y -= speed
            vars_global.spectator_y -= 1

        if (self.buttons_held['Left'] or self.buttons_held['Right'] or \
                self.buttons_held['Up'] or self.buttons_held['Down']) \
                and self.last_output + 500 <= int(round(time.time() * 1000)):
            self.last_output = int(round(time.time() * 1000))
            print("Spectator Pos: ({}, {})".format(vars_global.spectator_x, vars_global.spectator_y))
            return True

        return False
