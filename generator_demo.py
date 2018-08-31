# Map generator
# Every section_l blocks there will be a block chosen by a certain number in the seed fed into a formula
# the blocks around these pivotal blocks will be chosen by a voting system of the pivotal blocks that
# have wants based on the seed and influence based on their distance from the block being selected

from vars_constant import state_dict
import vars_global

from math import sin, sqrt

from seed import generate_seed


def seed_interpreter(seed):
    def set_by_dict(key, digit, value):
        if type(value) is not int:
            value = int("0x" + value, 0) * (1 if digit == 1 else ((digit - 1) * 16))

        if key is 'x_mod':
            vars_global.x_pivotal_gap += value
        elif key is 'y_mod':
            vars_global.y_pivotal_gap += value

    seed_dict = {
        0: (lambda value: set_by_dict('y_mod', 1, value)),
        1: (lambda value: set_by_dict('y_mod', 2, value)),
        2: (lambda value: set_by_dict('x_mod', 1, value)),
        3: (lambda value: set_by_dict('x_mod', 2, value))
    }

    seed = seed[::-1].upper()

    if len(seed) < len(seed_dict):
        seed += generate_seed(len(seed_dict) - len(seed))

    for n in range(0, len(seed)):
        seed_dict[n](seed[n])

    # Ensure hard requirements met
    if vars_global.x_pivotal_gap < 10: vars_global.x_pivotal_gap = 10

    if vars_global.y_pivotal_gap < 10: vars_global.y_pivotal_gap = 10

    if vars_global.x_pivotal_gap > 40: vars_global.x_pivotal_gap = 40

    if vars_global.y_pivotal_gap > 40: vars_global.y_pivotal_gap = 40


def pivotal_oscillator(x, y):
    oscillator = abs(
        100 * sin(x + y) / (
            x + y if not x + (
                        y) == 0 else 44)
    )

    return oscillator


def pivotal_filter(value):
    if value < 2:
        return 0
    elif value < 5:
        return 1
    elif value < 8:
        return 2
    else:
        return 3


def pivotal_state(xx, yy):
    return pivotal_filter(pivotal_oscillator(xx, yy))


def filler_state(x, y):
    dx = x % vars_global.x_pivotal_gap
    dy = y % vars_global.y_pivotal_gap

    x1 = x - dx
    x2 = x + (vars_global.x_pivotal_gap - dx) if dx else None
    y1 = y - dy
    y2 = y + (vars_global.y_pivotal_gap - dy) if dy else None

    surrounding_pivotals = [[(x1, y1)]]
    surrounding_pivotals += [[(x2, y1)]] if dx else []
    surrounding_pivotals += [[(x1, y2)]]if dy else []
    surrounding_pivotals += [[(x2, y2)]] if dx and dy else []

    for pivotal in surrounding_pivotals:
        if x - pivotal[0][0] and y - pivotal[0][1]:
            pivotal.append(sqrt((x - pivotal[0][0])**2 + (y - pivotal[0][1])**2))
        elif x - pivotal[0][0]:
            pivotal.append(abs(x - pivotal[0][0]))
        else:  # y - pivotal[0][1]:
            pivotal.append(abs(y - pivotal[0][1]))

    # vote with weights based on distance & block weights
    votes = [[key] for key in state_dict]

    for pivotal in surrounding_pivotals:
        index = None

        for i in range(0, len(votes)):
            if votes[i][0] is pivotal_state(pivotal[0][0], pivotal[0][1]):
                index = i
                break

        try:
            votes[index][1] += 1 * pivotal[1]
        except IndexError:
            votes[index].append(1 * pivotal[1])

    state = 0
    max_vote = 0
    for vote in votes:
        if len(vote) > 1:
            if vote[1] > max_vote:
                max_vote = vote[1]
                state = vote[0]

    return state
