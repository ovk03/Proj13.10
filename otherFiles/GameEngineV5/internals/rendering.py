"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.07
"""
import sys
from tkinter import *
from dataclasses import dataclass
import math
from GameEngineV5.mathAndStructs import *

if __name__ == "some random stuff to trick pep8 thinking that i have mathAndStructs module imported (I do)":
    from ..mathAndStructs import *


@dataclass
class draw_buffer:
    triangles = []

    def __init__(self, tris=[]):
        self.triangles = tris


def backface_culling(view_dir: Vector3, triangles: list):
    filter(lambda t: t.normal * view_dir > 0, triangles)


def frustum_culling(triangles: list):
    filter_func = lambda triangle: (-1 < triangle.vert1.x < 1 or -1 < triangle.vert1.y < 1 or 0 < triangle.vert1.z < 1) \
                             and (-1 < triangle.vert2.x < 1 or -1 < triangle.vert2.y < 1 or 0 < triangle.vert2.z < 1) \
                             and (-1 < triangle.vert3.x < 1 or -1 < triangle.vert3.y < 1 or 0 < triangle.vert3.z < 1)
    filter(filter_func, triangles)
