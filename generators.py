# List of available generator objects


class GeneratorTemplate(object):
    # Functions should have the same arguments as the ones in the demo, unless you know what your doing
    def __init__(self, seed_interpreter, oscillation_function, pivotal_filter, pivotal_state, filler_chooser):
        self.seed_interpreter = seed_interpreter

        self.oscillation_function = oscillation_function
        self.pivotal_filter = pivotal_filter

        self.pivotal_state = pivotal_state

        # Needs better name than filler_chooser
        self.filler_chooser = filler_chooser


import generator_demo as gen_dem

generator_dict = {
    "Demo": GeneratorTemplate(
        gen_dem.seed_interpreter, gen_dem.pivotal_oscillator, gen_dem.pivotal_filter, gen_dem.pivotal_state, gen_dem.filler_state
    )
}
