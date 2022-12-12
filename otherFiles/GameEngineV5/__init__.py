"""
This is the main entry point to the game_scripts engine, when imported as a package
"""

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 13.24
"""

if __name__ == "__main__":
    # import test without relative path
    import sys
    import pathlib
    sys.path.append(str(pathlib.Path().absolute().parent))
    import test
    quit()

else:
    # imported as a package and not ran as code
    from .internals import *
    from .mathAndStructs import *
    from .engine import *