import pickle

startup_dict = {'Control Slot': 1}

with open('../data/startup.dat', 'wb') as file:
    pickle.dump(startup_dict, file)
