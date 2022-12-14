"""this file implements unittests"""

"""Onni Kolkka 
150832953 (student number)
created 11.12.2022 20.53
"""

from GameEngineV6 import *
import time
import math
import pstats
import logging
import unittest
import cProfile

def tri(pos):
    vert_top=[pos[0],pos[1]+0.5,pos[2]]
    vert_left = [pos[0]-0.1,pos[1],pos[2]-0.1]
    vert_right = [pos[0]+0.1,pos[1],pos[2]-0.1]
    vert_back = [pos[0],pos[1],pos[2]+0.3]
    return [
        vert_top,
        vert_left,
        vert_right,
        vert_top,
        vert_right,
        vert_back,
        vert_top,
        vert_back,
        vert_left]

def quad(pos):
    return [
        [pos[0]-.1,pos[1]-.1,pos[2]],
        [pos[0]+.1,pos[1]-.1,pos[2]],
        [pos[0]+.1,pos[1]+.1,pos[2]],
        [pos[0]-.1,pos[1]-.1,pos[2]],
        [pos[0]+.1,pos[1]+.1,pos[2]],
        [pos[0]-.1,pos[1]+.1,pos[2]]]



def grid_test():
    l=[]
    for x in range(-3,4):
        for y in range(-3,4):
            for z in range(-3,4):
                l.extend(tri([x,y,z]))
    for i in l:
        if type(i) is not list:
            raise TypeError
    return l


def test():
    try:
        inter=CameraRender()
        i=0

        print(len(grid_test()))
        inter.camera_rot=[0,90,0]
        inter.render(grid_test())
        time.sleep(1)
        t=0
        while inter.render(grid_test()):
            inter.camera_rot=[0,i*5+90,0]
            # print(inter.camera_rot)
            print(f"frame rate: {1 / (t + time.time()+1e-20)}")
            t = -time.time()
            i += 1
    except Exception as e:
        logging.getLogger().exception(e)
    unittest.main()


if __name__ == "__main__":
    pass
cProfile.run("test()","testStats")
p = pstats.Stats('testStats')
p.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats()


