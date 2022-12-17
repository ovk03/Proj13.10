"""
This is the main entry point to the game_scripts engine, when run as code:
for example though pycharm console with: "python [[path to this directory]]\\GameEngineV5"
"""
import logging

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 14.59
"""
import platform

# simple function to define if audio and mouse control is available
# is_windows lambda:True if platform().lower().__contains__("windows")else False
def is_windows():return True if platform.platform().lower().__contains__("windows")else False

if __name__ == "__main__":
    # import test without relative path
    import sys
    import pathlib
    sys.path.append(str(pathlib.Path().absolute().parent))
    try:
        from __test__ import test
        test()
    except ModuleNotFoundError:
        logging.getLogger().error("External test failed to run. Make sure the test file exists and contains function \"test\"")