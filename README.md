# Generative map engine tester
Cell based map engine meant to test (pseudo)random terrain generation algorithms. I created this project mainly to practice git and teach myself about controlling randomness as a sort of prerequisite to machine learning. Hopefully though, someone can make use of this as a part of a game or to learn something new! I am also trying to learn to program in a way that is more readable so please pardon my lack of comments. Uses Python 3.6 and PyGame 1.9. 

# How to use
 * Pseudo-Random Map Generation Testing Engine by Cole Dieckhaus *

# Purpose #

This engine is meant to test and compare different map generation algorithms. You can configure & create a generator
object in the dictionary 'generator_dict' located in file 'generators.py'. Then you can either set the default generator
in 'launcher.py' or choose it in the command line by calling 'python launcher.py -r GeneratorName -s Seed'. If no seed
is specified the generator can choose what to do.

# Engine Backbone Explanation #

Global constants ie variables that may need to be tweaked on a frequent basis are stored in vars_constant
Currently all dynamic global variables are stored in vars_global but in the future there will be none of these.

User settings are stored in data/startup.dat. These are read in at game startup in the launcher which has a single
purpose of initialization. The launcher also initializes PyGame, the clock, the display, the map and the controller
object.

    The display is a simple PyGame display with dimensions set in vars_constant.
    The clock is a simple PyGame clock used to set a fixed update rate
    The map is a cell based map that is generated pseudo-randomly in the generator(explained later).
    The controller handles all PyGame events which currently is only mouse/keyboard inputs and the big ole X button.

After initialization the launcher calls main() which is the game loop. Main gets controller input, updates the map and
then renders it onto the screen. It also handles the clock ticks which is solely for update limiting.


# Per-Object Explanations #

Controller
    The controller pretty much just factors the pygame.event.get loop out of the main loop.

Player
    As of writing this there is no player implemented yet but this is what I have been planning on making the player do.
    The player object will handle the movement code, be able to edit blocks and place items. I will try and leave
    everything as open to improvement as possible as I am with everything else, but this should be open to the most
    broad set of uses.

Map
    The map is a collection of cells that are generated randomly but can be modified and can have items on top of. The
    initial state of the blocks are generated by a generator object that only needs to fill the players screen with
    cells at a time. It does this by placing a so called pivotal block every so often(x_length, y_length) which has a
    frequency defined by the seed and a minimum value hardcoded. The pivotal blocks are generated with an oscillating
    function with coefficients set by the seed. This oscillating functions values are passed through a filter that
    assigns a state for the block. These pivotal blocks then assign all of the other 'filler' blocks a value through
    a voting system. The blocks can be placed over and items can be placed on top of by the player and this data will
    be saved into a file that will be read when necessary.

Map Seed
    The map seed is a series of hex numbers that set certain variables that are essential to the cell generation
    process. A map seed is crucial to the generator because it would be nearly impossible(for me) to debug and update
    an entirely random map generator. The seed allows the developer to make use of a static intermediary between the
    code and its produced output.

Dev Tools
    This project was made to help improve randomness controlling skills and it helps to have some tools that measure
    purposeful metrics automatically. These are all pretty self explanatory and very susceptible to change so figuring
    them out in code is the most effective path.