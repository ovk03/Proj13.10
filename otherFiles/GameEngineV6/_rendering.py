"""Optimized to the maximum. Does pretty much the same as render.py"""
"""Onni Kolkka 
150832953 (student number)
created 15.12.2022 21.18
"""


import threading
from ._tk_inter_inter import *
from .structures import *
from .__main__ import EngineTypeSingleton
import time


class CameraRenderOptimized(metaclass=EngineTypeSingleton):
    
    buffer=None

    camera_pos = ()
    camera_rot = ()
    sinx = 0.0
    cosx = 0.0
    siny = 0.0
    cosy = 0.0
    sinz = 0.0
    cosz = 0.0


    def __init__(self, pos=(0,)*3, rot=(0,)*3):
        self.camera_pos = pos
        self.camera_rot = rot

    def render(self, buffer=None, *_):
        was_rendered=False
        tcl_code=[]
        return self.render3d(buffer,True)

    def render3d(self, buffer=None, cache: bool = False) -> bool:
        """really complicated and unreadable code, but REALLY OPTIMIZED for rendering objects with tkinter
        Input is tuple of form:
        ((1,1,1),(1,1,1),(1,2,3))
    
        This is composed of three different parts.
        # 1. checks
        # 2. constants
        # 3. calculations
        """


        # 1. checks
        if type(buffer) is not list:
            buffer = self.buffer
        elif cache:
            self.buffer = buffer


        # 2. constants

    
        x_fov = 9 / 10
        y_fov = 16 / 10
        near = 0.01
        far = 100
        fov_near_x=-x_fov
        fov_near_y=-y_fov
        far_near_far=far/(far-near)

        c_pos_x,c_pos_y,c_pos_z = self.camera_pos
        
        screen_width, screen_height, canvas = GameToTK().get_data_for_rend()

        sa = math.sin(self.camera_rot[0] * math.radians(1))
        ca = math.cos(self.camera_rot[0] * math.radians(1))
        sb = math.sin(self.camera_rot[1] * math.radians(1))
        cb = math.cos(self.camera_rot[1] * math.radians(1))
        sy = math.sin(self.camera_rot[2] * math.radians(1))
        cy = math.cos(self.camera_rot[2] * math.radians(1))

        # https://en.wikipedia.org/wiki/Rotation_matrix
        # I had to change multiply order to z last
        trans_m3x3 = (
            cy*cb - sy*sa*sb,   cy*sa*sb + sy*cb,   ca*sb,
            -sy * ca        ,   cy*ca           ,   -sa,
            -cy*sb - sy*sa*cb,  cy*sa*cb - sy*sb,   ca * cb)

        proj_m4 = (
            x_fov, 0, 0, 0,
            0, y_fov, 0, 0,
            0, 0, far / (far - near), -near * far / (far - near),
            0, 0, 1, 0)

        tcl_code = []


        # 3. calculations
        for tri in buffer:
            point1_v4 = (
                trans_m3x3[0] * (tri[3]-c_pos_x)+
                trans_m3x3[3] * (tri[4]-c_pos_y)+
                trans_m3x3[6] * (tri[5]-c_pos_z),
                trans_m3x3[1] * (tri[3]-c_pos_x)+
                trans_m3x3[4] * (tri[4]-c_pos_y)+
                trans_m3x3[7] * (tri[5]-c_pos_z),
                trans_m3x3[2] * (tri[3]-c_pos_x)+
                trans_m3x3[5] * (tri[4]-c_pos_y)+
                trans_m3x3[8] * (tri[5]-c_pos_z))
            point2_v4 = (
                trans_m3x3[0] * (tri[6]-c_pos_x)+
                trans_m3x3[3] * (tri[7]-c_pos_y)+
                trans_m3x3[6] * (tri[8]-c_pos_z),
                trans_m3x3[1] * (tri[6]-c_pos_x)+
                trans_m3x3[4] * (tri[7]-c_pos_y)+
                trans_m3x3[7] * (tri[8]-c_pos_z),
                trans_m3x3[2] * (tri[6]-c_pos_x)+
                trans_m3x3[5] * (tri[7]-c_pos_y)+
                trans_m3x3[8] * (tri[8]-c_pos_z))
            point3_v4 = (
                trans_m3x3[0] * (tri[9]-c_pos_x)+
                trans_m3x3[3] * (tri[10]-c_pos_y)+
                trans_m3x3[6] * (tri[11]-c_pos_z),
                trans_m3x3[1] * (tri[9]-c_pos_x)+
                trans_m3x3[4] * (tri[10]-c_pos_y)+
                trans_m3x3[7] * (tri[11]-c_pos_z),
                trans_m3x3[2] * (tri[9]-c_pos_x)+
                trans_m3x3[5] * (tri[10]-c_pos_y)+
                trans_m3x3[8] * (tri[11]-c_pos_z))
            point4_v4 = (
                trans_m3x3[0] * (tri[12]-c_pos_x)+
                trans_m3x3[3] * (tri[13]-c_pos_y)+
                trans_m3x3[6] * (tri[14]-c_pos_z),
                trans_m3x3[1] * (tri[12]-c_pos_x)+
                trans_m3x3[4] * (tri[13]-c_pos_y)+
                trans_m3x3[7] * (tri[14]-c_pos_z),
                trans_m3x3[2] * (tri[12]-c_pos_x)+
                trans_m3x3[5] * (tri[13]-c_pos_y)+
                trans_m3x3[8] * (tri[14]-c_pos_z))

            z = ((point1_v4[0]*point1_v4[0]+point1_v4[2]*point1_v4[2]+point1_v4[1]*point1_v4[1])+
                 (point2_v4[0]*point2_v4[0]+point2_v4[2]*point2_v4[2]+point2_v4[1]*point2_v4[1])+
                 (point3_v4[0]*point3_v4[0]+point3_v4[2]*point3_v4[2]+point3_v4[1]*point3_v4[1])+
                 (point4_v4[0]*point4_v4[0]+point4_v4[2]*point4_v4[2]+point4_v4[1]*point4_v4[1]))


            # projection transform
            point1_v4 = (
                fov_near_x * point1_v4[0],
                fov_near_y * point1_v4[1],
                point1_v4[2]-near,
                point1_v4[2]+far_near_far)
            point2_v4 = (
                fov_near_x * point2_v4[0],
                fov_near_y * point2_v4[1],
                point2_v4[2]-near,
                point2_v4[2]+far_near_far)
            point3_v4 = (
                fov_near_x * point3_v4[0],
                fov_near_y * point3_v4[1],
                point3_v4[2]-near,
                point3_v4[2]+far_near_far)
            point4_v4 = (
                fov_near_x * point4_v4[0],
                fov_near_y * point4_v4[1],
                point4_v4[2]-near,
                point4_v4[2]+far_near_far)

            if (point1_v4[0] > point1_v4[3]) and \
                    (point2_v4[0] > point2_v4[3]) and \
                    (point3_v4[0] > point3_v4[3]) and \
                    (point4_v4[0] > point4_v4[3]):
                continue
            if (point1_v4[0] < -point1_v4[3]) and \
                    (point2_v4[0] < -point2_v4[3]) and \
                    (point3_v4[0] < -point3_v4[3]) and \
                    (point4_v4[0] < -point4_v4[3]):
                continue
            if (point1_v4[1] > point1_v4[3]) and \
                    (point2_v4[1] > point2_v4[3]) and \
                    (point3_v4[1] > point3_v4[3]) and \
                    (point4_v4[1] > point4_v4[3]):
                continue
            if (point1_v4[1] < -point1_v4[3]) and \
                    (point2_v4[1] < -point2_v4[3]) and \
                    (point3_v4[1] < -point3_v4[3]) and \
                    (point4_v4[1] < -point4_v4[3]):
                continue


            if (0.0 > point1_v4[2]) and \
                    (0.0 > point2_v4[2]) and \
                    (0.0 > point3_v4[2]) and \
                    (0.0 > point4_v4[2]):
                continue

            # TODO: cull Z  in a way that makes sense perspective wise


            # conversion to screen points
            # this used to be 3 different functions, but by merging them like this I saved alot of performance
            point1_v4 = (((point1_v4[0] / (abs(point1_v4[3]) + 2.2250738585072014e-308) + 1) * screen_width / 2,
                          (point1_v4[1] / (abs(point1_v4[3]) + 2.2250738585072014e-308) + 1) * screen_height / 2))
            point2_v4 = (((point2_v4[0] / (abs(point2_v4[3]) + 2.2250738585072014e-308) + 1) * screen_width / 2,
                          (point2_v4[1] / (abs(point2_v4[3]) + 2.2250738585072014e-308) + 1) * screen_height / 2))
            point3_v4 = (((point3_v4[0] / (abs(point3_v4[3]) + 2.2250738585072014e-308) + 1) * screen_width / 2,
                          (point3_v4[1] / (abs(point3_v4[3]) + 2.2250738585072014e-308) + 1) * screen_height / 2))
            point4_v4 = (((point4_v4[0] / (abs(point4_v4[3]) + 2.2250738585072014e-308) + 1) * screen_width / 2,
                          (point4_v4[1] / (abs(point4_v4[3]) + 2.2250738585072014e-308) + 1) * screen_height / 2))

            a=int(z/100000)

            # tcl_code.append((z,f"{canvas} coords {i} {point1_v4[0]} {point1_v4[1]} {point2_v4[0]} {point2_v4[1]} {point3_v4[0]} {point3_v4[1]} {point4_v4[0]} {point4_v4[1]}\n"
            #                 f"{canvas} itemconfigure {i} -fill #{tri[0]:02x}{tri[1]:02x}{tri[2]:002x}\n"))

            tcl_code.append((z,f"{canvas} create poly {point1_v4[0]} {point1_v4[1]} {point2_v4[0]} {point2_v4[1]} "
                               f"{point3_v4[0]} {point3_v4[1]} {point4_v4[0]} {point4_v4[1]} -tag 3d "
                               f"-fill #{tri[0]:02x}{tri[1]:02x}{tri[2]:02x}\n"))
        size=len(tcl_code)
        tcl_code=sorted(tcl_code,reverse=True)
        tcl_code=[string for _, string in tcl_code]

        # for i in range(size+1,POLYGON_COUNT):
        #     tcl_code.append(f"{canvas} coords {i} 0 0 0 0 0 0 0 0\n"
        #                     f"{canvas} itemconfigure {i} -fill #000000\n")

        return GameToTK().draw_code("".join(tcl_code))