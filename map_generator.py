# Map generator
# Every section_l blocks there will be a block chosen by a certain number in the seed fed into a formula
# the blocks around these pivotal blocks will be chosen by a voting system of the pivotal blocks that
# have wants based on the seed and influence based on their distance from the block being selected

from cell import Cell

from vars_constant import section_l
import vars_global

from math import sin
import random


class Generator(object):
    def __init__(self, display=None, seed="3232"):
        self.display = display

        self.cell_list = []

        def set_by_dict(key, digit, value):
            if type(value) is not int:
                value = int("0x" + value, 0) * (1 if digit == 1 else ((digit - 1) * 16))

            if key is 'x_mod':
                vars_global.x_length += value
            elif key is 'y_mod':
                vars_global.y_length += value

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
        if vars_global.x_length < 40: vars_global.x_length = 40

        if vars_global.y_length < 40: vars_global.y_length = 40

    def generate(self, range_x, range_y):
        for x in range(-vars_global.x_length, vars_global.x_length):
            for y in range(-vars_global.y_length, vars_global.y_length):
                if (x, y) not in vars_global.pivotals_cached:
                    vars_global.pivotals_cached.add((x, y))
                    vars_global.pivotal_cache.append(Cell(self.display, x, y))

        cell_list = [
            [Cell(self.display, x, y) for y in range(range_y[0], range_y[1])]
            for x in range(range_x[0], range_x[1])
        ]

        self.cell_list = cell_list


def pivotal_oscillator(x, y):
    oscillator = abs(
        100 * sin((x % vars_global.x_length) + (y % vars_global.y_length)) / (
            (x % vars_global.x_length) + (y % vars_global.y_length) if not (x % vars_global.x_length) + (
                        y % vars_global.y_length) == 0 else 44)
    )

    return oscillator


def pivotal_state(x, y):
    oscillator = pivotal_oscillator(x, y)

    if oscillator < .8:
        return 0
    elif oscillator < 2.8:
        return 1
    elif oscillator < 5:
        return 2
    else:
        return 3


def filler_state(x, y):
    # get x and y values for what should be pivotals
    dx = x % vars_global.x_length
    dy = y % vars_global.y_length

    x1 = x - dx
    x2 = x + (vars_global.x_length - dx) if dx else None
    y1 = y - dy
    y2 = y + (vars_global.y_length - dy) if dy else None

    surrounding_pivotals = [(x1, y1)]
    surrounding_pivotals += [(x2, y1)] if dx else []
    surrounding_pivotals += [(x1, y2)] if dy else []
    surrounding_pivotals += [(x2, y2)] if dx and dy else []

    print(surrounding_pivotals)
    # get 2/4 surrounding pivotals

    return 4


def get_state(x=None, y=None, cell=None):
    if x is None:
        x = cell.x

    if y is None:
        y = cell.y

    if not x % section_l and not y % section_l:  # is pivotal block
        state = pivotal_state(x, y)

    else:  # is filler block
        state = filler_state(x, y)

    return state
