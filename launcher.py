# Launcher!
# Separated from main to individualize modules by having main just run game loop

from file_io import read_startup_file

import pygame

from vars_constant import screen_width, screen_height

from map import Map

from controller import Controller

import main


def launch():
    startup_dict = read_startup_file()

    pygame.init()

    display = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption("2d Cell Engine by Cole")

    main.main(display, pygame.time.Clock(), Map(display), Controller(startup_dict['Control Slot']))


if __name__ == "__main__":
    launch()
