# This module is meant to show the quality of pivotal block generation

from map_generator import Generator


def map_o_piv_o_tal():

    generator = Generator()

    state_list = [
        [generator.pivotal_state(x, y) for y in range(0, generator.y_length)]
        for x in range(0, generator.x_length)
    ]

    [print(row) for row in state_list]


if __name__ == '__main__':
    map_o_piv_o_tal()


