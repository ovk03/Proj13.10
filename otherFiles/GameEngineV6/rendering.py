"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.07
"""
import math
import unittest
import copy
from  ._tk_inter_inter import *
from .structures import *

class CameraRender:
    buffer=None
    camera_pos=[]
    camera_rot=[]
    def __init__(self,pos=[0]*3, rot=[0]*3):
        self.inter=Interpeter()
        self.camera_pos=pos
        self.camera_rot=rot




    def camera_transform_matrix(self,point_to_transform: list):
        # https://en.wikipedia.org/wiki/Rotation_matrix
        # we also need depth to decide what goes above what (z buffer) so we need 4x4 projection matrix

        # python thinks Vector times Float is Float XD
        camera_rot = [r*math.radians(1) for r in self.camera_rot]
        # Translation order. It Really matters
        # 1. (t Matrix) Position, so that camera is in 0,0,0
        # 2. (x Matrix) Camera up down rotation
        # 3. (y Matrix) Camera rotation around Up axis. Probably the most common rotation.
        # 4. (z Matrix) Camera tilt. May or may not be ever used XD

        # 1.
        point_v4 = [point_to_transform[0] - self.camera_pos[0],
                           point_to_transform[1] - self.camera_pos[1],
                           point_to_transform[2] - self.camera_pos[2],
                           1]

        # 2. (x Matrix) Camera up down rotation
        anglex = camera_rot[0]
        sinx = math.sin(anglex)
        cosx = math.cos(anglex)
        x_rot_m4 = EYE_MATRIX.copy()
        x_rot_m4[1+4*1] = x_rot_m4[2+4*2] = cosx
        x_rot_m4[2+4*1] = -sinx
        x_rot_m4[1+4*2] = sinx

        # 3. (y Matrix) Camera rotation around Up axis. Probably the most common rotation.
        angley = camera_rot[1]
        siny = math.sin(angley)
        cosy = math.cos(angley)
        y_rot_m4 = EYE_MATRIX.copy()
        y_rot_m4[0] = y_rot_m4[2+4*2] = cosy
        y_rot_m4[2] = -siny
        y_rot_m4[4*2] = -siny

        # 4. (z Matrix) Camera tilt. May or may not be ever used XD
        anglez = camera_rot[2]
        sinz = math.sin(anglez)
        cosz = math.cos(anglez)
        z_rot_m4 = EYE_MATRIX.copy()
        z_rot_m4[0] = z_rot_m4[1+4*1] = cosz
        z_rot_m4[1] = -sinz
        z_rot_m4[4*1] = sinz

        #
        #  print("\nrot: ",end="")
        #  print(camera_rot)
        # print(point_v4)
        point_v4 = m4x4_times_v4(x_rot_m4,point_v4)
        # print(point_v4)
        point_v4 = m4x4_times_v4(y_rot_m4,point_v4)
        # print(point_v4)
        point_v4 = m4x4_times_v4(z_rot_m4,point_v4)
        # print(point_v4)

        return [point_v4[0] / point_v4[3],
                point_v4[1] / point_v4[3],
                point_v4[2] / point_v4[3]]


    def camera_project_matrix(self,point):
        # https://en.wikipedia.org/wiki/Camera_matrix
        # https://en.wikipedia.org/wiki/3D_projection
        # https://en.wikipedia.org/wiki/Camera_matrix

        # https://www.youtube.com/watch?v=8bQ5u14Z9OQ

        point_v4 = point
        point_v4.append(1)

        x_fov = 9/10
        y_fov = 16/10
        x_off = 0
        y_off = 0
        near = .1
        far = 1000
        # I really hope the formulas I found online are correct
        proj = [
             x_fov, 0, x_off, 0,
             0, y_fov, y_off, 0,
             0, 0, far / (far - near), 1,
             0, 0, -near * far / (far - near), 0]

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

        point_v4 = m4x4_times_v4(proj,point_v4)
        try:
            return [point_v4[0] / point_v4[3],
                           point_v4[1] / point_v4[3],
                           point_v4[2] / point_v4[3]]
        except ZeroDivisionError as e:
            logging.getLogger("render").warning(e)
            logging.getLogger("render").warning(f"{self.camera_rot}  ,  {self.camera_pos}")
            logging.getLogger("render").warning(f"{point}  ,  {point_v4}")
            logging.getLogger("render").warning(f"{proj}")

    def backface_culling(self,triangles: list):
        return list(filter(lambda t: t.normal * self.camera_rot > 0, triangles))


    def basic_frustum_culling(self,triangles: list):
        filter_func = lambda triangle: (0.01 >= triangle.vert1[2]) and \
                                       (0.01 >= triangle.vert2[2]) and \
                                       (0.01 >= triangle.vert3[2])
        triangles=list(filter(filter_func, triangles))

        for t in triangles:
            t.depth = (t.vert1.z + t.vert2.z + t.vert3.z) / 3

        return triangles


    def frustum_culling(self,triangles: list):

        # HOW TF DOES PYTHON NOT HAVE SIGN FUNCTION ???????
        sign = lambda f: f/math.fabs(f) if f != 0 else 0

        filter_func = lambda triangle: ((-1 <= triangle.vert1[0]  <= 1 or -1 <= triangle.vert1[1] <= 1) and
                                        (-1 <= triangle.vert2[0]  <= 1 or -1 <= triangle.vert2[1] <= 1) and
                                        (-1 <= triangle.vert3[0]  <= 1 or -1 <= triangle.vert3[1] <= 1)) or \
                                       (not (sign(triangle.vert1[0]) == sign(triangle.vert2[0]) == sign(triangle.vert3[0])) and
                                        not (sign(triangle.vert1[1]) == sign(triangle.vert2[1]) == sign(triangle.vert3[1])))

        triangles=list(filter(filter_func, triangles))

        return triangles


    def render(self,buffer=None) -> bool:
        print(self.camera_rot)
        if type(buffer) is not list:
            buffer = self.buffer
        else:
            self.buffer = buffer
        new_buffer=[]
        for t in buffer:
            new_buffer.append(self.camera_transform_matrix(t))

        # buffer.triangles=self.basic_frustum_culling(buffer.triangles)

        final_buffer=[]
        for t in new_buffer:
            final_buffer.append(self.camera_project_matrix(t))

        if self.inter.draw(final_buffer):
            return True
        else:
            return False


class proj_unit_test(unittest.TestCase):
    def test(self):

        rend = CameraRender()

        # tris = []
        # tris.append([0.1, 0, 1, 0.1, 0, 10, 0.0, 0, 0])
        # tris.append([2, 1, 1, -1, 0, 10, 0.0, 2, 0])
        # tris.append([-3, 1, 1, -1, -2, 10, -2, -1, 0])
        # new_tris = rend.frustum_culling(tris)

        # self.assertEqual(len(new_tris),3)


        rend.camera_rot = [0, 0, 0]
        rend.camera_pos = [0, 0, 0]
        point = [0, 0, 1]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, [0, 0, 1])

        rend.camera_rot = [0, 90, 0]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, [-1, 0, 6.123233995736766e-17])

        rend.camera_rot = [0, 90 * 3177, 0]
        new_point = rend.camera_transform_matrix( point)
        self.assertEqual(new_point, [-1, 0, 1.2880994098674778e-13])

        rend.camera_rot = [0, 180, 0]
        point = [0, 1, 1]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, [-1.2246467991473532e-16, 1, -1])

        rend.camera_rot = [0, 90, 0]
        point = [0, 0, 1]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, [-1, 0, 6.123233995736766e-17])

        rend.camera_rot = [90, 270, -90]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, [-1, 1.2246467991473532e-16, -1.1248198369963932e-32])

        rend.camera_rot = [90,270,90]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, [1, 0, -1.1248198369963932e-32])

        rend.camera_rot = [0, 0, 0]
        rend.camera_pos = [0, 0, -1]
        points = [[0, 0, -0.8], [4, 0, 10],
                  [0, 0, 0], [-.1, -.1, -0.2]]
        new_points = [rend.camera_project_matrix(rend.camera_transform_matrix(p)) for p in points]
        for new_point in new_points:
            self.assertNotEqual(point, new_point)
            self.assertTrue(-1 <= new_point[0] <= 1)
            self.assertTrue(-1 <= new_point[1] <= 1)
            self.assertTrue(-1 <= new_point[2] <= 1)
        a=[0,0,0]
        print(rend.camera_project_matrix(rend.camera_transform_matrix(a)))
        a=rend.camera_project_matrix(rend.camera_transform_matrix(a))
        print(a)

        rend.camera_rot = [0, 0, 0]
        rend.camera_pos = [0, 0, -1]
        point1 = [5, 2, 0]
        point2 = [5, 2, 100]
        new_point1 = rend.camera_project_matrix(rend.camera_transform_matrix( point1))
        new_point2 = rend.camera_project_matrix(rend.camera_transform_matrix( point2))
        self.assertTrue(new_point2[0] < new_point1[0] and new_point2[1] < new_point1[1] )
