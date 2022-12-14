"""Extremely hard to read module for 3d camera projection and culling
I had to optimize this to the maximum in order to achieve realtime rendering
Due to that the code might be unreadable """

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.07
"""
import functools
import math
import unittest
import copy
import platform
print(platform.processor())
from  ._tk_inter_inter import *
from .structures import *
import time

class CameraRender:
    camera_pos=()
    camera_rot=()
    sinx = 0.0
    cosx = 0.0
    siny = 0.0
    cosy = 0.0
    sinz = 0.0
    cosz = 0.0

    def __init__(self,pos=(0,)*3, rot=(0,)*3):
        self.inter=Interpeter()
        self.camera_pos = pos
        self.camera_rot = rot

    #region deprecated

    # deprecated
    @ functools.lru_cache
    def camera_transform_matrix(self, point:tuple):
        """deprecated, transforms points so that camera is in the origin facing forward
        use \"optimized_proj_and_culling\" instead for better performance"""
        # https://en.wikipedia.org/wiki/Rotation_matrix
        # we also need depth to decide what goes above what (z buffer) so we need 4x4 projection matrix


        # region old readable code (does same as current optimized aka unreadable code)
        # # Translation order. It Really matters
        # # 1. (t Matrix) Position, so that camera is in 0,0,0
        # # 2. (x Matrix) Camera up down rotation
        # # 3. (y Matrix) Camera rotation around Up axis. Probably the most common rotation.
        # # 4. (z Matrix) Camera tilt. May or may not be ever used XD
        #
        # # 1.
        # point_v4 = (point_to_transform[0] - self.camera_pos[0],
        #             point_to_transform[1] - self.camera_pos[1],
        #             point_to_transform[2] - self.camera_pos[2],
        #             1)
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
        #
        # return (point_v4[0] / point_v4[3],
        #         point_v4[1] / point_v4[3],
        #         point_v4[2] / point_v4[3])
        # endregion


        # This way there is no unnesecary variable assignastions.
        # I Really wish we didn't need this but as it stands, this is necessary for this code to run
        # I never have had to do this with any other programming language and
        # I wish I'm doing something wrong as this is terrible code compared to any other code in any other language
        point_v4 = m4x4_times_v4(
                # matrix
               (self.cosx*self.cosy,self.cosx*self.siny*self.sinz-self.sinx*self.cosz,
                        self.cosx*self.siny*self.cosz+self.sinx*self.sinz,0,
                self.sinx*self.cosy, self.sinx*self.siny*self.sinz+self.cosx*self.cosz,
                        self.sinx*self.siny*self.cosz-self.cosx*self.sinz,0,
                -self.siny,self.cosy*self.sinz,self.cosy*self.cosz,0,
                0,0,0,1),

                # point
                (point[0] - self.camera_pos[0],
                 point[1] - self.camera_pos[1],
                 point[2] - self.camera_pos[2], 1))

        return (point_v4[0] / point_v4[3],
                point_v4[1] / point_v4[3],
                point_v4[2] / point_v4[3])

    # deprecated
    @ functools.lru_cache()
    def camera_project_matrix(self,point):
        """deprecated, transforms points according to camera projection
        use \"optimized_proj_and_culling\" instead for better performance"""
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
        return (point_v4[0] / point_v4[3],
                       point_v4[1] / point_v4[3],
                       point_v4[2] / point_v4[3])

    def backface_culling(self,triangle: list):
        """deprecated due to performance"""
        pass
        # if(tri_normal((*triangle[0],*triangle[1],*triangle[2])))[3]

    def basic_frustum_culling(self,triangle: tuple):
        """deprecated due to performance"""
        # removes points behind camera
        # TODO: clamp them in a way that makes sense perspective wise
        if (0.0 < triangle[0][2]) and \
           (0.0 < triangle[1][2]) and \
           (0.0 < triangle[2][2]):
            return triangle
        else:
            return ()

    def frustum_culling(self,triangle: list):
        """deprecated due to performance"""

        # HOW TF DOES PYTHON NOT HAVE SIGN FUNCTION ???????
        sign = lambda f: f/math.fabs(f) if f != 0 else 0

        # checks that all X and Y values are between -1 - 1
        # if not checks If they go across the screen, else discards that triangle
        if ((-1 <= triangle[0][0] <= 1 or -1 <= triangle[0][1] <= 1) and
            (-1 <= triangle[1][0] <= 1 or -1 <= triangle[1][1] <= 1) and
            (-1 <= triangle[2][0] <= 1 or -1 <= triangle[2][1] <= 1)) or (
            # check if vertices span the whole screen
            not (sign(triangle[0][0]) == sign(triangle[0][0]) == sign(triangle[0][0])) and
            not (sign(triangle[1][1]) == sign(triangle[1][1]) == sign(triangle[1][1]))):
            return triangle
        else:
            return ()

    @functools.lru_cache
    def optimized_proj_and_culling(self, triangles: tuple, matrix1: tuple, matrix2: tuple):
        """deprecated due to performance"""

        new_buff=[]
        for triangle in range(0,len(triangles),3):
            point1_v4 = m4x4_times_v4(matrix1,
                                      (triangle[0] - self.camera_pos[0],
                                       triangle[1] - self.camera_pos[1],
                                       triangle[2] - self.camera_pos[2], 1))
            point2_v4 = m4x4_times_v4(matrix1,
                                      (triangle[3] - self.camera_pos[0],
                                       triangle[4] - self.camera_pos[1],
                                       triangle[5] - self.camera_pos[2], 1))
            point3_v4 = m4x4_times_v4(matrix1,
                                      (triangle[6] - self.camera_pos[0],
                                       triangle[7] - self.camera_pos[1],
                                       triangle[8] - self.camera_pos[2], 1))

            point1_v4 = m4x4_times_v4(matrix2, point1_v4)
            point2_v4 = m4x4_times_v4(matrix2, point2_v4)
            point3_v4 = m4x4_times_v4(matrix2, point3_v4)
            new_buff.extend([point1_v4[0] / point1_v4[3],
                             point1_v4[1] / point1_v4[3],
                             point1_v4[2] / point1_v4[3],
                             point2_v4[0] / point2_v4[3],
                             point2_v4[1] / point2_v4[3],
                             point2_v4[2] / point2_v4[3],
                             point3_v4[0] / point3_v4[3],
                             point3_v4[1] / point3_v4[3],
                             point3_v4[2] / point3_v4[3]])
        return new_buff

    def project_and_cull(self,buffer:list):
        """deprecated due to performance"""
        self.sinx = math.sin(self.camera_rot[0] * math.radians(1))
        self.cosx = math.cos(self.camera_rot[0] * math.radians(1))
        self.siny = math.sin(self.camera_rot[1] * math.radians(1))
        self.cosy = math.cos(self.camera_rot[1] * math.radians(1))
        self.sinz = math.sin(self.camera_rot[2] * math.radians(1))
        self.cosz = math.cos(self.camera_rot[2] * math.radians(1))

        step_buffer_first = []
        for t in buffer:
            step_buffer_first.append(self.camera_transform_matrix(t))

        step_buffer_second = []
        for i in range(0, len(step_buffer_first), 3):
            step_buffer_second.extend(self.basic_frustum_culling(
                (step_buffer_first[i], step_buffer_first[i + 1], step_buffer_first[i + 2])))

        step_buffer_first.clear()
        for t in step_buffer_second:
            step_buffer_first.append(self.camera_project_matrix(t))



        return self.optimized_proj_and_culling()

    # endregion

    def render(self,buffer=None,cache:bool=False) -> bool:
        # print(self.camera_rot)
        if type(buffer) is not list:
            buffer = self.buffer
        elif cache: self.buffer = buffer

        self.sinx = math.sin(self.camera_rot[0] * math.radians(1))
        self.cosx = math.cos(self.camera_rot[0] * math.radians(1))
        self.siny = math.sin(self.camera_rot[1] * math.radians(1))
        self.cosy = math.cos(self.camera_rot[1] * math.radians(1))
        self.sinz = math.sin(self.camera_rot[2] * math.radians(1))
        self.cosz = math.cos(self.camera_rot[2] * math.radians(1))

        x_fov = 9/10
        y_fov = 16/10
        x_off = 0
        y_off = 0
        near = 1
        far = 1000

        screen_width,screen_height=self.inter.get_width_and_height()


        trans_m4=(self.cosx * self.cosy, self.cosx * self.siny * self.sinz - self.sinx * self.cosz,
                        self.cosx * self.siny * self.cosz + self.sinx * self.sinz, 0,
                  self.sinx * self.cosy, self.sinx * self.siny * self.sinz + self.cosx * self.cosz,
                        self.sinx * self.siny * self.cosz - self.cosx * self.sinz, 0,
                  -self.siny, self.cosy * self.sinz, self.cosy * self.cosz, 0,
                  0, 0, 0, 1)
        proj_m4 = (
             x_fov, 0, x_off, 0,
             0, y_fov, y_off, 0,
             0, 0, far / (far - near), 1,
             0, 0, -near * far / (far - near), 0)

        new_buff=[]
        for point in buffer:
            point1_v4 = m4x4_times_v4(trans_m4,
                                      (point[0][0] - self.camera_pos[0],
                                       point[0][1] - self.camera_pos[1],
                                       point[0][2] - self.camera_pos[2], 1))
            point2_v4 = m4x4_times_v4(trans_m4,
                                      (point[1][0] - self.camera_pos[0],
                                       point[1][1] - self.camera_pos[1],
                                       point[1][2] - self.camera_pos[2], 1))
            point3_v4 = m4x4_times_v4(trans_m4,
                                      (point[2][0] - self.camera_pos[0],
                                       point[2][1] - self.camera_pos[1],
                                       point[2][2] - self.camera_pos[2], 1))

            point1_v4 = m4x4_times_v4(proj_m4, point1_v4)
            point2_v4 = m4x4_times_v4(proj_m4, point2_v4)
            point3_v4 = m4x4_times_v4(proj_m4, point3_v4)

            new_buff.append(((point1_v4[0] / (point1_v4[3]+1e-32),
                             point1_v4[1] / (point1_v4[3]+1e-32),
                             point1_v4[2] / (point1_v4[3]+1e-32)),
                            (point2_v4[0] / (point2_v4[3]+1e-32),
                             point2_v4[1] / (point2_v4[3]+1e-32),
                             point2_v4[2] / (point2_v4[3]+1e-32)),
                            (point3_v4[0] / (point3_v4[3]+1e-32),
                             point3_v4[1] / (point3_v4[3]+1e-32),
                             point3_v4[2] / (point3_v4[3]+1e-32))))


        if self.inter.draw(new_buff):
            return True
        else:
            return False

# region uTests
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
# endregion