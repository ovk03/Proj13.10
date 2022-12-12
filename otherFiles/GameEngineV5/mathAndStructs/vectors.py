"""Handles vector types and their math"""

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 19.41
"""

"""I believe this code is really self explanatory
so added comments would only make reading harder for the most part"""

from dataclasses import dataclass
import unittest
import math


# region vect
@dataclass
class Vector2:

    def __init__(self, x=float(0), y=float(0)):
        self.x = x
        self.y = y
    def __eq__(self, other):
        # guard clause for different data type
        if type(other) != type(self):
            return False

        if other.x == self.x and other.y == self.y:
            return True

        else:
            return False


@dataclass
class Vector3:

    def __init__(self, x=float(0), y=float(0), z=float(0)):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        # guard clause for different data type
        if type(other) != type(self):
            return False

        if other.x == self.x and \
                other.y == self.y and \
                other.z == self.z:
            return True

        else:
            return False


@dataclass
class Vector4:

    def __init__(self, x=float(0), y=float(0), z=float(0), w=float(0)):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

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


# endregion

# region tris
@dataclass
class Triangle2d:
    vert1 = Vector2()
    vert2 = Vector2()
    vert3 = Vector2()
    normal = float(0)
    depth = float("inf")

    def __init__(self, vert1, vert2, vert3, normal=float(0), depth=float("inf")):
        self.vert1 = vert1
        self.vert2 = vert2
        self.vert3 = vert3
        self.normal = normal
        self.depth = depth

    def toArray(self):
        return self.vert1.x, self.vert1.y, \
               self.vert2.x, self.vert2.y, \
               self.vert3.x, self.vert3.y

    def __eq__(self, other):
        # guard clause for different data type
        if type(other) != type(self):
            return False

        # comparison
        if other.normal == self.normal and \
                other.vert1 == self.vert1 and \
                other.vert2 == self.vert2 and \
                other.vert3 == self.vert3:
            return True

        else:
            return False


@dataclass
class Triangle:
    vert1 = Vector3()
    vert2 = Vector3()
    vert3 = Vector3()
    normal = Vector3()
    depth = float("inf")

    def __init__(self, vert1, vert2, vert3, normal, depth=float("inf")):
        self.vert1 = vert1
        self.vert2 = vert2
        self.vert3 = vert3
        self.normal = normal
        self.depth = depth

    def __eq__(self, other):
        # guard clause for different data type
        if type(other) != type(self):
            return False

        # comparison
        if other.normal == self.normal and \
                other.vert1 == self.vert1 and \
                other.vert2 == self.vert2 and \
                other.vert3 == self.vert3:
            return True

        else:
            return False


# endregion

# region math
def dot(a, b) -> float:
    """Dot product of any two vectors
    (of same type)"""

    # guard clause for mismatch type
    if type(a) != type(b):
        raise TypeError

    # apparently this was retuning ints, so now they are cast into floats
    if type(a) == Vector2:
        return float(_dot2(a, b))
    if type(a) == Vector3:
        return float(_dot3(a, b))
    if type(a) == Vector4:
        return float(_dot4(a, b))
    else:
        raise TypeError


def _dot2(a: Vector2, b: Vector2) -> float:
    return a.x*b.x + a.y*b.y


def _dot3(a: Vector3, b: Vector3) -> float:
    return a.x*b.x + a.y*b.y + a.z*b.z


def _dot4(a: Vector4, b: Vector4) -> float:
    return a.x*b.x + a.y*b.y + a.z*b.z + a.w*b.w


def cross(a: Vector3, b: Vector3) -> Vector3:
    """Simple cross product of two Vector3"""

    # guard clause for mismatch type
    if type(a) != type(b) or type(b) != Vector3:
        raise TypeError

    # https://en.wikipedia.org/wiki/Cross_product
    return Vector3(
        a.y * b.z - a.z * b.y,
        a.z * b.x - a.x * b.z,
        a.x * b.y - a.y * b.x)


# endregion

# region uTest
class vectors_unit_test(unittest.TestCase):
    def test_dot(self):
        a2 = Vector2(1, 2)
        b2 = Vector2(1, 0)

        a3 = Vector3(1, 2, 0)
        b3 = Vector3(1, 0, 1)

        a4 = Vector4(1, 2, 0, 1)
        b4 = Vector4(1, 0, 1, 0)

        test = lambda a, b: self.assertEqual(type(dot(a,b)),float)
        test(a2, b2)
        test(a3, b3)
        test(a4, b4)

        test = lambda a, b: self.assertEqual(type(cross(a, a)),Vector3)

        test(a3, b3)
        test(b3, a3)
# endregion