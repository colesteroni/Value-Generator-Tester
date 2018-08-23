# Map generator

from cell import Cell

from vars_constant import section_l


class Generator(object):
    def __init__(self, display):
        self.display = display

        self.seed = 101010101

    def get_state(self, x, y):
        # Every section_l blocks there will be a block chosen by a certain number in the seed fed into a formula
        # the blocks around these pivotal blocks will be chosen by a voting system of the pivotal blocks that
        # have wants based on the seed and influence based on their distance from the block being selected
        if not x % section_l and not y % section_l:
            # is pivotal block
            state = 5
        else:
            if (x + y) % 2:
                # is odd block
                state = 4
            else:
                # is even block
                state = 6

        return state

    def generate(self, range_x, range_y):
        cell_list = []

        for x in range(range_x[0], range_x[1]):
            cell_list.append([])

            for y in range(range_y[0], range_y[1]):
                cell_list[x - range_x[0]].append(Cell(self.display, self.get_state(x, y), x, y))

        return cell_list
