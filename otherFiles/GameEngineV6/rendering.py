"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.07
"""
import math
import unittest
import copy
from  ._tk_inter_inter import *
from .structures import *
from time import clock

class CameraRender:
    buffer=None
    camera_pos=()
    camera_rot=()
    def __init__(self,pos=(0,)*3, rot=(0,)*3):
        self.inter=Interpeter()
        self.camera_pos=pos
        self.camera_rot=rot




    def camera_transform_matrix(self,point_to_transform: tuple):
        # https://en.wikipedia.org/wiki/Rotation_matrix
        # we also need depth to decide what goes above what (z buffer) so we need 4x4 projection matrix
        t=-clock()
        point_v4 = (point_to_transform[0] - self.camera_pos[0],
                    point_to_transform[1] - self.camera_pos[1],
                    point_to_transform[2] - self.camera_pos[2],
                    1)

        # region old readable code (does same as current optimized aka unreadable code)
        # # python thinks Vector times Float is Float XD
        # # Translation order. It Really matters
        # # 1. (t Matrix) Position, so that camera is in 0,0,0
        # # 2. (x Matrix) Camera up down rotation
        # # 3. (y Matrix) Camera rotation around Up axis. Probably the most common rotation.
        # # 4. (z Matrix) Camera tilt. May or may not be ever used XD
        #
        # # 1.
        #
        # # 2. (x Matrix) Camera up down rotation
        # anglex = self.camera_rot[0]*math.radians(1)
        # sinx = math.sin(anglex)
        # cosx = math.cos(anglex)
        # x_rot_m4 = (1,0,0,0,
        #             0,cosx,-sinx,0,
        #             0,sinx,cosx,0,
        #             0,0,0,1)
        #
        # # 3. (y Matrix) Camera rotation around Up axis. Probably the most common rotation.
        # angley = self.camera_rot[1]*math.radians(1)
        # siny = math.sin(angley)
        # cosy = math.cos(angley)
        # y_rot_m4 = (cosy,0,siny,0,
        #             0,1,0,0,
        #             -siny,0,cosy,0,
        #             0,0,0,1)
        #
        # # 4. (z Matrix) Camera tilt. May or may not be ever used XD
        # anglez = self.camera_rot[2]*math.radians(1)
        # sinz = math.sin(anglez)
        # cosz = math.cos(anglez)
        # z_rot_m4 = (cosz,-sinz,0,0,
        #             sinz,cosz,0,0,
        #             0,0,1,0,
        #             0,0,0,1)
        #
        # #
        # #  print("\nrot: ",end="")
        # #  print(camera_rot)
        # # print(point_v4)
        # point_v4 = m4x4_times_v4(x_rot_m4,point_v4)
        # # print(point_v4)
        # point_v4 = m4x4_times_v4(y_rot_m4,point_v4)
        # # print(point_v4)
        # point_v4 = m4x4_times_v4(z_rot_m4,point_v4)
        # # print(point_v4)
        # endregion


        sinx = math.sin(self.camera_rot[0]*math.radians(1))
        cosx = math.cos(self.camera_rot[0]*math.radians(1))
        siny = math.sin(self.camera_rot[1]*math.radians(1))
        cosy = math.cos(self.camera_rot[1]*math.radians(1))
        sinz = math.sin(self.camera_rot[2]*math.radians(1))
        cosz = math.cos(self.camera_rot[2]*math.radians(1))
        rot_m4=(cosx*cosy,
                cosx*siny*sinz-sinx*cosz,
                cosx*siny*cosz+sinx*sinz,0,

                sinx*cosy,
                sinx*siny*sinz+cosx*cosz,
                sinx*siny*cosz-cosx*sinz,0,

                -siny,
                cosy*sinz,
                cosy*cosz,0,

                0,0,0,1)

        point_v4=m4x4_times_v4(rot_m4,point_v4)

        print(t+clock())
        return (point_v4[0] / point_v4[3],
                point_v4[1] / point_v4[3],
                point_v4[2] / point_v4[3])

    def camera_project_matrix(self,point):
        # https://en.wikipedia.org/wiki/Camera_matrix
        # https://en.wikipedia.org/wiki/3D_projection
        # https://en.wikipedia.org/wiki/Camera_matrix

        # https://www.youtube.com/watch?v=8bQ5u14Z9OQ

        point_v4 = (point[0],point[1],point[2],1)

        x_fov = 9/10
        y_fov = 16/10
        x_off = 0
        y_off = 0
        near = 1
        far = 1000
        # I really hope the formulas I found online are correct
        proj = (
             x_fov, 0, x_off, 0,
             0, y_fov, y_off, 0,
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

        point_v4 = m4x4_times_v4(proj,point_v4)
        try:
            return (point_v4[0] / point_v4[3],
                           point_v4[1] / point_v4[3],
                           point_v4[2] / point_v4[3])
        except ZeroDivisionError as e:
            logging.getLogger("render").warning(e)
            logging.getLogger("render").warning(f"{self.camera_rot}  ,  {self.camera_pos}")
            logging.getLogger("render").warning(f"{point}  ,  {point_v4}")
            logging.getLogger("render").warning(f"{proj}")

    def backface_culling(self,triangles: list):
        return list(filter(lambda t: t.normal * self.camera_rot > 0, triangles))


    def basic_frustum_culling(self,triangle: tuple):
        if (0.0 < triangle[0][2]) and \
           (0.0 < triangle[1][2]) and \
           (0.0 < triangle[2][2]):
            return triangle
        else:
            return ()

    def frustum_culling(self,triangle: list):

        # HOW TF DOES PYTHON NOT HAVE SIGN FUNCTION ???????
        sign = lambda f: f/math.fabs(f) if f != 0 else 0

        if ((-1 <= triangle[0][0] <= 1 or -1 <= triangle[0][1] <= 1) and
            (-1 <= triangle[1][0] <= 1 or -1 <= triangle[1][1] <= 1) and
            (-1 <= triangle[2][0] <= 1 or -1 <= triangle[2][1] <= 1)) or \
           (not (sign(triangle[0][0]) == sign(triangle[0][0]) == sign(triangle[0][0])) and
            not (sign(triangle[1][1]) == sign(triangle[1][1]) == sign(triangle[1][1]))):
            return triangle
        else:
            return ()

    def render(self,buffer=None) -> bool:
        # print(self.camera_rot)
        if type(buffer) is not list:
            buffer = self.buffer
        else:
            self.buffer = buffer

        step_buffer_first = []
        for t in buffer:
            step_buffer_first.append(self.camera_transform_matrix(t))

        step_buffer_second = []
        for i in range(0,len(step_buffer_first),3):
            step_buffer_second.extend(self.basic_frustum_culling(
                (step_buffer_first[i],step_buffer_first[i+1],step_buffer_first[i+2])))

        step_buffer_first = []
        for t in step_buffer_second:
            step_buffer_first.append(self.camera_project_matrix(t))

        if self.inter.draw(step_buffer_first):
            return True
        else:
            return False


class proj_unit_test(unittest.TestCase):
    def test(self):

        rend = CameraRender()

        # tris = ()
        # tris.append([0.1, 0, 1, 0.1, 0, 10, 0.0, 0, 0])
        # tris.append([2, 1, 1, -1, 0, 10, 0.0, 2, 0])
        # tris.append([-3, 1, 1, -1, -2, 10, -2, -1, 0])
        # new_tris = rend.frustum_culling(tris)

        # self.assertEqual(len(new_tris),3)


        rend.camera_rot = (0, 0, 0)
        rend.camera_pos = (0, 0, 0)
        point = (0, 0, 1)
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, tuple([0, 0, 1]))

        rend.camera_rot = [0, 90, 0]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, tuple([-1, 0, 6.123233995736766e-17]))

        rend.camera_rot = [0, 90 * 3177, 0]
        new_point = rend.camera_transform_matrix( point)
        self.assertEqual(new_point, tuple([-1, 0, 1.2880994098674778e-13]))

        rend.camera_rot = [0, 180, 0]
        point = [0, 1, 1]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, tuple([-1.2246467991473532e-16, 1, -1]))

        rend.camera_rot = [0, 90, 0]
        point = [0, 0, 1]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, tuple([-1, 0, 6.123233995736766e-17]))

        rend.camera_rot = [90, 270, -90]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, tuple([-1, 1.2246467991473532e-16, -1.1248198369963932e-32]))

        rend.camera_rot = [90,270,90]
        new_point = rend.camera_transform_matrix(point)
        self.assertEqual(new_point, tuple([1, 0, -1.1248198369963932e-32]))

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
