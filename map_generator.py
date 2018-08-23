# Map generator

from cell import Cell

from vars_constant import section_l

from math import sin


class Generator(object):
    def __init__(self, display):
        self.display = display

        self.seed = 101010101

    def get_state(self, x, y):
        # Every section_l blocks there will be a block chosen by a certain number in the seed fed into a formula
        # the blocks around these pivotal blocks will be chosen by a voting system of the pivotal blocks that
        # have wants based on the seed and influence based on their distance from the block being selected
        if not x % section_l and not y % section_l:  # is pivotal block
            # Will use oscillating function with weights determined by the seed to chose pivotal blocks

            oscillator = 100 * sin((x % 100) + (y % 100)) / ((x % 100) + (y % 100) if not (x % 1) + (y % 100) == 0 else 44)

            oscillator = abs(oscillator)

            if oscillator < 1:
                state = 0
            elif oscillator < 5:
                state = 1
            elif oscillator < 10:
                state = 2
            else:
                state = 3

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
