"""
This is the main entry point to the game_scripts engine, when run as code:
for example though pycharm console with: "python [[path to this directory]]\\GameEngineV5"
"""

import platform
import logging

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 14.59
"""


class EngineType(type):
    """This is a metaclass used by Everything.
    It differs from a normal class in many useful ways.
    In this case it is used to implement Global like functionality without actually using Global variables"""

    # simple function to define if audio and mouse control is available
    is_windows = False
    is_working = True
    singletons = {}
    run_count = 0

    def __new__(mcs, name, bases, dct):
        print("meta: creating %s %s" % (name, bases))
        obj = type.__new__(mcs, name, bases, dct)
        obj.is_windows = True if platform.platform().lower().__contains__("windows") else False
        obj.run_count = 0
        return obj

    def __del__(cls):
        if cls in cls.singletons:
            cls.singletons.pop(cls)
        cls.is_working = False
        # this super call doesn't exist oops
        # super().__del__(cls)

    def __call__(cls, *args, **kwargs):
        # does class instance exist yet?
        if cls not in cls.singletons:
            cls.singletons[cls] = super(EngineType, cls).__call__(*args, **kwargs)

        # is that instance working?  this is a case that shouldn't happen often
        elif not cls.singletons[cls].is_working:
            logging.warning(f"Singleton of: {cls.__name__} not working, but alive")
            cls.singletons[cls].__del__()
            cls.singletons[cls] = super(EngineType, cls).__call__(*args, **kwargs)

        # if all good, return singelton
        return cls.singletons[cls]

    # @ staticmethod # this way no class reference needs to be passed
    # NVM in need it to be passed
    def log(cls,func,verbose=False):
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
    except ModuleNotFoundError:
        logging.getLogger().error("External test failed to run. Make sure the test file exists and contains function \"test\"")