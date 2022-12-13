"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.07
"""
import sys
from tkinter import *
from dataclasses import dataclass
import math
import unittest

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))
from GameEngineV5.mathAndStructs import *
from GameEngineV5 import *
from GameEngineV5.internals.tk_inter_inter import *
if __name__ == "some random stuff to trick pep8 thinking that i have mathAndStructs module imported (I do)":
    from ..mathAndStructs import *
    from .tk_inter_inter import Interpeter



class CameraRender:
    tris=[]
    camera_pos=Vector3()
    camera_rot=Vector3()
    def __init__(self,pos=Vector3(), rot=Vector3()):
        self.inter=Interpeter()
        self.camera_pos=pos
        self.camera_rot=rot




    def camera_transform_matrix(self,point_to_transform: Vector3):
        # https://en.wikipedia.org/wiki/Rotation_matrix
        # we also need depth to decide what goes above what (z buffer) so we need 4x4 projection matrix

        # python thinks Vector times Float is Float XD
        camera_rot = self.camera_rot*math.radians(1)
        # Translation order. It Really matters
        # 1. (t Matrix) Position, so that camera is in 0,0,0
        # 2. (x Matrix) Camera up down rotation
        # 3. (y Matrix) Camera rotation around Up axis. Probably the most common rotation.
        # 4. (z Matrix) Camera tilt. May or may not be ever used XD

        # 1.
        point_v4 = Vector4(point_to_transform.x - self.camera_pos.x,
                           point_to_transform.y - self.camera_pos.y,
                           point_to_transform.z - self.camera_pos.z,
                           1)

        # 2. (x Matrix) Camera up down rotation
        angle = camera_rot.x
        sin = math.sin(angle)
        cos = math.cos(angle)
        x_rot_m4 = Matrix4x4(eye=True)
        x_rot_m4.m11 = x_rot_m4.m22 = cos
        x_rot_m4.m21 = -sin
        x_rot_m4.m12 = sin

        # 3. (y Matrix) Camera rotation around Up axis. Probably the most common rotation.
        angle = camera_rot.y
        sin = math.sin(angle)
        cos = math.cos(angle)
        y_rot_m4 = Matrix4x4(eye=True)
        y_rot_m4.m00 = y_rot_m4.m22 = cos
        y_rot_m4.m20 = sin
        y_rot_m4.m02 = -sin

        # 4. (z Matrix) Camera tilt. May or may not be ever used XD
        angle = camera_rot.z
        sin = math.sin(angle)
        cos = math.cos(angle)
        z_rot_m4 = Matrix4x4(eye=True)
        z_rot_m4.m00 = z_rot_m4.m11 = cos
        z_rot_m4.m10 = -sin
        z_rot_m4.m01 = sin

        #
        #  print("\nrot: ",end="")
        #  print(camera_rot)
        # print(point_v4)
        point_v4 = z_rot_m4 * point_v4
        # print(point_v4)
        point_v4 = y_rot_m4 * point_v4
        # print(point_v4)
        point_v4 = x_rot_m4 * point_v4
        # print(point_v4)

        return Vector3(point_v4.x / point_v4.w,
                       point_v4.y / point_v4.w,
                       point_v4.z / point_v4.w)


    def camera_project_matrix(self,point):
        # https://en.wikipedia.org/wiki/Camera_matrix
        # https://en.wikipedia.org/wiki/3D_projection
        # https://en.wikipedia.org/wiki/Camera_matrix

        # https://www.youtube.com/watch?v=8bQ5u14Z9OQ

        point_v4 = point.vec4()

        x_fov = 1
        y_fov = 1
        x_off = 0
        y_off = 0
        near = .1
        far = 10
        # I really hope the formulas I found online are correct
        proj = Matrix4x4 \
            (near / x_fov, 0, x_off, 0,
             0, near / y_fov, y_off, 0,
             0, 0, far / (far - near), 1,
             0, 0, -near * far / (far - near), 0)

        # proj = Matrix4x4 \
        #     (near / x_fov, 0, x_off, 0,
        #      0, near / y_fov, y_off, 0,
        #      0, 0, far / (far - near), 1,
        #      0, 0, -near * far / (far - near), 0)


        # proj = Matrix4x4\
        #     (near/x_fov,0,          x_off,  0,
        #     0,          near/y_fov, y_off,  0,
        #     0,          0,          1,     -0.1,
        #     0,          0,          1,      0)

        point_v4 = proj * point_v4
        try:
            return Vector3(point_v4.x / point_v4.w,
                           point_v4.y / point_v4.w,
                           point_v4.z / point_v4.w)
        except ZeroDivisionError as e:
            logging.getLogger("render").warning(e)
            logging.getLogger("render").warning(f"{self.camera_rot}  ,  {self.camera_pos}")
            logging.getLogger("render").warning(f"{point}  ,  {point_v4.vec3()}")


    def backface_culling(self, triangles: list):
        return list(filter(lambda t: t.normal * self.rot > 0, triangles))

    def basic_frustum_culling(self,triangles: list):
        filter_func = lambda triangle: (0.01 > triangle.vert1.z) and \
                                       (0.01 > triangle.vert2.z) and \
                                       (0.01 > triangle.vert3.z)
        triangles=list(filter(filter_func, triangles))
        for t in triangles:
            t.depth = (t.vert1.z + t.vert2.z + t.vert3.z) / 3
        return triangles

    def frustum_culling(self,triangles: list):

        # HOW TF DOES PYTHON NOT HAVE SIGN FUNCTION ???????
        sign = lambda f: f/math.fabs(f) if f != 0 else 0

        filter_func = lambda triangle: ((-1 < triangle.vert1.x < 1 or -1 < triangle.vert1.y < 1) and
                                        (-1 < triangle.vert2.x < 1 or -1 < triangle.vert2.y < 1) and
                                        (-1 < triangle.vert3.x < 1 or -1 < triangle.vert3.y < 1)) or \
                                       (not (sign(triangle.vert1.x) == sign(triangle.vert2.x) == sign(triangle.vert3.x)) and
                                        not (sign(triangle.vert1.y) == sign(triangle.vert2.y) == sign(triangle.vert3.x)))

        triangles=list(filter(filter_func, triangles))

        tri = Triangle(Vector3(0.1, 0, 1),
                         Vector3(0.1, 0, 10),
                         Vector3(0.0, 0, 0),Vector3())
        for t in triangles:
            t.depth = (t.vert1.z + t.vert2.z + t.vert3.z) / 3
        return triangles


    def render(self,buffer) -> bool:
        buffer=buffer.project(self, self.camera_transform_matrix)
        buffer=buffer.project(self, self.camera_project_matrix)

        for i in buffer.triangles:
            if type(i) != Triangle:
                raise TypeError

        if self.inter.draw(buffer):
            return True
        else:
            return False


class proj_unit_test(unittest.TestCase):
    def test(self):

        rend = CameraRender()

        tris = []
        tris.append(Triangle(Vector3(0.1, 0, 1), Vector3(0.1, 0, 10), Vector3(0.0, 0, 0), Vector3()))
        tris.append(Triangle(Vector3(2, 1, 1), Vector3(-1, 0, 10), Vector3(0.0, 2, 0), Vector3()))
        tris.append(Triangle(Vector3(-3, 1, 1), Vector3(-1, -2, 10), Vector3(-2, -1, 0), Vector3()))
        new_tris = rend.frustum_culling(tris)

        self.assertEqual(len(new_tris),2)


        rend.camera_rot = Vector3(0, 0, 0)
        rend.camera_pos = Vector3(0, 0, 0)
        point = Vector3(0, 0, 1)
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, Vector3(0, 0, 1))

        rend.camera_rot = Vector3(0, 90, 0)
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, Vector3(-1, 0, 0))

        rend.camera_rot = Vector3(0, 90 * 3177, 0)
        new_point = rend.camera_transform_matrix( point)
        self.assertEqual(new_point, Vector3(-1, 0, 0))

        rend.camera_rot = Vector3(0, 180, 0)
        point = Vector3(0, 1, 1)
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, Vector3(0, 1, -1))

        rend.camera_rot = Vector3(0, 90, 0)
        point = Vector3(0, 0, 1)
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, Vector3(-1, 0, 0))

        rend.camera_rot = Vector3(90, 90, 423423)
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, Vector3(-1, 0, 0))

        rend.camera_rot = Vector3(312378,270,0)
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, Vector3(1, 0, 0))

        rend.camera_rot = Vector3(0, 0, 0)
        rend.camera_pos = Vector3(0, 0, -1)
        points = [Vector3(5, 0, 1), Vector3(50, 0, 10),
                  Vector3(0, 0, 0), Vector3(-1, -.1, -0.8)]
        new_points = [rend.camera_project_matrix(rend.camera_transform_matrix( p)) for p in points]
        for new_point in new_points:
            self.assertNotEqual(point, new_point)
            self.assertTrue(-1 < new_point.x < 1)
            self.assertTrue(-1 < new_point.y < 1)
            self.assertTrue(-1 < new_point.z < 1)

        rend.camera_rot = Vector3(0, 0, 0)
        rend.camera_pos = Vector3(0, 0, -1)
        point1 = Vector3(5, 2, 0)
        point2 = Vector3(5, 2, 100)
        new_point1 = rend.camera_project_matrix(rend.camera_transform_matrix( point1))
        new_point2 = rend.camera_project_matrix(rend.camera_transform_matrix( point2))
        self.assertTrue(new_point2.x < new_point1.x and new_point2.y < new_point1.y)
