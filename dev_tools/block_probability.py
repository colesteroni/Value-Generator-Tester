# This is meant to solve the probability of a block spawning based on seed & formulas in use

from vars_constant import state_dict
import vars_global

from generator_demo import pivotal_state


def prob_pivotal_block():

    counter = []

    for key in state_dict:
        counter.append([key, 0, 0])

    for xx in range(0, vars_global.x_section_length):
        for yy in range(0, vars_global.y_section_length):
            output = pivotal_state(xx, yy)

            for i in range(0, len(counter)):
                if int(output) == counter[i][0]:
                    counter[i][1] += 1
                    break

    total = 0

    for item in counter:
        total += item[1]

    for item in counter:
        item[2] = (str(item[1] / total * 100) if total > 0 else "0") + '%'

    print(counter)


if __name__ == '__main__':
    prob_pivotal_block()
