# A unit test manager that can be controlled from the command line

from optparse import OptionParser
import sys


def demo_func():
    pass


test_dict = {'Demo does nothin': demo_func}


def print_tests(option=None, opt=None, value=None, parser=None):
    print([key for key in test_dict])


def run_all_tests(option=None, opt=None, value=None, parser=None):
    for key, value in test_dict.items():
        print("Running test \"{}\"".format(key))
        value()


def run_test(options=None, opt=None, value=None, parser=None):
    try:
        test_dict[options.run]()
    except KeyError:
        print("ERROR: Failed to find test \"{}\"".format(options.run))


def main():
    parser = OptionParser()

    # parser.add_option("-a", "--all", action="callback", callback=run_all_tests,
    #                  help="Run all available unit tests")

    parser.add_option("-r", "--run", type=str, dest="run", default=None,
                      help="Choose which unit tests to run. Usage python unit_test_manager.py -r <test>")

    parser.add_option("-l", "--list",
                      action="callback", callback=print_tests,
                      help="Print list of available unit tests. Usage python unit_test_manager.py -l")

    (options, args) = parser.parse_args(sys.argv)

    if options.run: run_test(options)
    else: run_all_tests()


if __name__ == "__main__":
    main()