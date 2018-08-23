# Map generator

from cell import Cell

from vars_constant import section_l

from math import sin


class Generator(object):
    def __init__(self, display=None):
        self.display = display

        self.seed = 101010101

        self.x_mod = 50
        self.y_mod = 50

    def pivotal_oscillator(self, x, y):
        oscillator = abs(
            100 * sin((x % self.x_mod) + (y % self.y_mod)) / (
                (x % self.x_mod) + (y % self.y_mod) if not (x % self.x_mod) + (y % self.y_mod) == 0 else 44)
        )

        return oscillator

    def pivotal_state(self, x, y):
        oscillator = self.pivotal_oscillator(x, y)

        if oscillator < 1:
            return 0
        elif oscillator < 5:
            return 1
        elif oscillator < 10:
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
        cell_list = []

        for x in range(range_x[0], range_x[1]):
            cell_list.append([])

            for y in range(range_y[0], range_y[1]):
                cell_list[x - range_x[0]].append(Cell(self.display, self.get_state(x, y), x, y))

        return cell_list
