"""this file implements unittests"""

"""Onni Kolkka 
150832953 (student number)
created 11.12.2022 20.53
"""

# import game engine from the game engine itself, on order to run unittests
from GameEngineV6 import *
import time
import math
import pstats
import logging
import unittest
import cProfile

def tri(pos):
    return [
        [pos.x,pos.y+.3,1],
        [pos.x+.2,pos.y-.2,1],
        [pos.x-.2,pos.y-.2,1]]

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
    for x in range(-5,6):
        for y in range(-5,6):
            for z in range(1,9):
                l.extend(quad([x,y,z]))
    for i in l:
        if type(i) is not list:
            raise TypeError
    return l


def test():
    try:
        inter=CameraRender(pos=[0,0,-10])
        i=0

        print(len(grid_test()))
        inter.render(grid_test())
        t=0
        while inter.render(grid_test()):
            inter.camera_rot=[math.cos(i/3.3)*6,math.sin(i/7)*6,0]
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


