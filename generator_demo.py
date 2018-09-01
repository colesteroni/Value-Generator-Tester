# Map generator
# Every section_l blocks there will be a block chosen by a certain number in the seed fed into a formula
# the blocks around these pivotal blocks will be chosen by a voting system of the pivotal blocks that
# have wants based on the seed and influence based on their distance from the block being selected

from vars_constant import state_dict, screen_width, screen_height
import vars_global

import map  # Cell size

from math import sin, sqrt

from seed import generate_seed


def base_gen(cell_map, var_dict):
    range_x = (
        int(vars_global.spectator_x / 50) - 1,
        int(vars_global.spectator_x / 50) + int(screen_width / map.Map.Cell.size) + 2
    )
    range_y = (
        int(vars_global.spectator_y / 50) - int(screen_height / map.Map.Cell.size) - 2,
        int(vars_global.spectator_y / 50) + 2
    )

    for x in range(-var_dict['x_pivotal_gap'], var_dict['x_pivotal_gap'], var_dict['x_pivotal_gap']):
        for y in range(-var_dict['y_pivotal_gap'], var_dict['y_pivotal_gap'], var_dict['y_pivotal_gap']):
            if (x, y) not in var_dict['pivotals_cached']:
                var_dict['pivotals_cached'].append((x, y))
                var_dict['pivotal_cache'].append(cell_map.Cell(cell_map, x, y))

    return [
        [cell_map.Cell(cell_map, x, y) for y in range(range_y[0], range_y[1])]
        for x in range(range_x[0], range_x[1])
    ]


def seed_interpreter(seed, var_dict):
    if not seed:
        seed = generate_seed(4)

    def set_by_dict(key, digit, value):
        if type(value) is not int:
            value = int("0x" + value, 0) * (1 if digit == 1 else ((digit - 1) * 16))

        if key is 'x_mod':
            var_dict['x_pivotal_gap'] += value
        elif key is 'y_mod':
            var_dict['y_pivotal_gap'] += value

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
    if var_dict['x_pivotal_gap'] < var_dict['min_x_pivotal_gap']:
        var_dict['x_pivotal_gap'] = var_dict['min_x_pivotal_gap']

    if var_dict['y_pivotal_gap'] < var_dict['min_y_pivotal_gap']:
        var_dict['y_pivotal_gap'] = var_dict['min_y_pivotal_gap']

    if var_dict['x_pivotal_gap'] > var_dict['max_x_pivotal_gap']:
        var_dict['x_pivotal_gap'] = var_dict['max_x_pivotal_gap']

    if var_dict['y_pivotal_gap'] > var_dict['max_y_pivotal_gap']:
        var_dict['y_pivotal_gap'] = var_dict['max_y_pivotal_gap']


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


def filler_state(x, y, var_dict):
    dx = x % var_dict['x_pivotal_gap']
    dy = y % var_dict['y_pivotal_gap']

    x1 = x - dx
    x2 = x + (var_dict['x_pivotal_gap'] - dx) if dx else None
    y1 = y - dy
    y2 = y + (var_dict['y_pivotal_gap'] - dy) if dy else None

    surrounding_pivotals = [[(x1, y1)]]
    surrounding_pivotals += [[(x2, y1)]] if dx else []
    surrounding_pivotals += [[(x1, y2)]]if dy else []
    surrounding_pivotals += [[(x2, y2)]] if dx and dy else []

    for pivotal in surrounding_pivotals:
        if pivotal[0] not in var_dict['pivotals_cached']:
            var_dict['pivotals_cached'].append(pivotal[0])
            var_dict['pivotal_cache'].append(pivotal_state(pivotal[0][0] / var_dict['x_pivotal_gap'], pivotal[0][1] / var_dict['y_pivotal_gap']))
            pivotal.append(pivotal_state(pivotal[0][0] / var_dict['x_pivotal_gap'], pivotal[0][1] / var_dict['y_pivotal_gap']))

        else:
            pivotal.append(var_dict['pivotal_cache'][var_dict['pivotals_cached'].index(pivotal[0])])

    for pivotal in surrounding_pivotals:
        if (x - pivotal[0][0]) and (y - pivotal[0][1]):
            pivotal.append(sqrt((x - pivotal[0][0])**2 + (y - pivotal[0][1])**2))
        elif x - pivotal[0][0]:
            pivotal.append(abs(x - pivotal[0][0]))
        else:  # y - pivotal[0][1]:
            pivotal.append(abs(y - pivotal[0][1]))

    # vote with weights based on distance & block weights
    votes = [[key, 0] for key in state_dict]

    for pivotal in surrounding_pivotals:
        for i in range(0, len(votes)):
            if votes[i][0] is pivotal[1]:
                votes[i][1] += 1 * pivotal[2]**3
                break

    state = 0
    max_vote = 0
    for vote in votes:
        if vote[1] > max_vote:
            max_vote = vote[1]
            state = vote[0]

    return state


def get_state(x, y, var_dict):
    if not x % var_dict['x_pivotal_gap'] and not y % var_dict['y_pivotal_gap']:  # is pivotal block
        xx = x / var_dict['x_pivotal_gap']
        yy = y / var_dict['y_pivotal_gap']

        state = pivotal_state(xx, yy)

    else:  # is filler block
        state = filler_state(x, y, var_dict)

    return state
