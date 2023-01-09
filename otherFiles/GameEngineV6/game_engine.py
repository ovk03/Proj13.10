"""Main script keeping track of game world"""

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 14.54
"""
from .__main__ import *
import unittest
import functools
import time
import abc




"""===============metaclass for gameobjects======================"""


class GameObject(EngineType):
    """This is a metaclass used by gameobjects."""


    # inherit EngineType stuff
    def __new__(mcs, name, bases, dct): return EngineType.__new__(mcs, name, bases, dct)

    def __del__(cls): EngineType.__del__(cls)

    def __call__(cls, *args, **kwargs): EngineType.__call__(cls, *args, **kwargs)



"""===============Singleton for gameobjects======================="""


class GameObjectSingleton(GameObject):
    """This is a metaclass used by Everything.
    It differs from a normal class in many useful ways.
    In this case it is used to implement Global like functionality without actually using Global variables"""

    singletons = {}

    # inherit EngineType stuff
    def __new__(mcs, name, bases, dct):
        return GameObject.__new__(mcs, name, bases, dct)

    def __del__(cls):
        GameObject.__del__(cls)

    def __call__(cls, *args, **kwargs):
        # does class instance exist yet?
        if cls not in cls.singletons:
            cls.singletons[cls] = super(GameObject, cls).__call__(*args, **kwargs)

        # is that instance working?  this is a case that shouldn't happen often
        elif hasattr(cls.singletons[cls], "is_working") and cls.singletons[cls].is_working:
            logging.warning(f"Singleton of: {cls.__name__} not working, but alive")
            cls.singletons[cls].__del__()
            cls.singletons[cls] = super(GameObject, cls).__call__(*args, **kwargs)

        # if all good, return singelton
        return cls.singletons[cls]

"""=================World update cycles========================="""


class GameEngine(EngineTypeSingleton):
    def __init__(self,game_manager:GameObjectSingleton):
        pass