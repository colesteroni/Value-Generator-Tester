# Seed generation

import time


def generate_seed(length):
    print("Generating seed. Length: {}".format(length))

    seed = ""

    for i in range(0, int(length / 2)):
        millis = int(round(time.time() * 1000))

        seed += str(hex(millis % 255)[2:])

        time.sleep(float(int(millis)**2 % 1000) / 1000.0)

    while len(seed) > length:
        seed = seed[1:]

    print("Done generating seed.")
    return seed
