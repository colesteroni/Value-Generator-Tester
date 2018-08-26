# This is meant to solve the probability of a block spawning based on seed & formulas in use

from vars_constant import state_dict

from map_generator import Generator


def prob_pivotal_block():
    generator = Generator()

    counter = []

    for key in state_dict:
        counter.append([key, 0, 0])

    for x in range(0, generator.x_length):
        for y in range(0, generator.y_length):
            output = generator.pivotal_state(x, y)

            for i in range(0, len(counter)):
                if int(output) == counter[i][0]:
                    counter[i][1] += 1
                    break

    total = 0

    for item in counter:
        total += item[1]

    for item in counter:
        item[2] = item[1] / total * 100

    print(counter)


if __name__ == '__main__':
    prob_pivotal_block()
