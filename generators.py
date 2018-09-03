# List of available generator objects


class GeneratorTemplate(object):
    # Functions should have the same arguments as the ones in the demo, unless you know what your doing
    def __init__(self, base_gen, var_dict, seed_interpreter, get_state, description="Generates map."):

        # Called on every Map.update() meaning every tick.
        # Takes 2 arguments
        #   cell_map(Map object),
        #   var_dict(declared in GeneratorTemplate for use in individual generator).
        # Returns: Cell list to be rendered on screen.
        self.base_gen = base_gen

        # Space to store variables needed for specific generator. Given as argument for every function.
        self.var_dict = var_dict

        # Can use to interpret seed. May need to generate parts or all of seed.
        # Takes 2 arguments
        #   seed(the manually set, hardcoded or undefined seed value),
        #   var_dict(declared in GeneratorTemplate for use in individual generator).
        # Returns: Nothing.
        self.seed_interpreter = seed_interpreter

        # Called on cell creation.
        # Takes 3 arguments
        #   x(X pos of specific cell),
        #   y(Y pos of specific cell),
        #   var_dict(declared in GeneratorTemplate for use in individual generator).
        # Returns: Cell state. States defined in vars_constant.state_dict
        self.get_state = get_state

        # Solely for the -l flag to list available generators when starting the engine.
        self.description = description


import generator_demo as gen_dem

generator_dict = {
    "Demo": GeneratorTemplate(
        gen_dem.base_gen,
        {'pivotals_cached': [], 'pivotal_cache': [], 'x_pivotal_gap': 10, 'y_pivotal_gap': 10, 'min_x_pivotal_gap': 10,
         'min_y_pivotal_gap': 10, 'max_x_pivotal_gap': 20, 'max_y_pivotal_gap': 20, 'x_section_length': 50,
         'y_section_length': 50},
        gen_dem.seed_interpreter, gen_dem.get_state,
        "The demo/default generator. Low values make for a good seed ie 0A0A or 0B0B (min 0A0A, max 1A1A)."
    )
}
