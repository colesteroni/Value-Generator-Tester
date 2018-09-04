# This module is meant to show the quality of pivotal block generation
# PLEASE NOTE: Can only run tools on command line from inside tools directory

from argparse import ArgumentParser

import sys
sys.path.append("..")

import generators


def map_o_piv_o_tal(range_x, range_y, space_x, space_y, generator, seed=None):

    if seed:
        generators.generator_dict[generator].seed_interpreter(seed, generators.generator_dict[generator].var_dict)

    state_list = [
        [generators.generator_dict[generator].get_state(x, y, generators.generator_dict[generator].var_dict)
         for y in range(0, range_y, space_y)]
        for x in range(0, range_x, space_x)]

    return state_list


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Usage: python pivotal_analyzer.py <generator> <range_x> <range_y> <space_x> <space_y>'
    )

    parser.add_argument('generator', type=str, nargs='?', default='Demo')

    parser.add_argument('range_x', type=int, nargs='?', default=50)

    parser.add_argument('range_y', type=int, nargs='?', default=50)

    parser.add_argument('space_x', type=int, nargs='?', default=10)

    parser.add_argument('space_y', type=int, nargs='?', default=10)

    parser.add_argument('-s', '--seed', type=str, dest='seed')

    args = parser.parse_args()

    [print(row) for row in map_o_piv_o_tal(args.range_x, args.range_y, args.space_x, args.space_y, args.generator, args.seed if args.seed else None)]
