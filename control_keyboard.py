# Object to handle keyboard controls

import sys  # sys.exit()
import pygame

import vars_global

from file_io import read_control_dictionary, write_control_dictionary


class Keyboard(object):
    def __init__(self, slot):
        self.slot = slot

        self.control_dictionary = read_control_dictionary(self.slot)

        self.keys_held = {'Left': False, 'Right': False, 'Up': False, 'Down': False}

    def update_control_dictionary(self):
        write_control_dictionary(self.slot, self.control_dictionary)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == self.control_dictionary['Left']:
                    self.keys_held['Left'] = True
                if event.key == self.control_dictionary['Right']:
                    self.keys_held['Right'] = True
                if event.key == self.control_dictionary['Up']:
                    self.keys_held['Up'] = True
                if event.key == self.control_dictionary['Down']:
                    self.keys_held['Down'] = True

            if event.type == pygame.KEYUP:
                if event.key == self.control_dictionary['Left']:
                    self.keys_held['Left'] = False
                if event.key == self.control_dictionary['Right']:
                    self.keys_held['Right'] = False
                if event.key == self.control_dictionary['Up']:
                    self.keys_held['Up'] = False
                if event.key == self.control_dictionary['Down']:
                    self.keys_held['Down'] = False

        # TODO - Move movement code?

        speed = vars_global.spectator_speed

        if self.keys_held['Left']:
            vars_global.spectator_x -= speed
            vars_global.spectator_x -= 1
        if self.keys_held['Right']:
            vars_global.spectator_x += speed
            vars_global.spectator_x += 1
        if self.keys_held['Up']:
            vars_global.spectator_y += speed
            vars_global.spectator_y += 1
        if self.keys_held['Down']:
            vars_global.spectator_y -= speed
            vars_global.spectator_y -= 1

        if self.keys_held['Left'] or self.keys_held['Right'] or self.keys_held['Up'] or self.keys_held['Down']:
            print("Spectator Pos: ({}, {})".format(vars_global.spectator_x, vars_global.spectator_y))
            return True

        return False
