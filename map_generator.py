# Map generator

from cell import Cell

from vars_constant import section_l

from math import sin


class Generator(object):
    def __init__(self, display=None, seed="3232"):
        self.display = display

        self.x_mod = 0
        self.y_mod = 0

        def set_by_dict(key, digit, value):
            value = int("0x" + value, 0) * (1 if digit == 1 else ((digit - 1) * 16))

            if key == 'x_mod':
                self.x_mod += value
            elif key == 'y_mod':
                self.y_mod += value

        seed_dict = {
            0: (lambda value: set_by_dict('y_mod', 1, value)),
            1: (lambda value: set_by_dict('y_mod', 2, value)),
            2: (lambda value: set_by_dict('x_mod', 1, value)),
            3: (lambda value: set_by_dict('x_mod', 2, value))
        }

        if len(seed) < len(seed_dict):
            # TODO - Randomly generate hex numbers for each but make sure are safe
            seed += 'A'

        self.seed = seed[::-1].upper()

        for digit in range(0, len(self.seed)):
            seed_dict[digit](self.seed[digit])

        print("x_mod: {}, y_mod: {}".format(self.x_mod, self.y_mod))

    def pivotal_oscillator(self, x, y):
        # TODO - Better oscillating function or different block selection because rare blocks get clustered around
        #       the top left edge of each section (unless that is the goal?) - One that hits higher values for longer
        # TODO - Test and see empirically how well mixed the pivotal blocks are!

        oscillator = abs(
            100 * sin((x % self.x_mod) + (y % self.y_mod)) / (
                (x % self.x_mod) + (y % self.y_mod) if not (x % self.x_mod) + (y % self.y_mod) == 0 else 44)
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
        # Every section_l blocks there will be a block chosen by a certain number in the seed fed into a formula
        # the blocks around these pivotal blocks will be chosen by a voting system of the pivotal blocks that
        # have wants based on the seed and influence based on their distance from the block being selected
        if not x % section_l and not y % section_l:  # is pivotal block
            # Will use oscillating function with weights determined by the seed to chose pivotal blocks

            state = self.pivotal_state(x, y)

        else:
            if (x + y) % 2:  # is odd block
                state = 4
            else:  # is even block
                state = 6

        return state

    def generate(self, range_x, range_y):
        cell_list = [
            [Cell(self.display, self.get_state(x, y), x, y) for y in range(range_y[0], range_y[1])]
            for x in range(range_x[0], range_x[1])
        ]

        return cell_list
