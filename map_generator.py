# Map generator
# Every section_l blocks there will be a block chosen by a certain number in the seed fed into a formula
# the blocks around these pivotal blocks will be chosen by a voting system of the pivotal blocks that
# have wants based on the seed and influence based on their distance from the block being selected

from vars_constant import section_l
import vars_global

from math import sin


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

    #print(surrounding_pivotals)
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
