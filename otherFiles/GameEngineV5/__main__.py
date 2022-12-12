"""
This is the main entry point to the game_scripts engine, when run as code:
for example though pycharm console with: "python [[path to this directory]]\\GameEngineV5"
"""

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 14.59
"""





if __name__ == "__main__":
    # import test without relative path
    import sys
    import pathlib
    sys.path.append(str(pathlib.Path().absolute().parent))
    import test
    quit()