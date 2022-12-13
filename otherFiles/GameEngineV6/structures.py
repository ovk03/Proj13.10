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
import functools
import logging


# region vect
@dataclass
class Vector2:

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other)->bool:
        # guard clause for different data type
        if type(other) != type(self):
            return False

        if math.isclose(other.x,self.x,abs_tol=1e-12) and math.isclose(other.y,self.y,abs_tol=1e-12):
            return True

        else:
            return False


    def __mul__(self, other):
        if type(other) is Vector2:
            return float(self.x * other.x + self.y * other.y)
        elif type(other) is float:
            return Vector2(self.x * other,
                           self.y * other)
        else:
            raise TypeError

    def __add__(self, other):
        # guard clause
        if type(other) != type(self):
            raise TypeError

        return Vector2(self.x + other.x,
                       self.y + other.y)

    def __repr__(self):
        return f"{self.x:.2f} :  {self.y:.2f}"


@dataclass
class Vector3:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __eq__(self, other)->bool:
        # guard clause for different data type
        if type(other) != type(self):
            return False

        if math.isclose(other.x,self.x,abs_tol=1e-12) and \
                math.isclose(other.y,self.y,abs_tol=1e-12) and \
                math.isclose(other.z,self.z,abs_tol=1e-12):
            return True

        else:
            return False

    def __mul__(self, other):
        if type(other) is Vector3:
            return float(self.x * other.x + self.y * other.y + self.z * other.z)
        elif type(other) is float:
            return Vector3(self.x * other,
                           self.y * other,
                           self.z * other)
        else:
            raise TypeError

    def __add__(self, other):
        # guard clause
        if type(other) != type(self):
            raise TypeError(f"{type(other).__name__} is not Vector3")

        return Vector3(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z)

    def __repr__(self):
        return f"{self.x:.2f} :  {self.y:.2f} :  {self.z:.2f}"

    def vec2(self,drop_y=False):
        if drop_y:
            return Vector2(self.x,self.z)
        else:
            return Vector2(self.x,self.y)

    def vec4(self):
        return Vector4(self.x, self.y, self.z,1)

@dataclass
class Vector4:

    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    def __eq__(self, other)->bool:
        # guard clause for different data type
        if type(other) != type(self):
            return False
        if math.isclose(other.x,self.x,abs_tol=1e-12) and \
                math.isclose(other.y,self.y,abs_tol=1e-12) and \
                math.isclose(other.z,self.z,abs_tol=1e-12) and \
                math.isclose(other.w,self.w,abs_tol=1e-12):
            return True

        else:
            return False

    def __mul__(self, other):
        if type(other) is Matrix4x4:
            # as multiplication order doesn't matter, let's just let matrices handle this
            return other*self
        elif type(other) is float:
            return Vector4(self.x * other,
                           self.y * other,
                           self.z * other,
                           self.w * other)
        elif type(other) is Vector4:
            return float(self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w)
        else:
            raise TypeError


    def __add__(self, other):
        # guard clause
        if type(other) != type(self):
            raise TypeError

        return Vector4(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z,
                       self.w + other.w)

    def vec2(self,drop_y=False):
        if drop_y:
            return Vector2(self.x,self.z)
        else:
            return Vector3(self.x,self.y)

    def vec3(self):
        return Vector3(self.x, self.y,self.z)

    def __repr__(self):
        return f"{self.x:.2f} :  {self.y:.2f} :  {self.z:.2f} :  {self.w:.2f}"


# endregion

# region matrix

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
                if len(args) > 0:
                    raise Exception("\33[31mCreating Matrix with too few values "
                                    "\33[33m(filled rest of the matrix with 0.0)\33[0m")

            # fills matrix so it contains every elements
            args += tuple([0.0] * (4 * 4 - len(args)))

        for number, value in enumerate(args, start=0):
            setattr(self, f"m{number % 4}{int(number / 4)}", value)
            # this result in attributes like   matrix.m10  matrix.m03  matrix.m33

    def __eq__(self, other) -> bool:
        # guard clause for different data type
        if type(other) != type(self):
            return False

        for number in range(4*4):
            if getattr(self, f"m{number % 4}{int(number / 4)}") != getattr(self, f"m{number % 4}{int(number / 4)}"):
                return False
        else:
            return True


    # @functools.cache
    def m4x4_times_m4x4(first, second):
        # as we only allow 4x4 matrices, every matrix multiplication is always possible
        calc = lambda x, y, n: getattr(first, f"m{x}{n}") * getattr(second, f"m{n}{y}")

        # writing out the for loop to maybe get extra performance. pythons performance is pretty poor anyway
        value_list = [
            calc(0, 0, 0) + calc(0, 0, 1) + calc(0, 0, 2) + calc(0, 0, 3),
            calc(1, 0, 0) + calc(1, 0, 1) + calc(1, 0, 2) + calc(1, 0, 3),
            calc(2, 0, 0) + calc(2, 0, 1) + calc(2, 0, 2) + calc(2, 0, 3),
            calc(3, 0, 0) + calc(3, 0, 1) + calc(3, 0, 2) + calc(3, 0, 3),

            calc(0, 1, 0) + calc(0, 1, 1) + calc(0, 1, 2) + calc(0, 1, 3),
            calc(1, 1, 0) + calc(1, 1, 1) + calc(1, 1, 2) + calc(1, 1, 3),
            calc(2, 1, 0) + calc(2, 1, 1) + calc(2, 1, 2) + calc(2, 1, 3),
            calc(3, 1, 0) + calc(3, 1, 1) + calc(3, 1, 2) + calc(3, 1, 3),

            calc(0, 2, 0) + calc(0, 2, 1) + calc(0, 2, 2) + calc(0, 2, 3),
            calc(1, 2, 0) + calc(1, 2, 1) + calc(1, 2, 2) + calc(1, 2, 3),
            calc(2, 2, 0) + calc(2, 2, 1) + calc(2, 2, 2) + calc(2, 2, 3),
            calc(3, 2, 0) + calc(3, 2, 1) + calc(3, 2, 2) + calc(3, 2, 3),

            calc(0, 3, 0) + calc(0, 3, 1) + calc(0, 3, 2) + calc(0, 3, 3),
            calc(1, 3, 0) + calc(1, 3, 1) + calc(1, 3, 2) + calc(1, 3, 3),
            calc(2, 3, 0) + calc(2, 3, 1) + calc(2, 3, 2) + calc(2, 3, 3),
            calc(3, 3, 0) + calc(3, 3, 1) + calc(3, 3, 2) + calc(3, 3, 3)
        ]

        return Matrix4x4(*value_list)

    # @functools.cache
    def m4x4_times_v4(first, second: Vector4) -> Vector4:
        # as we only allow 4x4 matrices, every matrix multiplication is always possible
        calc = lambda x, vector_value, n: getattr(first, f"m{x}{n}") * vector_value

        # writing out the for loop to maybe get extra performance. pythons performance is pretty poor anyway
        value_list = [
            calc(0, second.x, 0) + calc(0, second.y, 1) + calc(0, second.z, 2) + calc(0, second.w, 3),
            calc(1, second.x, 0) + calc(1, second.y, 1) + calc(1, second.z, 2) + calc(1, second.w, 3),
            calc(2, second.x, 0) + calc(2, second.y, 1) + calc(2, second.z, 2) + calc(2, second.w, 3),
            calc(3, second.x, 0) + calc(3, second.y, 1) + calc(3, second.z, 2) + calc(3, second.w, 3)
        ]

        return Vector4(*value_list)

    # @functools.cache
    def __mul__(self, other):
        if type(other) == Matrix4x4:
            return self.m4x4_times_m4x4(other)
        elif type(other) == Vector4:
            return self.m4x4_times_v4(other)
        else:
            raise TypeError

# endregion

# region tris
@dataclass
class Triangle2d:
    vert1 = Vector2()
    vert2 = Vector2()
    vert3 = Vector2()
    normal = 0.0
    depth = float("inf")

    def __init__(self, vert1, vert2, vert3, normal=0.0, depth=float("inf")):
        self.vert1 = vert1
        self.vert2 = vert2
        self.vert3 = vert3
        self.normal = normal
        self.depth = depth

    def toArray(self):
        return self.vert1.x, self.vert1.y, \
               self.vert2.x, self.vert2.y, \
               self.vert3.x, self.vert3.y

    def __eq__(self, other)->bool:
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

    def __eq__(self, other)->bool:
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

# region renderingData
@dataclass
class DrawBuffer:
    triangles = []

    def __init__(self, tris=[]):
        self.triangles = tris

    def project(self,projection):
        new_buffer = DrawBuffer(self.triangles)
        return new_buffer

# endregion


# region math
def dot(a, b) -> float:
    """Dot product of any two vectors
    (of same type)"""
    return a*b
    #
    # # guard clause for mismatch type
    # if type(a) != type(b):
    #     raise TypeError
    #
    # # apparently this was retuning ints, so now they are cast into floats
    # if type(a) == Vector2:
    #     return float(_dot2(a, b))
    # if type(a) == Vector3:
    #     return float(_dot3(a, b))
    # if type(a) == Vector4:
    #     return float(_dot4(a, b))
    # else:
    #     raise TypeError


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


def rot(vector_to_rotate, *args):
    # first parse args in this case we need to do more work than in "dot", as we might have one or two vectors and float
    if type(args[1]) == float or int:
        angle = args[1]
    elif type(args[1]) == Vector2 and type(args[2]) == float:
        angle = args[2]
        axis_vector = args[1]
    else:
        print(vector_to_rotate, args[1])
        raise TypeError

    if type(args[-1]) == bool:
        angle = math.radians(angle) if args[-1] else angle
    if not hasattr("", "axis_vector"):
        return _rot2d(vector_to_rotate, angle)
    else:
        return _rot3d()  # TODO: not implemented


def _rot2d(vector, angle):
    # https://en.wikipedia.org/wiki/Rotation_matrix
    x = vector.x * math.cos(angle) - vector.y * math.sin(angle)
    y = vector.x * math.sin(angle) + vector.y * math.cos(angle)
    return Vector2(x, y)


def _rot3d(vector_to_rot, axis_vector, angle):
    # TODO: can you figure out what is missing? :-)
    return vector_to_rot


# endregion

# region uTest
class vectors_unit_test(unittest.TestCase):
    def test(self):
        a2 = Vector2(1, 2)
        b2 = Vector2(1, 0)

        a3 = Vector3(1, 2, 0)
        b3 = Vector3(1, 0, 1)

        a4 = Vector4(1, 2, 0, 1)
        b4 = Vector4(1, 0, 1, 0)

        test = lambda a, b: self.assertIs(type(dot(a, b)), float)
        test(a2, b2)
        test(a3, b3)
        test(a4, b4)

        test = lambda a, b: self.assertIs(type(cross(a, b)), Vector3) \
                            and self.assertIs(type(cross(a, a)), Vector3(0, 0)) \
                            and self.assertIs(type(cross(b, b)), Vector3(0, 0))

        test(a3, b3)
        test(b3, a3)

        test = lambda a, b, rad=False: self.assertIs(type(rot(a, a, rad)), Vector2)

        test(a2, math.pi, True)
        test(a2, 90)
        test(b2, math.pi * 3, True)
        test(b2, 75)

# endregion


# region uTest
class matrices_unit_test(unittest.TestCase):
    def test(self):
        self.assertIs(type(Matrix4x4(suppress=True)), Matrix4x4)
        self.assertIs(type(Matrix4x4(eye=True)), Matrix4x4)

        # too few args should throw error
        self.assertRaises(Exception, Matrix4x4, 1)

        # matrices can only be multiplied with vector4
        test_func = lambda vector: Matrix4x4(eye=True) * vector
        self.assertRaises(TypeError, test_func, Vector2(1, 1))
        self.assertRaises(TypeError, test_func, Vector3(1, 1, 1))

        # testing with eye matrix
        self.assertEqual(test_func(Vector4(1, 1, 1, 1)), Vector4(1, 1, 1, 1))
        self.assertEqual(test_func(Matrix4x4(1,1,1,1,1,1,suppress=True)), Matrix4x4(1,1,1,1,1,1,suppress=True))


# endregion
