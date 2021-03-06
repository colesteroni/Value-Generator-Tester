# This is meant to solve the probability of a block spawning based on seed & formulas in use
# PLEASE NOTE: Can only run tools on command line from inside tools directory

from argparse import ArgumentParser

import sys
sys.path.append("..")

import vars_constant

import generators


def prob_pivotal_block(range_x, range_y, generator, seed=None):

    if seed:
        generators.generator_dict[generator].seed_interpreter(seed, generators.generator_dict[generator].var_dict)

    counter = []

    for key in vars_constant.state_dict:
        counter.append([key, 0, 0])

    for x in range(0, range_x):
        for y in range(0, range_y):
            output = generators.generator_dict[generator].get_state(x, y, generators.generator_dict[generator].var_dict)

            for i in range(0, len(counter)):
                if int(output) == counter[i][0]:
                    counter[i][1] += 1
                    break

    total = 0

    for item in counter:
        total += item[1]

    for item in counter:
        item[2] = (str(item[1] / total * 100) if total > 0 else "0") + '%'

    return counter


if __name__ == '__main__':
    parser = ArgumentParser(description='Usage: python block_probability.py <generator> <x> <y>')

    parser.add_argument('generator', type=str, nargs='?', default='Demo')

    parser.add_argument('range_x', type=int, nargs='?', default=50)

    parser.add_argument('range_y', type=int, nargs='?', default=50)

    parser.add_argument('-s', '--seed', type=str, dest='seed')

    args = parser.parse_args()

    print(prob_pivotal_block(args.range_x, args.range_y, args.generator, args.seed if args.seed else None))
