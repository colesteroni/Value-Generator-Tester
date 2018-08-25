# Map generator

from cell import Cell

from vars_constant import section_l

from math import sin


class Generator(object):
    def __init__(self, display=None, seed="3434"):
        self.display = display

        # TODO - make each key apply the value at the index to the variable that is the value
        seed_dict = {
            0: 'y_mod', 1: 'y_mod', 2: 'x_mod', 3: 'x_mod'
        }

        # See if seed valid, if not append to it
        if len(seed) < len(seed_dict):
            # TODO - Randomly generate hex numbers for each but make sure are safe
            seed += 'A'

        self.seed = seed[::-1].upper()

        # TODO - better system of converting hex string to int!ww
        self.x_mod = int("0x" + self.seed[2:4], 0)
        self.y_mod = int("0x" + self.seed[0:2], 0)

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
        cell_list = []

        for x in range(range_x[0], range_x[1]):
            cell_list.append([])

            for y in range(range_y[0], range_y[1]):
                cell_list[x - range_x[0]].append(Cell(self.display, self.get_state(x, y), x, y))

        return cell_list
