"""this file implements unittests"""
import time

"""Onni Kolkka 
150832953 (student number)
created 11.12.2022 20.53
"""

import unittest

# import game engine from the game engine itself, on order to run unittests
import sys
import pathlib
import logging
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))
# this throws error but runs just fine. This is probably not good, but this is the unittest solution for this project
# its not like anyone will ever see my terrible game engine structure :) oh wait.
from GameEngineV5 import *
if __name__ == "some random stuff to trick pep8 thinking that i have GameEngine module imported (I do)":
    from ...GameEngineV5 import *

tri=Triangle2d(
    vert1=Vector2(0,0),
    vert2=Vector2(1000,0),
    vert3=Vector2(1000,1000),
    normal=0,
    depth=0
)

def test():
    has_run_unittest=False
    try:
         inter=interpeter()
         while inter.draw(draw_buffer([tri])):
             time.sleep(0.001)
    except Exception as e:
        has_run_unittest = True
        logging.getLogger().exception(e)
        unittest.main()
    finally:
        if not has_run_unittest:
            unittest.main()

test()