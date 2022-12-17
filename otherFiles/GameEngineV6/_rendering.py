"""Optimized to the maximum. Does pretty much the same as render.py"""
"""Onni Kolkka 
150832953 (student number)
created 15.12.2022 21.18
"""


import threading
from ._tk_inter_inter import *
from .structures import *
import time

class CameraRenderOptimized(metaclass=EngineType):
    
    buffer=None
    inter=None

    camera_pos = ()
    camera_rot = ()
    sinx = 0.0
    cosx = 0.0
    siny = 0.0
    cosy = 0.0
    sinz = 0.0
    cosz = 0.0


    def __init__(self, pos=(0,)*3, rot=(0,)*3):
        self.inter = GameToTK()
        self.camera_pos = pos
        self.camera_rot = rot



    def render(self, buffer=None, cache: bool = False) -> bool:
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
    
        sinx = math.sin(self.camera_rot[0] * math.radians(1))
        cosx = math.cos(self.camera_rot[0] * math.radians(1))
        siny = math.sin(self.camera_rot[1] * math.radians(1))
        cosy = math.cos(self.camera_rot[1] * math.radians(1))
        sinz = math.sin(self.camera_rot[2] * math.radians(1))
        cosz = math.cos(self.camera_rot[2] * math.radians(1))
    
        x_fov = 9 / 10
        y_fov = 16 / 10
        near = 0.1
        far = 1000
        fov_near_x=-x_fov
        fov_near_y=-y_fov
        far_near_far=far/(far-near)

        c_pos_x,c_pos_y,c_pos_z = self.camera_pos
        
        screen_width, screen_height, canvas = self.inter.get_data_for_rend()
    
        trans_m3x3 = (cosx * cosy, cosx * siny * sinz - sinx * cosz,
                      cosx * siny * cosz + sinx * sinz,
                      sinx * cosy, sinx * siny * sinz + cosx * cosz,
                      sinx * siny * cosz - cosx * sinz,
                      -siny, cosy * sinz, cosy * cosz)
        proj_m4 = (
            x_fov, 0, 0, 0,
            0, y_fov, 0, 0,
            0, 0, far / (far - near), -near * far / (far - near),
            0, 0, 1, 0)


        tcl_code = []
    
        # 3. calculations
        i=0
        for tri in buffer:
            point1_v4 = (
                trans_m3x3[0] * (tri[0]-c_pos_x)+
                trans_m3x3[1] * (tri[1]-c_pos_y)+
                trans_m3x3[2] * (tri[2]-c_pos_z),
                trans_m3x3[3] * (tri[0]-c_pos_x)+
                trans_m3x3[4] * (tri[1]-c_pos_y)+
                trans_m3x3[5] * (tri[2]-c_pos_z),
                trans_m3x3[6] * (tri[0]-c_pos_x)+
                trans_m3x3[7] * (tri[1]-c_pos_y)+
                trans_m3x3[8] * (tri[2]-c_pos_z))
            point2_v4 = (
                trans_m3x3[0] * (tri[3]-c_pos_x)+
                trans_m3x3[1] * (tri[4]-c_pos_y)+
                trans_m3x3[2] * (tri[5]-c_pos_z),
                trans_m3x3[3] * (tri[3]-c_pos_x)+
                trans_m3x3[4] * (tri[4]-c_pos_y)+
                trans_m3x3[5] * (tri[5]-c_pos_z),
                trans_m3x3[6] * (tri[3]-c_pos_x)+
                trans_m3x3[7] * (tri[4]-c_pos_y)+
                trans_m3x3[8] * (tri[5]-c_pos_z))
            point3_v4 = (
                trans_m3x3[0] * (tri[6]-c_pos_x)+
                trans_m3x3[1] * (tri[7]-c_pos_y)+
                trans_m3x3[2] * (tri[8]-c_pos_z),
                trans_m3x3[3] * (tri[6]-c_pos_x)+
                trans_m3x3[4] * (tri[7]-c_pos_y)+
                trans_m3x3[5] * (tri[8]-c_pos_z),
                trans_m3x3[6] * (tri[6]-c_pos_x)+
                trans_m3x3[7] * (tri[7]-c_pos_y)+
                trans_m3x3[8] * (tri[8]-c_pos_z))
            point4_v4 = (
                trans_m3x3[0] * (tri[9]-c_pos_x)+
                trans_m3x3[1] * (tri[10]-c_pos_y)+
                trans_m3x3[2] * (tri[11]-c_pos_z),
                trans_m3x3[3] * (tri[9]-c_pos_x)+
                trans_m3x3[4] * (tri[10]-c_pos_y)+
                trans_m3x3[5] * (tri[11]-c_pos_z),
                trans_m3x3[6] * (tri[9]-c_pos_x)+
                trans_m3x3[7] * (tri[10]-c_pos_y)+
                trans_m3x3[8] * (tri[11]-c_pos_z))

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
            point1_v4 = (((point1_v4[0] / (math.fabs(point1_v4[3]) + 2.2250738585072014e-308) + 1) * screen_width / 2,
                          (point1_v4[1] / (math.fabs(point1_v4[3]) + 2.2250738585072014e-308) + 1) * screen_height / 2))
            point2_v4 = (((point2_v4[0] / (math.fabs(point2_v4[3]) + 2.2250738585072014e-308) + 1) * screen_width / 2,
                          (point2_v4[1] / (math.fabs(point2_v4[3]) + 2.2250738585072014e-308) + 1) * screen_height / 2))
            point3_v4 = (((point3_v4[0] / (math.fabs(point3_v4[3]) + 2.2250738585072014e-308) + 1) * screen_width / 2,
                          (point3_v4[1] / (math.fabs(point3_v4[3]) + 2.2250738585072014e-308) + 1) * screen_height / 2))
            point4_v4 = (((point4_v4[0] / (math.fabs(point4_v4[3]) + 2.2250738585072014e-308) + 1) * screen_width / 2,
                          (point4_v4[1] / (math.fabs(point4_v4[3]) + 2.2250738585072014e-308) + 1) * screen_height / 2))


            i+=1
            tcl_code.append(f"{canvas} coords {i} {point1_v4[0]} {point1_v4[1]} {point2_v4[0]} {point2_v4[1]} {point3_v4[0]} {point3_v4[1]} {point4_v4[0]} {point4_v4[1]}\n")
        size=len(tcl_code)
        for i in range(size+1,4096):
            tcl_code.append(f"{canvas} coords {i} 0 0 0 0 0 0 0 0\n")
        return self.inter.draw_code("".join(tcl_code))