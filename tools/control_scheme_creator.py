import pickle

from controller import default_control_scheme

slot = 1

with open('../data/controller_schemes/{}.dat'.format(slot), 'wb') as file:
    pickle.dump(default_control_scheme, file)
