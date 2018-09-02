# Launcher!
# Separated from main to individualize modules by having main just run game loop

from optparse import OptionParser
import sys

from generators import generator_dict

from file_io import read_startup_file

import pygame

from vars_constant import screen_width, screen_height
import vars_global  # for -p / --pos

from map import Map

from player import Player

from controller import Controller

from main import main


def launch():
    # Possible flags to throw when running module from command line. python launcher.py <flags>
    parser = OptionParser()

    parser.add_option("-r", "--run", type=str, dest="generator",
                      help="Enter a the name of the generator you would like to run. Use -l to see list of generators.")

    parser.add_option("-s", "--seed", type=str, dest="seed",
                      help="Enter seed to test generator with. Extra digits ignored, more digits added if needed.")

    parser.add_option("-p", "--pos", type=int, nargs=2, dest="pos",
                      help="Enter starting cell as two ints separated by spaces.")

    def print_generators(options=None, opt=None, value=None, parser=None):
        [print("{}: {}".format(name, generator_object.description)) for name, generator_object in generator_dict.items()]
        pygame.quit()
        sys.exit()

    parser.add_option("-l", "--list",
                      action="callback", callback=print_generators,
                      help="Print list of available generators.")

    (options, args) = parser.parse_args(sys.argv)

    # Seeing if value set in flag, if not set to hardcoded default
    try:
        generator = options.generator

        if not options.generator:
            raise AttributeError

        if str(options.generator) not in [key for key in generator_dict]:
            print("Invalid generator - {}!".format(options.generator))
            pygame.quit()
            sys.exit()

    except AttributeError:
        generator = str([key for key in generator_dict][0])

    try:
        if not options.seed:
            raise AttributeError

        seed = options.seed
    except AttributeError:
        seed = None

    try:
        if not options.pos:
            raise AttributeError

        vars_global.spectator_x = options.pos[0] * Map.Cell.size
        if __name__ == '__main__':
            vars_global.spectator_y = options.pos[1] * Map.Cell.size
    except AttributeError:
        pass

    print("Received values, Generator Choice: \"{}\", Seed: \"{}\"".format(generator, seed))
    print("Initializing engine.")

    startup_dict = read_startup_file()

    pygame.init()

    display = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption("2d Cell Engine by Cole")

    cell_map = Map(display, generator, seed)

    player = Player(cell_map)

    print(main(display, pygame.time.Clock(), cell_map, player, Controller(startup_dict['Control Slot'], player)))


if __name__ == "__main__":
    launch()
