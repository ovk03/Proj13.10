"""Initialize the module"""

import unittest
import logging
import cProfile

"""Onni Kolkka 
150832953 (student number)
created 14.12.2022 0.14
"""

def utest():unittest.main()

if __name__ == "__main__":
    try:
        print("\33[94mHi welcome to my little gaem enige, i maed it myself （ ^_^）")
        print("\33[1m\33[4mBe sure to read the documetation before getting overwhelmed by my spaghetti code")
        print("\n\33[0m\33[93m\33[7mRunning Unittests:\33[0m")
        cProfile.run("utest()","unittest")

        print(f"\33[0m\33[92m\33[7m\33[1m\n{' '*20}!!!EVERYTHIN WORKED!!! ヽ(´▽`)/\n\n\33[0m")
    except Exception as e:
        logging.getLogger().exception(e)
        print("\33[0m\n\33[91m\33[7m\33[1m!!!SOMETHINGS WRONG!!! (╯°□°）╯︵ ┻━┻  \33[0m")
        quit()

    if str(input("\n\33[4mShall I run a test scene for this module? (y/n) ")).lower().strip() != "y":
        quit()

    # import test without relative path
    # FIXME: find a way to make this better. Luckily this version of module doesn't depend on this kind of structure, like the last one
    import sys
    import pathlib
    sys.path.append(str(pathlib.Path().absolute().parent))
    try:
        from __test__ import test
        test()
    except ModuleNotFoundError:
        logging.getLogger().error("External test failed to run. Make sure the test file exists and contains function \"test\"")
