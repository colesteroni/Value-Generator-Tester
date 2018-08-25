# Map creation, cell controlling and selective rendering

import map_generator

import vars_global


class Map(object):
    def __init__(self, display, generator=None):
        self.display = display

        self.generator = generator if generator else map_generator.Generator(self.display)

        self.cell_list = self.generator.generate(
            (vars_global.spectator_x - 10, vars_global.spectator_x + 10),
            (vars_global.spectator_y - 10, vars_global.spectator_y + 10)
        )

    def update(self):
        self.cell_list = self.generator.generate(
            (int(vars_global.spectator_x / 50) - 1, int(vars_global.spectator_x / 50) + 14),
            (int(vars_global.spectator_y / 50) - 10, int(vars_global.spectator_y / 50) + 2)
        )

    def render(self):
        self.update()

        for column in self.cell_list:
            for row in column:
                row.render()
