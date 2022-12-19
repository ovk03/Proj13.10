"""Optimized to the maximum. """

import threading
from ._tk_inter_inter import *
from .structures import *
from .__main__ import EngineTypeSingleton
import time

"""Onni Kolkka 
150832953 (student number)
created 15.12.2022 21.18
"""


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

    tri_colors = ["000000" for _ in range(POLYGON_COUNT)]
    def __init__(self, pos=(0,)*3, rot=(0,)*3):
        self.camera_pos = pos
        self.camera_rot = rot
        self.msg_del=0
        # self.is_debug = False
        # TODO: this
        self.log("Have you implemented area culling yet? (pref quad/oct tree)","CYAN")
        # remove this after it has been implemented

    def render(self, buffer=None, *_):
        was_rendered=False
        tcl_code=[]
        was_rendered = self.render3d(buffer,True)
        return was_rendered

    def render3d(self, buffer=None, cache: bool = False) -> bool:
        """really complicated and unreadable code, but REALLY OPTIMIZED for rendering objects with tkinter
        Input is tuple of form:
        ((1,1,1),(1,1,1),(1,2,3))
    
        This is composed of two parts.
        # 1. constants
        # 2. calculations
        """

        # 1. constants

        if type(buffer) is not list:
            buffer = self.buffer
        elif cache:
            self.buffer = buffer

        x_fov = 9 / 10/2
        y_fov = 16 / 10/2
        near = .001
        far = 1000
        fov_near_x = -x_fov
        fov_near_y = -y_fov
        far_far_near = far / (far - near)
        far_near_near_far = near * far / (far - near)

        c_pos_x,c_pos_y,c_pos_z = self.camera_pos
        
        screen_width, screen_height, canvas = GameToTK().get_data_for_rend()

        sa = math.sin((self.camera_rot[0]) * math.radians(1))
        ca = math.cos((self.camera_rot[0]) * math.radians(1))
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

        # proj_m4 = (
        #     x_fov, 0, 0, 0,
        #     0, y_fov, 0, 0,
        #     0, 0, far / (far - near), -near * far / (far - near),
        #     0, 0, 1, 0)

        cam_fwd_vec = (trans_m3x3[6],trans_m3x3[7],trans_m3x3[8])

        tcl_code = []


        # 2. calculations



        # region confusing math Keep collapsed
        z_list=[]
        for tri in buffer:
            z_list.append(
        ((tri[0]-c_pos_x) * (tri[0]-c_pos_x) + (tri[1]-c_pos_y) *
         (tri[1]-c_pos_y) + (tri[2]-c_pos_z) * (tri[2]-c_pos_z)) +
        ((tri[3]-c_pos_x) * (tri[3]-c_pos_x) + (tri[4]-c_pos_y) *
         (tri[4]-c_pos_y) + (tri[5]-c_pos_z) * (tri[5]-c_pos_z)) +
        ((tri[6]-c_pos_x) * (tri[6]-c_pos_x) + (tri[7]-c_pos_y) *
         (tri[7]-c_pos_y) + (tri[8]-c_pos_z) * (tri[8]-c_pos_z)) +
        ((tri[9]-c_pos_x) * (tri[9]-c_pos_x) + (tri[10]-c_pos_y) *
         (tri[10]-c_pos_y) + (tri[11]-c_pos_z) * (tri[11]-c_pos_z)))
        buffer = [i[1] for i in sorted(zip(z_list,buffer))]

        lenght = 0

        # Each calculation inside this loop is run approximately 1e9 times in only 20 seconds
        # For that reason I have to use all possible optimizations, even though it wont result in readable code
        for tri in buffer:
            """This has explanation in USER MANUAL. This section doesn't contain comments as they 
            wouldn't be sufficient in explaining this and that would increase the rowcount further"""

            # TODO: backface culling
            if cam_fwd_vec[0]*tri[15]+ \
               cam_fwd_vec[1]*tri[16]+ \
               cam_fwd_vec[2]*tri[17] > 0:
                continue

            # region confusing math Keep collapsed
            point1_v4 = (
                trans_m3x3[0] * (tri[0]-c_pos_x)+
                trans_m3x3[3] * (tri[1]-c_pos_y)+
                trans_m3x3[6] * (tri[2]-c_pos_z),
                trans_m3x3[1] * (tri[0]-c_pos_x)+
                trans_m3x3[4] * (tri[1]-c_pos_y)+
                trans_m3x3[7] * (tri[2]-c_pos_z),
                trans_m3x3[2] * (tri[0]-c_pos_x)+
                trans_m3x3[5] * (tri[1]-c_pos_y)+
                trans_m3x3[8] * (tri[2]-c_pos_z))
            point2_v4 = (
                trans_m3x3[0] * (tri[3]-c_pos_x)+
                trans_m3x3[3] * (tri[4]-c_pos_y)+
                trans_m3x3[6] * (tri[5]-c_pos_z),
                trans_m3x3[1] * (tri[3]-c_pos_x)+
                trans_m3x3[4] * (tri[4]-c_pos_y)+
                trans_m3x3[7] * (tri[5]-c_pos_z),
                trans_m3x3[2] * (tri[3]-c_pos_x)+
                trans_m3x3[5] * (tri[4]-c_pos_y)+
                trans_m3x3[8] * (tri[5]-c_pos_z))
            point3_v4 = (
                trans_m3x3[0] * (tri[6]-c_pos_x)+
                trans_m3x3[3] * (tri[7]-c_pos_y)+
                trans_m3x3[6] * (tri[8]-c_pos_z),
                trans_m3x3[1] * (tri[6]-c_pos_x)+
                trans_m3x3[4] * (tri[7]-c_pos_y)+
                trans_m3x3[7] * (tri[8]-c_pos_z),
                trans_m3x3[2] * (tri[6]-c_pos_x)+
                trans_m3x3[5] * (tri[7]-c_pos_y)+
                trans_m3x3[8] * (tri[8]-c_pos_z))
            point4_v4 = (
                trans_m3x3[0] * (tri[9]-c_pos_x)+
                trans_m3x3[3] * (tri[10]-c_pos_y)+
                trans_m3x3[6] * (tri[11]-c_pos_z),
                trans_m3x3[1] * (tri[9]-c_pos_x)+
                trans_m3x3[4] * (tri[10]-c_pos_y)+
                trans_m3x3[7] * (tri[11]-c_pos_z),
                trans_m3x3[2] * (tri[9]-c_pos_x)+
                trans_m3x3[5] * (tri[10]-c_pos_y)+
                trans_m3x3[8] * (tri[11]-c_pos_z))

            if (0.0 >= point1_v4[2]) and \
               (0.0 >= point2_v4[2]) and \
               (0.0 >= point3_v4[2]) and \
               (0.0 >= point4_v4[2]):
                continue

            point1_v4 = (
                fov_near_x * point1_v4[0],
                fov_near_y * point1_v4[1],
                point1_v4[2]*far_far_near-far_near_near_far,
                point1_v4[2])
            point2_v4 = (
                fov_near_x * point2_v4[0],
                fov_near_y * point2_v4[1],
                point2_v4[2]*far_far_near-far_near_near_far,
                point2_v4[2])
            point3_v4 = (
                fov_near_x * point3_v4[0],
                fov_near_y * point3_v4[1],
                point3_v4[2]*far_far_near-far_near_near_far,
                point3_v4[2])
            point4_v4 = (
                fov_near_x * point4_v4[0],
                fov_near_y * point4_v4[1],
                point4_v4[2]*far_far_near-far_near_near_far,
                point4_v4[2])

            # TODO: maybe skiping these checks and relying on area culling would result in better performance
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

            # region append geometry

            if (0.0 < point1_v4[2]) and \
               (0.0 < point2_v4[2]) and \
               (0.0 < point3_v4[2]) and \
               (0.0 < point4_v4[2]):

                point1_v4 = (((point1_v4[0]/point1_v4[3]+1)*screen_width/2,(point1_v4[1]/point1_v4[3]+1)*screen_height/2))
                point2_v4 = (((point2_v4[0]/point2_v4[3]+1)*screen_width/2,(point2_v4[1]/point2_v4[3]+1)*screen_height/2))
                point3_v4 = (((point3_v4[0]/point3_v4[3]+1)*screen_width/2,(point3_v4[1]/point3_v4[3]+1)*screen_height/2))
                point4_v4 = (((point4_v4[0]/point4_v4[3]+1)*screen_width/2,(point4_v4[1]/point4_v4[3]+1)*screen_height/2))
                tcl_code.append(f"{canvas} coords {lenght} {point1_v4[0]} {point1_v4[1]} {point2_v4[0]} {point2_v4[1]} "
                                f"{point3_v4[0]} {point3_v4[1]} {point4_v4[0]} {point4_v4[1]}\n"
                                f"{canvas} itemconfigure {lenght} -fill #{tri[12]:02x}{tri[13]:02x}{tri[14]:002x}\n")

            else: # OH NO THIS IS GONNA GET MESSY
                # TODO: cull Z  in a way that makes sense perspective wise
                c1 = (0.0 >= point1_v4[2])
                c2 = (0.0 >= point2_v4[2])
                c3 = (0.0 >= point3_v4[2])
                c4 = (0.0 >= point4_v4[2])

                if c1 and c2 and c3 and c4:
                    continue

                clip_count=(
                       (1 if c1 else 0)+
                       (1 if c2 else 0)+
                       (1 if c3 else 0)+
                       (1 if c4 else 0))

                if (clip_count == 2 and ((c1 == c2) or (c1 == c4))) or clip_count == 3:
                    if clip_count == 2:
                        if c1:
                            if c2: #c12  self.log("Z clip #12","COLORBG")
                                a=1+point1_v4[2]/(point4_v4[2]-point1_v4[2])
                                point1_v4 = (point1_v4[0]*a+point4_v4[0]*(1-a),
                                             point1_v4[1]*a+point4_v4[1]*(1-a),
                                             point1_v4[2]*a+point4_v4[2]*(1-a),
                                             point1_v4[3]*a+point4_v4[3]*(1-a))
                                a=1+point2_v4[2]/(point3_v4[2]-point2_v4[2])
                                point2_v4 = (point2_v4[0]*a+point3_v4[0]*(1-a),
                                             point2_v4[1]*a+point3_v4[1]*(1-a),
                                             point2_v4[2]*a+point3_v4[2]*(1-a),
                                             point2_v4[3]*a+point3_v4[3]*(1-a))
                            else: #c14 self.log("Z clip #14","COLORBG")
                                a=1+point1_v4[2]/(point2_v4[2]-point1_v4[2])
                                point1_v4 = (point1_v4[0]*a+point2_v4[0]*(1-a),
                                             point1_v4[1]*a+point2_v4[1]*(1-a),
                                             point1_v4[2]*a+point2_v4[2]*(1-a),
                                             point1_v4[3]*a+point2_v4[3]*(1-a))
                                a=1+point4_v4[2]/(point3_v4[2]-point4_v4[2])
                                point4_v4 = (point4_v4[0]*a+point3_v4[0]*(1-a),
                                             point4_v4[1]*a+point3_v4[1]*(1-a),
                                             point4_v4[2]*a+point3_v4[2]*(1-a),
                                             point4_v4[3]*a+point3_v4[3]*(1-a))
                        elif c2: #c23 self.log("Z clip #23","COLORBG")
                                a=1+point2_v4[2]/(point1_v4[2]-point2_v4[2])
                                point2_v4 = (point2_v4[0]*a+point1_v4[0]*(1-a),
                                             point2_v4[1]*a+point1_v4[1]*(1-a),
                                             point2_v4[2]*a+point1_v4[2]*(1-a),
                                             point2_v4[3]*a+point1_v4[3]*(1-a))
                                a=1+point3_v4[2]/(point4_v4[2]-point3_v4[2])
                                point3_v4 = (point3_v4[0]*a+point4_v4[0]*(1-a),
                                             point3_v4[1]*a+point4_v4[1]*(1-a),
                                             point3_v4[2]*a+point4_v4[2]*(1-a),
                                             point3_v4[3]*a+point4_v4[3]*(1-a))
                        else:    #c34 self.log("Z clip #34","COLORBG")
                                a=1+point3_v4[2]/(point2_v4[2]-point3_v4[2])
                                point3_v4 = (point3_v4[0]*a+point2_v4[0]*(1-a),
                                             point3_v4[1]*a+point2_v4[1]*(1-a),
                                             point3_v4[2]*a+point2_v4[2]*(1-a),
                                             point3_v4[3]*a+point2_v4[3]*(1-a))
                                a=1+point4_v4[2]/(point1_v4[2]-point4_v4[2])
                                point4_v4 = (point4_v4[0]*a+point1_v4[0]*(1-a),
                                             point4_v4[1]*a+point1_v4[1]*(1-a),
                                             point4_v4[2]*a+point1_v4[2]*(1-a),
                                             point4_v4[3]*a+point1_v4[3]*(1-a))
                    elif not c1: #c24 self.log("Z clip #234","COLORBG")
                                a=1+point2_v4[2]/(point1_v4[2]-point2_v4[2])
                                point2_v4 = (point2_v4[0]*a+point1_v4[0]*(1-a),
                                             point2_v4[1]*a+point1_v4[1]*(1-a),
                                             point2_v4[2]*a+point1_v4[2]*(1-a),
                                             point2_v4[3]*a+point1_v4[3]*(1-a))
                                a=1+point4_v4[2]/(point1_v4[2]-point4_v4[2])
                                point4_v4 = (point4_v4[0]*a+point1_v4[0]*(1-a),
                                             point4_v4[1]*a+point1_v4[1]*(1-a),
                                             point4_v4[2]*a+point1_v4[2]*(1-a),
                                             point4_v4[3]*a+point1_v4[3]*(1-a))
                                point3_v4 = point4_v4
                    elif not c2: #c134 self.log("Z clip #134","COLORBG")
                                a=1+point1_v4[2]/(point2_v4[2]-point1_v4[2])
                                point1_v4 = (point1_v4[0]*a+point2_v4[0]*(1-a),
                                             point1_v4[1]*a+point2_v4[1]*(1-a),
                                             point1_v4[2]*a+point2_v4[2]*(1-a),
                                             point1_v4[3]*a+point2_v4[3]*(1-a))
                                a=1+point3_v4[2]/(point2_v4[2]-point3_v4[2])
                                point3_v4 = (point3_v4[0]*a+point2_v4[0]*(1-a),
                                             point3_v4[1]*a+point2_v4[1]*(1-a),
                                             point3_v4[2]*a+point2_v4[2]*(1-a),
                                             point3_v4[3]*a+point2_v4[3]*(1-a))
                                point4_v4 = point1_v4
                    elif not c3: #c124 self.log("Z clip #124","COLORBG")
                                a=1+point2_v4[2]/(point3_v4[2]-point2_v4[2])
                                point2_v4 = (point2_v4[0]*a+point3_v4[0]*(1-a),
                                             point2_v4[1]*a+point3_v4[1]*(1-a),
                                             point2_v4[2]*a+point3_v4[2]*(1-a),
                                             point2_v4[3]*a+point3_v4[3]*(1-a))
                                a=1+point4_v4[2]/(point3_v4[2]-point4_v4[2])
                                point4_v4 = (point4_v4[0]*a+point3_v4[0]*(1-a),
                                             point4_v4[1]*a+point3_v4[1]*(1-a),
                                             point4_v4[2]*a+point3_v4[2]*(1-a),
                                             point4_v4[3]*a+point3_v4[3]*(1-a))
                                point1_v4 = point2_v4
                    else:        #c123 self.log("Z clip #123","COLORBG")
                                a=1+point1_v4[2]/(point4_v4[2]-point1_v4[2])
                                point1_v4 = (point1_v4[0]*a+point4_v4[0]*(1-a),
                                             point1_v4[1]*a+point4_v4[1]*(1-a),
                                             point1_v4[2]*a+point4_v4[2]*(1-a),
                                             point1_v4[3]*a+point4_v4[3]*(1-a))
                                a=1+point3_v4[2]/(point4_v4[2]-point3_v4[2])
                                point3_v4 = (point3_v4[0]*a+point4_v4[0]*(1-a),
                                             point3_v4[1]*a+point4_v4[1]*(1-a),
                                             point3_v4[2]*a+point4_v4[2]*(1-a),
                                             point3_v4[3]*a+point4_v4[3]*(1-a))
                                point2_v4 = point3_v4

                    point1_v4 = ((point1_v4[0]/point1_v4[3]+1)*screen_width/2,(point1_v4[1]/point1_v4[3]+1)*screen_height/2)
                    point2_v4 = ((point2_v4[0]/point2_v4[3]+1)*screen_width/2,(point2_v4[1]/point2_v4[3]+1)*screen_height/2)
                    point3_v4 = ((point3_v4[0]/point3_v4[3]+1)*screen_width/2,(point3_v4[1]/point3_v4[3]+1)*screen_height/2)
                    point4_v4 = ((point4_v4[0]/point4_v4[3]+1)*screen_width/2,(point4_v4[1]/point4_v4[3]+1)*screen_height/2)
                    tcl_code.append(f"{canvas} coords {lenght} {point1_v4[0]} {point1_v4[1]} {point2_v4[0]} {point2_v4[1]} "
                                    f"{point3_v4[0]} {point3_v4[1]} {point4_v4[0]} {point4_v4[1]}\n"
                                    f"{canvas} itemconfigure {lenght} -fill #{tri[12]:02x}{tri[13]:02x}{tri[14]:002x}\n")

                elif clip_count == 1: # In this case we need more polygons to represent this polygon
                    if c1:   #c1 self.log("Z clip #1","COLORBG")
                        a1=1+point1_v4[2]/(point2_v4[2]-point1_v4[2])
                        a2=1+point1_v4[2]/(point4_v4[2]-point1_v4[2])
                        pos=point1_v4
                        point1_v4 = (pos[0]*a1+point2_v4[0]*(1-a1),
                                     pos[1]*a1+point2_v4[1]*(1-a1),
                                     pos[2]*a1+point2_v4[2]*(1-a1),
                                     pos[3]*a1+point2_v4[3]*(1-a1))
                        point5_v4 = (pos[0]*a2+point4_v4[0]*(1-a2),
                                     pos[1]*a2+point4_v4[1]*(1-a2),
                                     pos[2]*a2+point4_v4[2]*(1-a2),
                                     pos[3]*a2+point4_v4[3]*(1-a2))
                        point6_v4 = point3_v4
                        point7_v4 = point4_v4
                        point8_v4 = point4_v4
                        point4_v4 = point5_v4  # move this last, as other depend on this val
                    elif c2: #c2 self.log("Z clip #2","COLORBG")
                        a1=1+point2_v4[2]/(point3_v4[2]-point2_v4[2])
                        a2=1+point2_v4[2]/(point1_v4[2]-point2_v4[2])
                        pos=point2_v4
                        point2_v4 = (pos[0]*a1+point3_v4[0]*(1-a1),
                                     pos[1]*a1+point3_v4[1]*(1-a1),
                                     pos[2]*a1+point3_v4[2]*(1-a1),
                                     pos[3]*a1+point3_v4[3]*(1-a1))
                        point5_v4 = (pos[0]*a2+point1_v4[0]*(1-a2),
                                     pos[1]*a2+point1_v4[1]*(1-a2),
                                     pos[2]*a2+point1_v4[2]*(1-a2),
                                     pos[3]*a2+point1_v4[3]*(1-a2))
                        point6_v4 = point4_v4
                        point7_v4 = point1_v4
                        point8_v4 = point1_v4
                        point1_v4 = point5_v4  # move this last, as other depend on this val
                    elif c3: #c3 self.log("Z clip #3","COLORBG")
                        a1=1+point3_v4[2]/(point4_v4[2]-point3_v4[2])
                        a2=1+point3_v4[2]/(point2_v4[2]-point3_v4[2])
                        pos=point3_v4
                        point3_v4 = (pos[0]*a1+point4_v4[0]*(1-a1),
                                     pos[1]*a1+point4_v4[1]*(1-a1),
                                     pos[2]*a1+point4_v4[2]*(1-a1),
                                     pos[3]*a1+point4_v4[3]*(1-a1))
                        point5_v4 = (pos[0]*a2+point2_v4[0]*(1-a2),
                                     pos[1]*a2+point2_v4[1]*(1-a2),
                                     pos[2]*a2+point2_v4[2]*(1-a2),
                                     pos[3]*a2+point2_v4[3]*(1-a2))
                        point6_v4 = point1_v4
                        point7_v4 = point2_v4
                        point8_v4 = point2_v4
                        point2_v4 = point5_v4 # move this last, as other depend on this val
                    else:    #c4 self.log("Z clip #4","COLORBG")
                        a1=1+point4_v4[2]/(point1_v4[2]-point4_v4[2])
                        a2=1+point4_v4[2]/(point3_v4[2]-point4_v4[2])
                        pos=point4_v4
                        point4_v4 = (pos[0]*a1+point1_v4[0]*(1-a1),
                                     pos[1]*a1+point1_v4[1]*(1-a1),
                                     pos[2]*a1+point1_v4[2]*(1-a1),
                                     pos[3]*a1+point1_v4[3]*(1-a1))
                        point5_v4 = (pos[0]*a2+point3_v4[0]*(1-a2),
                                     pos[1]*a2+point3_v4[1]*(1-a2),
                                     pos[2]*a2+point3_v4[2]*(1-a2),
                                     pos[3]*a2+point3_v4[3]*(1-a2))
                        point6_v4 = point2_v4
                        point7_v4 = point3_v4
                        point8_v4 = point3_v4
                        point3_v4 = point5_v4  # move this last, as other depend on this val

                    point1_v4 = ((point1_v4[0]/point1_v4[3]+1)*screen_width/2,(point1_v4[1]/point1_v4[3]+1)*screen_height/2)
                    point2_v4 = ((point2_v4[0]/point2_v4[3]+1)*screen_width/2,(point2_v4[1]/point2_v4[3]+1)*screen_height/2)
                    point3_v4 = ((point3_v4[0]/point3_v4[3]+1)*screen_width/2,(point3_v4[1]/point3_v4[3]+1)*screen_height/2)
                    point4_v4 = ((point4_v4[0]/point4_v4[3]+1)*screen_width/2,(point4_v4[1]/point4_v4[3]+1)*screen_height/2)
                    point5_v4 = ((point5_v4[0]/point5_v4[3]+1)*screen_width/2,(point5_v4[1]/point5_v4[3]+1)*screen_height/2)
                    point6_v4 = ((point6_v4[0]/point6_v4[3]+1)*screen_width/2,(point6_v4[1]/point6_v4[3]+1)*screen_height/2)
                    point7_v4 = ((point7_v4[0]/point7_v4[3]+1)*screen_width/2,(point7_v4[1]/point7_v4[3]+1)*screen_height/2)
                    point8_v4 = ((point8_v4[0]/point8_v4[3]+1)*screen_width/2,(point8_v4[1]/point8_v4[3]+1)*screen_height/2)
                    tcl_code.append(f"{canvas} coords {lenght} {point1_v4[0]} {point1_v4[1]} {point2_v4[0]} {point2_v4[1]} "
                                    f"{point3_v4[0]} {point3_v4[1]} {point4_v4[0]} {point4_v4[1]}\n"
                                    f"{canvas} itemconfigure ¤ -fill #{tri[12]:02x}{tri[13]:02x}{tri[14]:002x}\n")
                    tcl_code.append(f"{canvas} coords {lenght} {point5_v4[0]} {point5_v4[1]} {point6_v4[0]} {point6_v4[1]} "
                                    f"{point7_v4[0]} {point7_v4[1]} {point8_v4[0]} {point8_v4[1]}\n"
                                    f"{canvas} itemconfigure {lenght} -fill #{tri[12]:02x}{tri[13]:02x}{tri[14]:002x}\n")
            # TODO: make this whole section shorter without functions, as they have proven themselves too slo
            # endregion append geom

            if lenght == POLYGON_COUNT-1:
                if self.msg_del % 100 == 0:
                    self.log(f"Polygons on screen ({len(tcl_code)}) exceed polygon pool of {POLYGON_COUNT}"
                             , "YELLOW","COLORBG")
                self.msg_del += 1
                break
            lenght+=1
            #endregion


        #endregion

        for i in range(len(tcl_code), POLYGON_COUNT):
            tcl_code.append(f"{canvas} coords {i} 0 0 0 0 0 0 0 0\n")


        return GameToTK().draw_code("".join(tcl_code))