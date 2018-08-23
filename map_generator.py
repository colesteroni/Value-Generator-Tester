# Map generator

from cell import Cell


def get_state(x, y):
    return (4, 6)[(x + y) % 2]

class Generator(object):
    def __init__(self, display):
        self.display = display

    def generate(self, range_x, range_y):
        cell_list = []

        for x in range(range_x[0], range_x[1]):
            cell_list.append([])

            for y in range(range_y[0], range_y[1]):
                cell_list[x - range_x[0]].append(Cell(self.display, get_state(x, y), x, y))

        return cell_list
