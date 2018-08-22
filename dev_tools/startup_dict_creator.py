startup_dict = {'Keyboard Control Slot': 1}

import pickle

with open('C:/Users/cole/Desktop/Bomb Cell Engine/startup.dat', 'wb') as file:
	pickle.dump(startup_dict, file)
