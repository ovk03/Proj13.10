"""[insert short description here]"""
"""Onni Kolkka 
150832953 (student number)
created 12.12.2022 20.31
"""

"""I believe this code is really self explanatory
so added comments would only make reading harder for the most part"""

from dataclasses import dataclass
import unittest
import math
import logging
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent))
# this throws error but runs just fine. This is probably not good, but this is the unittest solution for this project
# its not like anyone will ever see my terrible game engine structure :) oh wait.
from vectors import *

if __name__ == "some random stuff to trick pep8 thinking that i have GameEngine module imported (I do)":
    from .vectors import *


@dataclass
class Matrix4x4:
    def __init__(self, *args, suppress=False, eye=False):

        if eye:
            for i in range(4 * 4):
                # creates eye matrix
                setattr(self, f"m{i % 4}{int(i / 4)}", 1.0 if int(i / 4) == i % 4 else 0.0)
            return

        elif len(args) != 4 * 4:
            if not suppress:
                if len(args)>0:
                    raise Exception("\33[31mCreating Matrix with too few values "
                                    "\33[33m(filled rest of the matrix with 0.0)\33[0m")

            # fills matrix so it contains every elements
            args += tuple([0.0] * (4 * 4 - len(args)))

        for number, value in enumerate(args, start=0):
            setattr(self, f"m{number % 4}{int(number / 4)}", value)
            # this result in attributes like   matrix.m10  matrix.m03  matrix.m33

    def __eq__(self, other):
        # guard clause for different data type
        if type(other) != type(self):
            return False

        if other.x == self.x and \
                other.y == self.y and \
                other.z == self.z and \
                other.w == self.w:
            return True

        else:
            return False

    def __mul__(self, other):
        if type(other) == Matrix4x4:
            pass
        elif type(other) == Vector4:
            pass


# region uTest
class matrices_unit_test(unittest.TestCase):
    def test_dot(self):

        self.assertIs(type(Matrix4x4(suppress=True)), Matrix4x4)
        self.assertIs(type(Matrix4x4(eye=True)), Matrix4x4)

        # too few args should throw error
        self.assertRaises(Exception,Matrix4x4,1)

# endregion
