"""this file implements unittests"""
import pathlib
import sys

"""Onni Kolkka 
150832953 (student number)
created 11.12.2022 20.53
"""

from GameEngineV6 import *
from GameEngineV6 import _rendering
from GameEngineV6 import _tk_inter_inter
import time
import math
import pstats
import pathlib
import logging
import unittest
import cProfile
from timeit import timeit

def tri(pos):
    vert_top=(pos[0],pos[1]+0.5,pos[2])
    vert_left = (pos[0]-0.1,pos[1],pos[2]-0.1)
    vert_right = (pos[0]+0.1,pos[1],pos[2]-0.1)
    vert_back = (pos[0],pos[1],pos[2]+0.3)
    return (
        (vert_top,
        vert_left,
        vert_right),
        (vert_top,
        vert_right,
        vert_back),
        (vert_top,
        vert_back,
        vert_left))

def quad(pos):
    return (
        (pos[0]-.1,pos[1]-.1,pos[2]),
        (pos[0]+.1,pos[1]-.1,pos[2]),
        (pos[0]+.1,pos[1]+.1,pos[2]),
        (pos[0]-.1,pos[1]-.1,pos[2]),
        (pos[0]+.1,pos[1]+.1,pos[2]),
        (pos[0]-.1,pos[1]+.1,pos[2]))


def box(pos):
    _ri_up_frnt = (pos[0]+.1,pos[1]+.1,pos[2]-.1)
    _le_up_frnt = (pos[0]-.1,pos[1]+.1,pos[2]-.1)
    _ri_up_back = (pos[0]+.1,pos[1]+.1,pos[2]+.1)
    _le_up_back = (pos[0]-.1,pos[1]+.1,pos[2]+.1)

    _ri_dwn_frnt = (pos[0]+.1,pos[1]-.1,pos[2]-.1)
    _le_dwn_frnt = (pos[0]-.1,pos[1]-.1,pos[2]-.1)
    _ri_dwn_back = (pos[0]+.1,pos[1]-.1,pos[2]+.1)
    _le_dwn_back = (pos[0]-.1,pos[1]-.1,pos[2]+.1)

    #front back verts
    return ((_le_up_frnt, _ri_up_frnt , _ri_dwn_frnt),
            (_le_up_frnt, _ri_dwn_frnt, _le_dwn_frnt),
            (_ri_up_back, _le_up_back , _le_dwn_back),
            (_ri_up_back, _le_dwn_back, _ri_dwn_back),

            (_ri_up_frnt, _ri_up_back , _ri_dwn_back),
            (_ri_up_frnt, _ri_dwn_back, _ri_dwn_frnt),
            (_le_up_frnt, _le_up_back , _le_dwn_back),
            (_le_up_frnt, _le_dwn_back, _le_dwn_frnt),

            (_le_up_back,  _ri_up_back,  _ri_up_frnt),
            (_le_up_back,  _ri_up_frnt,  _le_up_frnt),
            (_le_dwn_back, _ri_dwn_back, _ri_dwn_frnt),
            (_le_dwn_back, _ri_dwn_frnt, _le_dwn_frnt))


def box_w_quads(pos):
    _ri_up_frnt = (pos[0] + .1, pos[1] + .1, pos[2] - .1)
    _le_up_frnt = (pos[0] - .1, pos[1] + .1, pos[2] - .1)
    _ri_up_back = (pos[0] + .1, pos[1] + .1, pos[2] + .1)
    _le_up_back = (pos[0] - .1, pos[1] + .1, pos[2] + .1)

    _ri_dwn_frnt = (pos[0] + .1, pos[1] - .1, pos[2] - .1)
    _le_dwn_frnt = (pos[0] - .1, pos[1] - .1, pos[2] - .1)
    _ri_dwn_back = (pos[0] + .1, pos[1] - .1, pos[2] + .1)
    _le_dwn_back = (pos[0] - .1, pos[1] - .1, pos[2] + .1)

    # front back verts
    return ((_le_up_frnt, _ri_up_frnt, _ri_dwn_frnt, _le_dwn_frnt),
            (_ri_up_back, _le_up_back, _le_dwn_back, _ri_dwn_back),

            (_ri_up_frnt, _ri_up_back, _ri_dwn_back, _ri_dwn_frnt),
            (_le_up_frnt, _le_up_back, _le_dwn_back, _le_dwn_frnt),

            (_le_up_back , _ri_up_back , _ri_up_frnt , _le_up_frnt),
            (_le_dwn_back, _ri_dwn_back, _ri_dwn_frnt, _le_dwn_frnt))

def box_w_quads_optim(pos):
    _ri_up_frnt = (pos[0] + .1, pos[1] + .1, pos[2] - .1)
    _le_up_frnt = (pos[0] - .1, pos[1] + .1, pos[2] - .1)
    _ri_up_back = (pos[0] + .1, pos[1] + .1, pos[2] + .1)
    _le_up_back = (pos[0] - .1, pos[1] + .1, pos[2] + .1)

    _ri_dwn_frnt = (pos[0] + .1, pos[1] - .1, pos[2] - .1)
    _le_dwn_frnt = (pos[0] - .1, pos[1] - .1, pos[2] - .1)
    _ri_dwn_back = (pos[0] + .1, pos[1] - .1, pos[2] + .1)
    _le_dwn_back = (pos[0] - .1, pos[1] - .1, pos[2] + .1)

    # front back verts
    return ((*_le_up_frnt, *_ri_up_frnt, *_ri_dwn_frnt, *_le_dwn_frnt),
            (*_ri_up_back, *_le_up_back, *_le_dwn_back, *_ri_dwn_back),

            (*_ri_up_frnt, *_ri_up_back, *_ri_dwn_back, *_ri_dwn_frnt),
            (*_le_up_frnt, *_le_up_back, *_le_dwn_back, *_le_dwn_frnt),

            (*_le_up_back , *_ri_up_back , *_ri_up_frnt , *_le_up_frnt),
            (*_le_dwn_back, *_ri_dwn_back, *_ri_dwn_frnt, *_le_dwn_frnt))

def grid_test_500():
    l=[]
    for x in range(-2,3):
        for y in range(-1,2):
            for z in range(-2,3):
                if x == 0 or y == 0 or z == 0:
                    pass
                l.extend(box_w_quads_optim((x,y,z)))
    for i in l:
        if type(i) is not tuple:
            raise TypeError
    return l
def grid_test_2k():
    l=[]
    for x in range(-3,4):
        for y in range(-3,4):
            for z in range(-3,4):
                if x == 0 or y == 0 or z == 0:
                    pass
                l.extend(box_w_quads_optim((x,y,z)))
    for i in l:
        if type(i) is not tuple:
            raise TypeError
    return l

def grid_test_10k():
    l=[]
    for x in range(-5,6):
        for y in range(-6,7):
            for z in range(-5,6):
                if x == 0 or y == 0 or z == 0:
                    pass
                l.extend(box_w_quads_optim((x,y,z)))
    for i in l:
        if type(i) is not tuple:
            raise TypeError
    return l


def test():
    try:
        inter=_rendering.CameraRenderOptimized()
        i=0

        print("count of polygons:")
        print(len(grid_test_10k()))
        inter.camera_rot=(0,90,0)
        # inter.render(grid_test_2k(),cache=True)
        inter.render(obj_parse(open(pathlib.Path(__file__).absolute().parent.joinpath("untitled.obj")).read()),cache=True)
        avrg_time=0.02
        t = -time.perf_counter()
        while inter.render():
            inter.camera_rot=(0,i/math.pi*3+_tk_inter_inter.GameToTK().namespace.mouse_pos_x,0)
            inter.camera_pos=(math.sin(i/180*3)*6,0,-math.cos(i/180*3)*8)
            # inter.camera_pos=(0,0,-15)
            # print(inter.camera_rot)
            i += 5
            lerp_val=0.99
            avrg_time=(t+time.time())*(1-lerp_val)+avrg_time*lerp_val
            # print(f"frame rate: {1 / (avrg_time + 1e-20)}")
            t = -time.perf_counter()
    except Exception as e:
        logging.getLogger().exception(e)
    unittest.main()

from GameEngineV6._file_helper import *

if __name__ == "__main__":
    try:
        cProfile.run("test()","testStats")
    except Exception as e:
        logging.getLogger().exception(e)
    finally:
        p = pstats.Stats('testStats')
        p.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats()


