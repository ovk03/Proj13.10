"""Optimized to the maximum. Does pretty much the same as render.py"""
"""Onni Kolkka 
150832953 (student number)
created 15.12.2022 21.18
"""


import threading
from ._tk_inter_inter import *
from .structures import *
import time


class CameraRenderOptimized:
    
    buffer=None
    
    camera_pos = ()
    camera_rot = ()
    sinx = 0.0
    cosx = 0.0
    siny = 0.0
    cosy = 0.0
    sinz = 0.0
    cosz = 0.0

    def __init__(self, pos=(0,) * 3, rot=(0,) * 3):
        self.inter = Interpeter()
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
        near = 1
        far = 1000

        c_pos_x,c_pos_y,c_pos_z = self.camera_pos
        
        screen_width, screen_height, canvas  = self.inter.get_data_for_rend()
    
        trans_m3x3 = (cosx * cosy, cosx * siny * sinz - sinx * cosz,
                      cosx * siny * cosz + sinx * sinz,
                      sinx * cosy, sinx * siny * sinz + cosx * cosz,
                      sinx * siny * cosz - cosx * sinz,
                      -siny, cosy * sinz, cosy * cosz)
        proj_m4 = (
            x_fov, 0, 0, 0,
            0, y_fov, 0, 0,
            0, 0, far / (far - near), 1,
            0, 0, -near * far / (far - near), 0)
    
        tcl_code = []
    
        # 3. calculations
        for i,tri in enumerate(buffer):
            point1_v4 = (
                trans_m3x3[0] * (tri[0]-c_pos_x)+
                trans_m3x3[1] * (tri[1]-c_pos_y)+
                trans_m3x3[2] * (tri[2]-c_pos_z),
                trans_m3x3[3] * (tri[0]-c_pos_x)+
                trans_m3x3[4] * (tri[1]-c_pos_y)+
                trans_m3x3[5] * (tri[2]-c_pos_z),
                trans_m3x3[6] * (tri[0]-c_pos_x)+
                trans_m3x3[7] * (tri[1]-c_pos_y)+
                trans_m3x3[8] * (tri[2]-c_pos_z),1)
            point2_v4 = (
                trans_m3x3[0] * (tri[3]-c_pos_x)+
                trans_m3x3[1] * (tri[4]-c_pos_y)+
                trans_m3x3[2] * (tri[5]-c_pos_z),
                trans_m3x3[3] * (tri[3]-c_pos_x)+
                trans_m3x3[4] * (tri[4]-c_pos_y)+
                trans_m3x3[5] * (tri[5]-c_pos_z),
                trans_m3x3[6] * (tri[3]-c_pos_x)+
                trans_m3x3[7] * (tri[4]-c_pos_y)+
                trans_m3x3[8] * (tri[5]-c_pos_z),1)
            point3_v4 = (
                trans_m3x3[0] * (tri[6]-c_pos_x)+
                trans_m3x3[1] * (tri[7]-c_pos_y)+
                trans_m3x3[2] * (tri[8]-c_pos_z),
                trans_m3x3[3] * (tri[6]-c_pos_x)+
                trans_m3x3[4] * (tri[7]-c_pos_y)+
                trans_m3x3[5] * (tri[8]-c_pos_z),
                trans_m3x3[6] * (tri[6]-c_pos_x)+
                trans_m3x3[7] * (tri[7]-c_pos_y)+
                trans_m3x3[8] * (tri[8]-c_pos_z),1)
            point4_v4 = (
                trans_m3x3[0] * (tri[9]-c_pos_x)+
                trans_m3x3[1] * (tri[10]-c_pos_y)+
                trans_m3x3[2] * (tri[11]-c_pos_z),
                trans_m3x3[3] * (tri[9]-c_pos_x)+
                trans_m3x3[4] * (tri[10]-c_pos_y)+
                trans_m3x3[5] * (tri[11]-c_pos_z),
                trans_m3x3[6] * (tri[9]-c_pos_x)+
                trans_m3x3[7] * (tri[10]-c_pos_y)+
                trans_m3x3[8] * (tri[11]-c_pos_z),1)

            # TODO: clamp them in a way that makes sense perspective wise
            if (0.0 > point1_v4[2]) or \
                    (0.0 > point2_v4[2]) or \
                    (0.0 > point2_v4[2]) or \
                    (0.0 > point4_v4[2]):
                continue

            point1_v4 = optimal_m4x4_times_v4_camera(proj_m4, point1_v4)
            point2_v4 = optimal_m4x4_times_v4_camera(proj_m4, point2_v4)
            point3_v4 = optimal_m4x4_times_v4_camera(proj_m4, point3_v4)
            point4_v4 = optimal_m4x4_times_v4_camera(proj_m4, point4_v4)

            # conversion to screen points
            # this used to be 3 different functions, but by merging them like this I saved alot of performance
            point1_v4 = (((point1_v4[0] / (point1_v4[3] + 1e-32) + 1) * screen_width / 2,
                          screen_height - (point1_v4[1] / (point1_v4[3] + 1e-32) + 1) * screen_height / 2))
            point2_v4 = (((point2_v4[0] / (point2_v4[3] + 1e-32) + 1) * screen_width / 2,
                          screen_height - (point2_v4[1] / (point2_v4[3] + 1e-32) + 1) * screen_height / 2))
            point3_v4 = (((point3_v4[0] / (point3_v4[3] + 1e-32) + 1) * screen_width / 2,
                          screen_height - (point3_v4[1] / (point3_v4[3] + 1e-32) + 1) * screen_height / 2))
            point4_v4 = (((point4_v4[0] / (point4_v4[3] + 1e-32) + 1) * screen_width / 2,
                          screen_height - (point4_v4[1] / (point4_v4[3] + 1e-32) + 1) * screen_height / 2))

            tcl_code.append(f"{canvas} coords {i} {point1_v4[0]} {point1_v4[1]} {point2_v4[0]} {point2_v4[1]} {point3_v4[0]} {point3_v4[1]} {point4_v4[0]} {point4_v4[1]}\n")

        boolean=self.inter.draw_code("".join(tcl_code))
        return boolean