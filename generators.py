# List of available generator objects


class GeneratorTemplate(object):
    # Functions should have the same arguments as the ones in the demo, unless you know what your doing
    def __init__(self, base_gen, var_dict, seed_interpreter, get_state):
        self.base_gen = base_gen

        self.var_dict = var_dict

        self.seed_interpreter = seed_interpreter

        self.get_state = get_state


import generator_demo as gen_dem

generator_dict = {
    "Demo": GeneratorTemplate(
        gen_dem.base_gen,
        {'pivotals_cached': set(()), 'pivotal_cache': [], 'x_pivotal_gap': 0, 'y_pivotal_gap': 0, 'x_section_length': 50, 'y_section_length': 50},
        gen_dem.seed_interpreter, gen_dem.get_state
    )
}
