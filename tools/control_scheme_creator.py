# PLEASE NOTE: Can only run tools on command line from inside tools directory

import pickle

import sys
sys.path.append("..")

import controller

slot = 1

default_control_scheme = controller.default_control_scheme

with open('../data/controller_schemes/{}.dat'.format(slot), 'wb') as file:
    pickle.dump(default_control_scheme, file)
