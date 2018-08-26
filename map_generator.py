# Map generator
# Every section_l blocks there will be a block chosen by a certain number in the seed fed into a formula
# the blocks around these pivotal blocks will be chosen by a voting system of the pivotal blocks that
# have wants based on the seed and influence based on their distance from the block being selected

from cell import Cell

from vars_constant import section_l

from math import sin
import random


class Generator(object):
    def __init__(self, display=None, seed="3232"):
        self.display = display

        self.x_length = 0
        self.y_length = 0

        self.cell_list = []

        def set_by_dict(key, digit, value):
            if type(value) is not int:
                value = int("0x" + value, 0) * (1 if digit == 1 else ((digit - 1) * 16))

            if key is 'x_mod':
                self.x_length += value
            elif key is 'y_mod':
                self.y_length += value

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
        if self.x_length < 40: self.x_length = 40

        if self.y_length < 40: self.y_length = 40

    def pivotal_oscillator(self, x, y):
        oscillator = abs(
            100 * sin((x % self.x_length) + (y % self.y_length)) / (
                (x % self.x_length) + (y % self.y_length) if not (x % self.x_length) + (y % self.y_length) == 0 else 44)
        )

        return oscillator

    def pivotal_state(self, x, y):
        oscillator = self.pivotal_oscillator(x, y)

        if oscillator < .8:
            return 0
        elif oscillator < 2.8:
            return 1
        elif oscillator < 5:
            return 2
        else:
            return 3

    def get_state(self, x, y):
        if not x % section_l and not y % section_l:  # is pivotal block
            state = self.pivotal_state(x, y)

        else: # is filler block
            # find 4 or 2 surrounding pivotal blocks
            state = 4

        return state

    def generate(self, range_x, range_y):
        cell_list = [
            [Cell(self.display, self.get_state(x, y), x, y) for y in range(range_y[0], range_y[1])]
            for x in range(range_x[0], range_x[1])
        ]

        for row in cell_list:
            for cell in row:
                if not cell.state:
                    cell_list[cell_list.index(row)][row.index(cell)] = Cell(self.display, self.get_state(cell.x, cell.y), cell.x, cell.y)

        self.cell_list = cell_list
