# Handles all of the file input/output

import pickle


def read_startup_file():
    with open('data/startup.dat', 'rb') as f:
        startup_dict = pickle.load(f)

        return startup_dict


def read_control_dictionary(slot):
    with open('data/controllers/{}.dat'.format(slot), 'rb') as f_control_dictionary:
        control_dictionary = pickle.load(f_control_dictionary)

        return control_dictionary


def write_control_dictionary(slot, control_dictionary):
    with open('data/controllers/{}.dat'.format(slot), 'wb') as f_control_dictionary:
        pickle.dump(control_dictionary, f_control_dictionary)
