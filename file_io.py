# Handles all of the file input/output

import pickle


def read_startup_file():
    try:
        with open('data/startup.dat', 'rb') as startup_file:
            return pickle.load(startup_file)

    except (OSError, pickle.UnpicklingError, AttributeError, EOFError, ImportError, IndexError) as e:
        print("Pickle cannot unpickle startup file because {}".format(e))


def access_control_dict(slot, control_dictionary=None):
    try:
        with open('data/controller_schemes/{}.dat'.format(slot), ('wb' if control_dictionary else 'rb')) as control_scheme:
            try:
                if control_dictionary:
                    pickle.dump(control_dictionary, control_scheme)
                    return True
                else:
                    return pickle.load(control_scheme)

            except (pickle.UnpicklingError, AttributeError, EOFError, ImportError, IndexError) as e:
                print("Pickle cannot unpickle controller @ slot {} because {}".format(slot, e))
                return False

    except OSError as e:
        print("Error accessing control_schemes/{}.dat because {}".format(slot, e))
        return False
