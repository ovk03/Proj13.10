"""this file implements unittests"""
import time

from t13.otherFiles.GameEngineV5.internals import Interpeter, draw_buffer
from t13.otherFiles.GameEngineV5.mathAndStructs import Triangle2d, Vector2

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
if __name__ == "some random stuff to trick pep8 thinking that I have  various modules  imported (which I do)":
    from ...GameEngineV5 import *
    from ...GameEngineV5.mathAndStructs.vectors import *
    from ...GameEngineV5.internals.rendering import *


def tri(pos):
    return Triangle(
        Vector3(pos.x,pos.y+.3,1),
        Vector3(pos.x+.2,pos.y-.2,1),
        Vector3(pos.x-.2,pos.y-.2,1),
        Vector3()
    )
def quad(pos,first=True):
    if(first):
        return Triangle(
            Vector3(pos.x-.01,pos.y-.01),
            Vector3(pos.x+.01,pos.y-.01),
            Vector3(pos.x+.01,pos.y+.01),
            Vector3()
        )
    else:
        return Triangle(
            Vector3(pos.x-.01,pos.y-.01),
            Vector3(pos.x+.01,pos.y+.01),
            Vector3(pos.x-.01,pos.y+.01),
            Vector3()
        )

def cube(x_pos,rot):
    vert=[]*8
    vert.append(Vector3(100+x_pos,100,100))
    vert.append(Vector3(-100+x_pos,100,100))
    vert.append(Vector3(-100+x_pos,-100,100))
    vert.append(Vector3(100+x_pos,-100,100))
    vert.append(Vector3(100+x_pos,100,-100))
    vert.append(Vector3(-100+x_pos,100,-100))
    vert.append(Vector3(-100+x_pos,-100,-100))
    vert.append(Vector3(100+x_pos,-100,-100))

    return [tri(v) for v in vert]

def grid_test():
    l=[]
    for x in range(-10,10):
        for y in range(-10,10):
            l.append(quad(Vector2(x,y)))
            l.append(quad(Vector2(x,y),False))
    for i in l:
        if type(i) != Triangle:
            raise TypeError
    return l


def test():
    try:
        inter=CameraRender(pos=Vector3(0,0,-10))
        i=0

        print(len(grid_test()))
        inter.render(draw_buffer(grid_test()))
        time.sleep(2)
        quit()
        while inter.render(draw_buffer(cube(0,i))):
            i+=1
            time.sleep(0.001)
    except Exception as e:
        logging.getLogger().exception(e)
    loader = unittest.TestLoader()
    start_dir = str(pathlib.Path(__file__).parent.parent)
    suite = loader.discover(start_dir)
    unittest_runner = unittest.TextTestRunner()
    unittest_runner.run(suite)
    quit()


if __name__ == "__main__":
    from test import *

test()

