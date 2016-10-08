from tester import HW_Tester

import sys

def main(*args):
    try:
        if args[0] == "init":
            t = HW_Tester(init=True)
    except:
        t = HW_Tester()

    t.import_test_file()
    t.test_module()

main(*tuple(sys.argv[1:]))

"""
FEATURES (that need to be implemented:
- check for docstring

"""