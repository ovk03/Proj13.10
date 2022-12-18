"""
This is the main entry point to the game_scripts engine, when run as code:
for example though pycharm console with: "python [[path to this directory]]\\GameEngineV5"
"""

import platform
import logging
import inspect

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 14.59
"""


# Dictionary containing the most common 16:9 resolutions, These correspond to specific files in data.
COMMON_SCREEN_RESOLUTIONS = {640:360,1600:900,1920:1080}
POLYGON_COUNT = 2**12
FRAME_RATE_LOG_FREQUENCY = 100
DEBUG_GAME_ENGINE = True
EXTRA_DEBUG_GAME_ENGINE = True

class EngineType(type):
    """This is a metaclass used by Everything.
    It differs from a normal class in many useful ways.
    In this case it is used to implement Global like functionality without actually using Global variables"""

    is_windows = False
    is_working = True
    run_count = 0
    debug = True

    def __new__(mcs, name, bases, dct):
        obj = type.__new__(mcs, name, bases, dct)
        # simple function to define if audio and mouse control is available
        obj.is_windows = True if platform.platform().lower().__contains__("windows") else False
        obj.run_count = 0
        setattr(obj, mcs.log.__name__, mcs.log)
        setattr(obj, mcs.log_func.__name__, mcs.log_func)
        setattr(obj, mcs.link.__name__, mcs.link)
        obj.debug = DEBUG_GAME_ENGINE
        return obj

    def __del__(cls):
        cls.is_working = False
        # this super call doesn't exist oops
        # super().__del__(cls)

    # @ staticmethod # this way no class reference needs to be passed
    # NVM in need it to be passed
    def log_func(cls,func,verbose=False):
        import time
        def wrapper(*args, **kwargs):
            t1 = -time.perf_counter()
            result = func(*args, **kwargs)
            t1 += time.perf_counter()
            if verbose:
                print(
                    f"function: \"{func.__name__}\" executed"+
                    "" if t1 < 0.01 else f"executed in {t1}" + "\n"+
                    f"with args: {args, kwargs}" if len(args) + len(kwargs) > 0 else ""+
                    f"total run count: {cls.run_count}")
            cls.run_count += 1
            return result
        return wrapper

    # @ staticmethod # this way no class reference needs to be passed
    # NVM in need it to be passed
    def log(cls, msg:str, *codes):
        try:
            # whether to add link to print line at the end of the log
            should_link = EXTRA_DEBUG_GAME_ENGINE
            if codes.__contains__("LINK"):
                should_link = True
                codes = filter(lambda a: a != "LINK", codes)

            # https://en.wikipedia.org/wiki/ANSI_escape_code
            # ANSI escape codes
            __color = {"PINK":95,"BLUE":94,"GREEN":92,"RED":91,"BOLD":1,
                       "UNDERLINE":4,"WHITE":97,"YELLOW":93,"CYAN":96,"ITALIC":3,
                       "OVER":9,"BOX":51,"BLACK":30,"BLACKBG":40,"REDBG":41,
                       "GREENBG":42,"YELLOWBG":43,"BLUEBG":44,"WHITEBG":47,"COLORBG":7}
            for color in codes:
                color=str(color)
                if cls.debug:
                    if color in __color.keys():
                        print(f"\033[{__color[color]}m",end="")
                    elif len(color) <= 2:
                        print(f"\033[{color}m",end="")
                    else:
                        print(color,end="")
            print(str(msg)+"\033[0m",end="")

            # link or not to link
            if should_link:
                cf = inspect.currentframe().f_back
                print(f' File "{inspect.getframeinfo(cf).filename}", line {max(inspect.getframeinfo(cf).lineno, 1)}'.replace("\\", "/"))
            else:
                print()

        except TypeError as e:
            print(f"\033[0m\33[91mType can't be converted to string. ({e})\033[0m")
            cf = inspect.currentframe().f_back
            print(f' File "{inspect.getframeinfo(cf).filename}", line {max(inspect.getframeinfo(cf).lineno, 1)}'.replace("\\", "/"))
            print()

        except Exception as e:
            print(f"\033[0m\33[91mType can't be converted to string. ({e})\033[0m")
            cf = inspect.currentframe().f_back
            print(f' File "{inspect.getframeinfo(cf).filename}", line {max(inspect.getframeinfo(cf).lineno, 1)}'.replace("\\", "/"))
            print()

    # @ staticmethod # this way no class reference needs to be passed
    # NVM in need it to be passed
    def link(cls):
        cf = inspect.currentframe().f_back
        print(f'File "{inspect.getframeinfo(cf).filename}", line {max(inspect.getframeinfo(cf).lineno, 1)}'.replace("\\", "/"))


class EngineTypeSingleton(EngineType):
    """This is a metaclass used by Everything.
    It differs from a normal class in many useful ways.
    In this case it is used to implement Global like functionality without actually using Global variables"""

    singletons = {}

    # inherit EngineType stuff
    def __new__(mcs, name, bases, dct): return EngineType.__new__(mcs, name, bases, dct)

    def __del__(cls): EngineType.__del__(cls)

    def __call__(cls, *args, **kwargs):
        # does class instance exist yet?
        if cls not in cls.singletons:
            print("meta: creating new singleton")
            cls.singletons[cls] = super(EngineType, cls).__call__(*args, **kwargs)

        # is that instance working?  this is a case that shouldn't happen often
        elif hasattr(cls.singletons[cls],"is_working") and cls.singletons[cls].is_working:
            logging.warning(f"Singleton of: {cls.__name__} not working, but alive")
            cls.singletons[cls].__del__()
            cls.singletons[cls] = super(EngineType, cls).__call__(*args, **kwargs)

        # if all good, return singelton
        return cls.singletons[cls]


# simple function to define if audio and mouse control is available
class IsWindows:
    def __getattr__(self):
        return True if platform.platform().lower().__contains__("windows") \
            else False

    def __setattr__(self, key, value):
        logging.getLogger().error("Tried to modify readonly class attribute")


if __name__ == "__main__":
    # import test without relative path
    # FIXME: find a way to make this better. Luckily this version of module doesn't depend on this kind of structure, like the last one
    import sys
    import pathlib
    sys.path.append(str(pathlib.Path().absolute().parent))
    try:
        from __test__ import test
        test()
        test()
    except ModuleNotFoundError:
        logging.getLogger().error("External test failed to run. Make sure the test file exists and contains function \"test\"")