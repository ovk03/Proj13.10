"""this file implements unittests"""
import pathlib
import sys
from GameEngineV6 import *
from GameEngineV6 import structures
from GameEngineV6._rendering import *
from GameEngineV6._game_to_tk import *
from GameEngineV6._input import *
import time
import math
import pstats
import pathlib
import logging
import unittest
import cProfile

"""Onni Kolkka 
150832953 (student number)
created 11.12.2022 20.53
"""

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
                l.extend(box_w_quads_optim((x, y, z)))
    for i in l:
        if type(i) is not tuple:
            raise TypeError
    return l

def test():
    try:
        t=-time.perf_counter()
        # world doesn't change, so we only pass data over once
        Camera.render(obj_parse(pathlib.Path(__file__).absolute().parent.joinpath("untitled.obj")))
        x_rot=0
        y_rot=0
        while Camera.render():

            # time
            delta_t=t+time.perf_counter()
            t = -time.perf_counter()


            if(Input.key_dwn("Escape")):
                Input.mouse_lock_switch()
            Input.update()

            # input
            y_input = 1 if Input().key('w') else 0
            y_input-= 1 if Input().key('s') else 0
            x_input = 1 if Input().key('a') else 0
            x_input-= 1 if Input().key('d') else 0
            z_input = 1 if Input().key('q') else 0
            z_input-= 1 if Input().key('e') else 0
            if(Input().key("Shift_L")):
                x_input*=15
                y_input*=15
                z_input*=15
                x_rot -= Input.mouse("x") / 3
                y_rot += Input.mouse("y") / 3
            else:
                x_rot -= Input.mouse("x") / 10
                y_rot += Input.mouse("y") / 10

            new_pos=structures.vec_rotate_inverse(
                Camera.get_rot(),
                (x_input,z_input,y_input))

            Camera.set_rot((y_rot,x_rot,0))
            Camera.incr_pos(new_pos)

    except Exception as e:
        logging.getLogger().exception(e)
    cProfile.run("unittest.main()","unittest")

from GameEngineV6._file_helper import *

if __name__ == "__main__":
    try:
        cProfile.run("test()","testStats")
        p = pstats.Stats('testStats')
        print("\33[94m")
        p.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats(25)
        print("\33[0m\33[92m\33[7m\33[1m（ ^_^）!!!EVERYTHIN WORKED!!! ヽ(´▽`)/\33[0m")
    except Exception as e:
        logging.getLogger().exception(e)
        p = pstats.Stats('testStats')
        print("\33[94m")
        p.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats(25)


