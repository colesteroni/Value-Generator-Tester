# This module is meant to show the quality of pivotal block generation

from generator_demo import pivotal_state


def map_o_piv_o_tal():

    vars_global.x_pivotal_gap = default_x_pivotal_gap
    vars_global.y_pivotal_gap = default_y_pivotal_gap

    state_list = [
        [pivotal_state(xx, yy) for yy in range(0, vars_global.x_section_length )]
        for xx in range(0, vars_global.y_section_length)
    ]

    [print(row) for row in state_list]


if __name__ == '__main__':
    map_o_piv_o_tal()


