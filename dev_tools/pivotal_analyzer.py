# This module is meant to show the quality of pivotal block generation

from map import Map
import vars_global

from map_generator import pivotal_state


def map_o_piv_o_tal():
    map = Map()
    generator = map.Generator(map)

    state_list = [
        [pivotal_state(x, y) for y in range(0, vars_global.y_length)]
        for x in range(0, vars_global.x_length)
    ]

    [print(row) for row in state_list]


if __name__ == '__main__':
    map_o_piv_o_tal()


