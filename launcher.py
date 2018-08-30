# Launcher!
# Separated from main to individualize modules by having main just run game loop

from file_io import read_startup_file

import pygame

from vars_constant import screen_width, screen_height

from map import Map

from player import Player

from controller import Controller

from main import main


def launch():
    startup_dict = read_startup_file()

    pygame.init()

    display = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption("2d Cell Engine by Cole")

    cell_map = Map(display)

    player = Player(cell_map)

    print(main(display, pygame.time.Clock(), cell_map, player, Controller(startup_dict['Control Slot'], player)))


if __name__ == "__main__":
    launch()
