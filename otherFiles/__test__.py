"""this file implements unittests"""
import math

"""Onni Kolkka 
150832953 (student number)
created 11.12.2022 20.53
"""

# import game engine from the game engine itself, on order to run unittests
from GameEngineV6 import *
import time
import logging
import unittest

def tri(pos):
    return Triangle(
        Vector3(pos.x,pos.y+.3,1),
        Vector3(pos.x+.2,pos.y-.2,1),
        Vector3(pos.x-.2,pos.y-.2,1),
        Vector3()
    )
def quad(pos,first=True):
    if(first):
        return [Triangle(
            Vector3(pos.x-.1,pos.y-.1,pos.z),
            Vector3(pos.x+.1,pos.y-.1,pos.z),
            Vector3(pos.x+.1,pos.y+.1,pos.z),
            Vector3()
        ),Triangle(
            Vector3(pos.x-.1,pos.y-.1,pos.z),
            Vector3(pos.x+.1,pos.y+.1,pos.z),
            Vector3(pos.x-.1,pos.y+.1,pos.z),
            Vector3()
        )]

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
    for x in range(-5,6):
        for y in range(-5,6):
            for z in range(-2,3):
                l.extend(quad(Vector3(x,y,z)))
    for i in l:
        if type(i) != Triangle:
            raise TypeError
    return l


def test():
    try:
        inter=CameraRender(pos=Vector3(0,0,-10))
        i=0

        print(len(grid_test()))
        inter.render(DrawBuffer(grid_test()))
        time.sleep(2)
        while inter.render():
            inter.camera_rot=Vector3(math.cos(i/3.3)*6,math.sin(i/7)*6,0)
            i+=1
    except Exception as e:
        logging.getLogger().exception(e)
    unittest.main()


if __name__ == "__main__":
    pass

test()

