import pickle

startup_dict = {'Control Slot': 1}

with open('C:/Users/cole/Desktop/Bomb Cell Engine/startup.dat', 'wb') as file:
    pickle.dump(startup_dict, file)
