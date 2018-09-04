# Tool to create a text based map
# PLEASE NOTE: Can only run tools on command line from inside tools directory

from argparse import ArgumentParser

import pickle
import os

import sys
sys.path.append("..")

import generators


def map_to_text(range_x, range_y, generator, seed=None):

    if seed:
        generators.generator_dict[generator].seed_interpreter(seed, generators.generator_dict[generator].var_dict)

    text_map = [
        [generators.generator_dict[generator].get_state(x, y, generators.generator_dict[generator].var_dict)
         for y in range(0, range_y)]
        for x in range(0, range_x)]

    return text_map


if __name__ == '__main__':
    parser = ArgumentParser(description='Usage: python map_to_text.py <generator> <x> <y>')

    parser.add_argument('generator', type=str, nargs='?', default='Demo')

    parser.add_argument('range_x', type=int, nargs='?', default=50)

    parser.add_argument('range_y', type=int, nargs='?', default=50)

    parser.add_argument('-s', '--seed', type=str, dest='seed')

    parser.add_argument('-o', '--output', type=str, dest='output',
                        help="S to save as text file, P to save as pickle file, C to output to console.")

    args = parser.parse_args()

    text_map = map_to_text(args.range_x, args.range_y, args.generator, args.seed if args.seed else None)

    if args.output:
        if args.output.upper() == 'S':
            text_file = "text_map"

            i = 0
            while os.path.exists(text_file + str(i) + ".txt"):
                i += 1

            with open(text_file + str(i) + ".txt", "a") as file:
                file.write(str(text_map))

        if args.output.upper() == 'P':
            pickle_file = "text_map_pickle"

            i = 0
            while os.path.exists(pickle_file + str(i) + ".dat"):
                i += 1

            with open(pickle_file + str(i) + ".dat", "wb") as f:
                pickle.dump(text_map, f)

        if args.output.upper() == 'C':
            print(text_map)

    else:
        [print(row) for row in text_map]
