# Psuedo-Random Value Generator Tester by Cole Dieckhaus
Cell based map engine meant to test (pseudo)random value generation algorithms. I created this project mainly to 
practice git and teach myself about controlling randomness as a prerequisite to machine learning. 

Uses Python 3.6 and PyGame 1.9. 

# How to use
You should create an index to the dictionary 'generator_dict' located in file 'generators.py'. The key should be the 
name of the generator and the value a GeneratorTemplate object(defined at the top of generators.py). Then you can either
hardcode a new default generator in 'launcher.py' or choose one in the command line by calling 'python launcher.py -r 
GeneratorName -s Seed'. If no seed is specified the generator can choose what to do which is noramally to generate a 
seed.

## Engine Backbone Explanation #
Global constants ie variables that may need to be tweaked on a frequent basis are stored in 'vars_constant.py'.
Currently all dynamic global variables are stored in 'vars_global.py'.

User settings are stored in data/startup.dat. These are read in at game startup in the launcher. The launcher is the 
starting point of the engine; when run in command line using 'python launcher.py' you can make use of the parser and 
pass extra commands.
    
Command List
* '-l' / '--list'  to list available generators
* '-r \<generator_name>' / '--run \<generator_name>' to run specified generator
* '-s \<seed>' / '--seed \<seed>' to specify seed to run
* '-p \<x> \<y>' / '--pos \<x> \<y>' to specify spectator/player start pos
   
The launcher also initializes PyGame, the clock, the display, the map, the player and the controller object.

    The display is a simple PyGame window with dimensions set in vars_constant.
    The clock is a simple PyGame clock used to set a fixed update rate
    The map is a cell based map that is generated pseudo-randomly in the generator(explained later).
    The player/spectator gets commands from the controller and can navigate the map.
    The controller handles all PyGame events which currently is only mouse/keyboard inputs and the big ole X button.

After initialization the launcher calls main() which is the game loop. Main gets controller input, updates the map & 
player then renders everything onto the screen. It also handles the clock ticks which is solely for update limiting.


## Per-Object Explanations #
###Controller
The controller pretty much just factors the pygame.event.get loop out of the main loop.

###Player
The player object handles movement and appears in the center of the screen as a green square.

###Map
The map is a collection of cells generated procedurally by the generator. Each map creates it's own generator and seed
    if not given. The map is navigated by the player.
    
###Map Seed
The map seed is a series of hex numbers that set certain variables in the generator. A map seed is crucial to the 
    generator because it would be very hard to debug and update an entirely random map generator. The seed allows the 
    developer to make use of a static intermediary between the code and its produced output.

###Map Generator
The map generator calls the functions assigned to the chosen generator in the GeneratorTemplate(generators.py). On 
    generator creation seed_interpreter is called. On each map.update base_gen is called which creates a cell list, each
    cell calls the get_state function with its x, y coordinates. Every generator function gets called with a variable 
    var_dict that can be customized for each generator with any amount of values.

###Unit Tests
The unit tests are to make sure that everything is working as it should be. The unit test manager will run everything
    that is has imported. The manager also has a built in parser so that you can call various extra functions.
* '-l' / '--list' lists available unit tests
* '-a' / '--all' is run by default.
* '-r \<test>' / '--run \<test>' runs the specific unit test

###Dev Tools
This project was made to help control and improve the randomness of psuedo-random value generation engines so it would 
    be helpful to have some built in tools to measure the quality a the generators value creation. These are all pretty 
    self explanatory and very susceptible to change so figuring them out in code is the most effective path.
