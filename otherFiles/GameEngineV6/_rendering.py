"""Optimized to the maximum. """

import threading
from ._game_to_tk import *
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
        
        screen_w, screen_h, canvas = GameToTK().get_data_for_rend()

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
        for quad_data in buffer:
            z_list.append(
        ((quad_data[0]-c_pos_x) * (quad_data[0]-c_pos_x) + (quad_data[1]-c_pos_y) *
         (quad_data[1]-c_pos_y) + (quad_data[2]-c_pos_z) * (quad_data[2]-c_pos_z)) +
        ((quad_data[3]-c_pos_x) * (quad_data[3]-c_pos_x) + (quad_data[4]-c_pos_y) *
         (quad_data[4]-c_pos_y) + (quad_data[5]-c_pos_z) * (quad_data[5]-c_pos_z)) +
        ((quad_data[6]-c_pos_x) * (quad_data[6]-c_pos_x) + (quad_data[7]-c_pos_y) *
         (quad_data[7]-c_pos_y) + (quad_data[8]-c_pos_z) * (quad_data[8]-c_pos_z)) +
        ((quad_data[9]-c_pos_x) * (quad_data[9]-c_pos_x) + (quad_data[10]-c_pos_y) *
         (quad_data[10]-c_pos_y) + (quad_data[11]-c_pos_z) * (quad_data[11]-c_pos_z)))
        buffer = [i[1] for i in sorted(zip(z_list,buffer))]

        lenght = POLYGON_COUNT-1

        # Each calculation inside this loop is run approximately 1e9 times in only 20 seconds
        # For that reason I have to use all possible optimizations, even though it wont result in readable code

        # quad contains 4 points, color and normal, in total 18

        for quad_data in buffer:
            """This has explanation in USER MANUAL. This section doesn't contain comments as they 
            wouldn't be sufficient in explaining this and that would increase the rowcount further"""

            # TODO: backface culling
            if (quad_data[0]-c_pos_x)*quad_data[15]+ \
               (quad_data[1]-c_pos_y)*quad_data[16]+ \
               (quad_data[2]-c_pos_z)*quad_data[17] >= 0:
                continue

            # region confusing math Keep collapsed
            p1 = (
                trans_m3x3[0] * (quad_data[0]-c_pos_x)+
                trans_m3x3[3] * (quad_data[1]-c_pos_y)+
                trans_m3x3[6] * (quad_data[2]-c_pos_z),
                trans_m3x3[1] * (quad_data[0]-c_pos_x)+
                trans_m3x3[4] * (quad_data[1]-c_pos_y)+
                trans_m3x3[7] * (quad_data[2]-c_pos_z),
                trans_m3x3[2] * (quad_data[0]-c_pos_x)+
                trans_m3x3[5] * (quad_data[1]-c_pos_y)+
                trans_m3x3[8] * (quad_data[2]-c_pos_z))
            p2 = (
                trans_m3x3[0] * (quad_data[3]-c_pos_x)+
                trans_m3x3[3] * (quad_data[4]-c_pos_y)+
                trans_m3x3[6] * (quad_data[5]-c_pos_z),
                trans_m3x3[1] * (quad_data[3]-c_pos_x)+
                trans_m3x3[4] * (quad_data[4]-c_pos_y)+
                trans_m3x3[7] * (quad_data[5]-c_pos_z),
                trans_m3x3[2] * (quad_data[3]-c_pos_x)+
                trans_m3x3[5] * (quad_data[4]-c_pos_y)+
                trans_m3x3[8] * (quad_data[5]-c_pos_z))
            p3 = (
                trans_m3x3[0] * (quad_data[6]-c_pos_x)+
                trans_m3x3[3] * (quad_data[7]-c_pos_y)+
                trans_m3x3[6] * (quad_data[8]-c_pos_z),
                trans_m3x3[1] * (quad_data[6]-c_pos_x)+
                trans_m3x3[4] * (quad_data[7]-c_pos_y)+
                trans_m3x3[7] * (quad_data[8]-c_pos_z),
                trans_m3x3[2] * (quad_data[6]-c_pos_x)+
                trans_m3x3[5] * (quad_data[7]-c_pos_y)+
                trans_m3x3[8] * (quad_data[8]-c_pos_z))
            p4 = (
                trans_m3x3[0] * (quad_data[9]-c_pos_x)+
                trans_m3x3[3] * (quad_data[10]-c_pos_y)+
                trans_m3x3[6] * (quad_data[11]-c_pos_z),
                trans_m3x3[1] * (quad_data[9]-c_pos_x)+
                trans_m3x3[4] * (quad_data[10]-c_pos_y)+
                trans_m3x3[7] * (quad_data[11]-c_pos_z),
                trans_m3x3[2] * (quad_data[9]-c_pos_x)+
                trans_m3x3[5] * (quad_data[10]-c_pos_y)+
                trans_m3x3[8] * (quad_data[11]-c_pos_z))

            if (0.0 >= p1[2]) and \
               (0.0 >= p2[2]) and \
               (0.0 >= p3[2]) and \
               (0.0 >= p4[2]):
                continue

            p1 = (
                fov_near_x * p1[0],
                fov_near_y * p1[1],
                p1[2]*far_far_near-far_near_near_far,
                p1[2])
            p2 = (
                fov_near_x * p2[0],
                fov_near_y * p2[1],
                p2[2]*far_far_near-far_near_near_far,
                p2[2])
            p3 = (
                fov_near_x * p3[0],
                fov_near_y * p3[1],
                p3[2]*far_far_near-far_near_near_far,
                p3[2])
            p4 = (
                fov_near_x * p4[0],
                fov_near_y * p4[1],
                p4[2]*far_far_near-far_near_near_far,
                p4[2])

            # TODO: maybe skiping these checks and relying on area culling would result in better performance
            if (p1[0] > p1[3]) and \
               (p2[0] > p2[3]) and \
               (p3[0] > p3[3]) and \
               (p4[0] > p4[3]):
                continue
            if (p1[0] < -p1[3]) and \
               (p2[0] < -p2[3]) and \
               (p3[0] < -p3[3]) and \
               (p4[0] < -p4[3]):
                continue
            if (p1[1] > p1[3]) and \
               (p2[1] > p2[3]) and \
               (p3[1] > p3[3]) and \
               (p4[1] > p4[3]):
                continue
            if (p1[1] < -p1[3]) and \
               (p2[1] < -p2[3]) and \
               (p3[1] < -p3[3]) and \
               (p4[1] < -p4[3]):
                continue

            # region append geometry

            if (0.0 < p1[2]) and \
               (0.0 < p2[2]) and \
               (0.0 < p3[2]) and \
               (0.0 < p4[2]):

                p1 = ((p1[0]/p1[3]+1)*screen_w/2, (p1[1]/p1[3]+1)*screen_h/2)
                p2 = ((p2[0]/p2[3]+1)*screen_w/2, (p2[1]/p2[3]+1)*screen_h/2)
                p3 = ((p3[0]/p3[3]+1)*screen_w/2, (p3[1]/p3[3]+1)*screen_h/2)
                p4 = ((p4[0]/p4[3]+1)*screen_w/2, (p4[1]/p4[3]+1)*screen_h/2)
                tcl_code.append(f"{canvas} coords {lenght} {p1[0]} {p1[1]} {p2[0]} {p2[1]} "
                                f"{p3[0]} {p3[1]} {p4[0]} {p4[1]}\n"
                                f"{canvas} itemconfigure {lenght} -fill #{quad_data[12]:02x}{quad_data[13]:02x}{quad_data[14]:002x}\n")

            else: # OH NO. THIS IS GONNA GET MESSY
                c1 = (0.0 >= p1[2])
                c2 = (0.0 >= p2[2])
                c3 = (0.0 >= p3[2])
                c4 = (0.0 >= p4[2])

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
                                a=1+p1[2]/(p4[2]-p1[2])
                                p1 = (p1[0]*a+p4[0]*(1-a),
                                             p1[1]*a+p4[1]*(1-a),
                                             p1[2]*a+p4[2]*(1-a),
                                             p1[3]*a+p4[3]*(1-a))
                                a=1+p2[2]/(p3[2]-p2[2])
                                p2 = (p2[0]*a+p3[0]*(1-a),
                                             p2[1]*a+p3[1]*(1-a),
                                             p2[2]*a+p3[2]*(1-a),
                                             p2[3]*a+p3[3]*(1-a))
                            else: #c14 self.log("Z clip #14","COLORBG")
                                a=1+p1[2]/(p2[2]-p1[2])
                                p1 = (p1[0]*a+p2[0]*(1-a),
                                             p1[1]*a+p2[1]*(1-a),
                                             p1[2]*a+p2[2]*(1-a),
                                             p1[3]*a+p2[3]*(1-a))
                                a=1+p4[2]/(p3[2]-p4[2])
                                p4 = (p4[0]*a+p3[0]*(1-a),
                                             p4[1]*a+p3[1]*(1-a),
                                             p4[2]*a+p3[2]*(1-a),
                                             p4[3]*a+p3[3]*(1-a))
                        elif c2: #c23 self.log("Z clip #23","COLORBG")
                                a=1+p2[2]/(p1[2]-p2[2])
                                p2 = (p2[0]*a+p1[0]*(1-a),
                                             p2[1]*a+p1[1]*(1-a),
                                             p2[2]*a+p1[2]*(1-a),
                                             p2[3]*a+p1[3]*(1-a))
                                a=1+p3[2]/(p4[2]-p3[2])
                                p3 = (p3[0]*a+p4[0]*(1-a),
                                             p3[1]*a+p4[1]*(1-a),
                                             p3[2]*a+p4[2]*(1-a),
                                             p3[3]*a+p4[3]*(1-a))
                        else:    #c34 self.log("Z clip #34","COLORBG")
                                a=1+p3[2]/(p2[2]-p3[2])
                                p3 = (p3[0]*a+p2[0]*(1-a),
                                             p3[1]*a+p2[1]*(1-a),
                                             p3[2]*a+p2[2]*(1-a),
                                             p3[3]*a+p2[3]*(1-a))
                                a=1+p4[2]/(p1[2]-p4[2])
                                p4 = (p4[0]*a+p1[0]*(1-a),
                                             p4[1]*a+p1[1]*(1-a),
                                             p4[2]*a+p1[2]*(1-a),
                                             p4[3]*a+p1[3]*(1-a))
                    elif not c1: #c24 self.log("Z clip #234","COLORBG")
                                a=1+p2[2]/(p1[2]-p2[2])
                                p2 = (p2[0]*a+p1[0]*(1-a),
                                             p2[1]*a+p1[1]*(1-a),
                                             p2[2]*a+p1[2]*(1-a),
                                             p2[3]*a+p1[3]*(1-a))
                                a=1+p4[2]/(p1[2]-p4[2])
                                p4 = (p4[0]*a+p1[0]*(1-a),
                                             p4[1]*a+p1[1]*(1-a),
                                             p4[2]*a+p1[2]*(1-a),
                                             p4[3]*a+p1[3]*(1-a))
                                p3 = p4
                    elif not c2: #c134 self.log("Z clip #134","COLORBG")
                                a=1+p1[2]/(p2[2]-p1[2])
                                p1 = (p1[0]*a+p2[0]*(1-a),
                                             p1[1]*a+p2[1]*(1-a),
                                             p1[2]*a+p2[2]*(1-a),
                                             p1[3]*a+p2[3]*(1-a))
                                a=1+p3[2]/(p2[2]-p3[2])
                                p3 = (p3[0]*a+p2[0]*(1-a),
                                             p3[1]*a+p2[1]*(1-a),
                                             p3[2]*a+p2[2]*(1-a),
                                             p3[3]*a+p2[3]*(1-a))
                                p4 = p1
                    elif not c3: #c124 self.log("Z clip #124","COLORBG")
                                a=1+p2[2]/(p3[2]-p2[2])
                                p2 = (p2[0]*a+p3[0]*(1-a),
                                             p2[1]*a+p3[1]*(1-a),
                                             p2[2]*a+p3[2]*(1-a),
                                             p2[3]*a+p3[3]*(1-a))
                                a=1+p4[2]/(p3[2]-p4[2])
                                p4 = (p4[0]*a+p3[0]*(1-a),
                                             p4[1]*a+p3[1]*(1-a),
                                             p4[2]*a+p3[2]*(1-a),
                                             p4[3]*a+p3[3]*(1-a))
                                p1 = p2
                    else:        #c123 self.log("Z clip #123","COLORBG")
                                a=1+p1[2]/(p4[2]-p1[2])
                                p1 = (p1[0]*a+p4[0]*(1-a),
                                             p1[1]*a+p4[1]*(1-a),
                                             p1[2]*a+p4[2]*(1-a),
                                             p1[3]*a+p4[3]*(1-a))
                                a=1+p3[2]/(p4[2]-p3[2])
                                p3 = (p3[0]*a+p4[0]*(1-a),
                                             p3[1]*a+p4[1]*(1-a),
                                             p3[2]*a+p4[2]*(1-a),
                                             p3[3]*a+p4[3]*(1-a))
                                p2 = p3

                    p1 = ((p1[0]/p1[3]+1)*screen_w/2,(p1[1]/p1[3]+1)*screen_h/2)
                    p2 = ((p2[0]/p2[3]+1)*screen_w/2,(p2[1]/p2[3]+1)*screen_h/2)
                    p3 = ((p3[0]/p3[3]+1)*screen_w/2,(p3[1]/p3[3]+1)*screen_h/2)
                    p4 = ((p4[0]/p4[3]+1)*screen_w/2,(p4[1]/p4[3]+1)*screen_h/2)
                    tcl_code.append(f"{canvas} coords {lenght} {p1[0]} {p1[1]} {p2[0]} {p2[1]} "
                                    f"{p3[0]} {p3[1]} {p4[0]} {p4[1]}\n"
                                    f"{canvas} itemconfigure {lenght} -fill #{quad_data[12]:02x}{quad_data[13]:02x}{quad_data[14]:002x}\n")

                elif clip_count == 1: # In this case we need more polygons to represent this polygon
                    if c1:   #c1 self.log("Z clip #1","COLORBG")
                        a1=1+p1[2]/(p2[2]-p1[2])
                        a2=1+p1[2]/(p4[2]-p1[2])
                        pos=p1
                        p1 = (pos[0]*a1+p2[0]*(1-a1),
                                     pos[1]*a1+p2[1]*(1-a1),
                                     pos[2]*a1+p2[2]*(1-a1),
                                     pos[3]*a1+p2[3]*(1-a1))
                        p5 = (pos[0]*a2+p4[0]*(1-a2),
                                     pos[1]*a2+p4[1]*(1-a2),
                                     pos[2]*a2+p4[2]*(1-a2),
                                     pos[3]*a2+p4[3]*(1-a2))
                        p6 = p3
                        p7 = p4
                        p8 = p4
                        p4 = p5  # move this last, as other depend on this val
                    elif c2: #c2 self.log("Z clip #2","COLORBG")
                        a1=1+p2[2]/(p3[2]-p2[2])
                        a2=1+p2[2]/(p1[2]-p2[2])
                        pos=p2
                        p2 = (pos[0]*a1+p3[0]*(1-a1),
                                     pos[1]*a1+p3[1]*(1-a1),
                                     pos[2]*a1+p3[2]*(1-a1),
                                     pos[3]*a1+p3[3]*(1-a1))
                        p5 = (pos[0]*a2+p1[0]*(1-a2),
                                     pos[1]*a2+p1[1]*(1-a2),
                                     pos[2]*a2+p1[2]*(1-a2),
                                     pos[3]*a2+p1[3]*(1-a2))
                        p6 = p4
                        p7 = p1
                        p8 = p1
                        p1 = p5  # move this last, as other depend on this val
                    elif c3: #c3 self.log("Z clip #3","COLORBG")
                        a1=1+p3[2]/(p4[2]-p3[2])
                        a2=1+p3[2]/(p2[2]-p3[2])
                        pos=p3
                        p3 = (pos[0]*a1+p4[0]*(1-a1),
                                     pos[1]*a1+p4[1]*(1-a1),
                                     pos[2]*a1+p4[2]*(1-a1),
                                     pos[3]*a1+p4[3]*(1-a1))
                        p5 = (pos[0]*a2+p2[0]*(1-a2),
                                     pos[1]*a2+p2[1]*(1-a2),
                                     pos[2]*a2+p2[2]*(1-a2),
                                     pos[3]*a2+p2[3]*(1-a2))
                        p6 = p1
                        p7 = p2
                        p8 = p2
                        p2 = p5 # move this last, as other depend on this val
                    else:    #c4 self.log("Z clip #4","COLORBG")
                        a1=1+p4[2]/(p1[2]-p4[2])
                        a2=1+p4[2]/(p3[2]-p4[2])
                        pos=p4
                        p4 = (pos[0]*a1+p1[0]*(1-a1),
                                     pos[1]*a1+p1[1]*(1-a1),
                                     pos[2]*a1+p1[2]*(1-a1),
                                     pos[3]*a1+p1[3]*(1-a1))
                        p5 = (pos[0]*a2+p3[0]*(1-a2),
                                     pos[1]*a2+p3[1]*(1-a2),
                                     pos[2]*a2+p3[2]*(1-a2),
                                     pos[3]*a2+p3[3]*(1-a2))
                        p6 = p2
                        p7 = p3
                        p8 = p3
                        p3 = p5  # move this last, as other depend on this val

                    p1 = ((p1[0]/p1[3]+1)*screen_w/2,(p1[1]/p1[3]+1)*screen_h/2)
                    p2 = ((p2[0]/p2[3]+1)*screen_w/2,(p2[1]/p2[3]+1)*screen_h/2)
                    p3 = ((p3[0]/p3[3]+1)*screen_w/2,(p3[1]/p3[3]+1)*screen_h/2)
                    p4 = ((p4[0]/p4[3]+1)*screen_w/2,(p4[1]/p4[3]+1)*screen_h/2)
                    p5 = ((p5[0]/p5[3]+1)*screen_w/2,(p5[1]/p5[3]+1)*screen_h/2)
                    p6 = ((p6[0]/p6[3]+1)*screen_w/2,(p6[1]/p6[3]+1)*screen_h/2)
                    p7 = ((p7[0]/p7[3]+1)*screen_w/2,(p7[1]/p7[3]+1)*screen_h/2)
                    p8 = ((p8[0]/p8[3]+1)*screen_w/2,(p8[1]/p8[3]+1)*screen_h/2)
                    tcl_code.append(f"{canvas} coords {lenght} {p1[0]} {p1[1]} {p2[0]} {p2[1]} "
                                    f"{p3[0]} {p3[1]} {p4[0]} {p4[1]}\n"
                                    f"{canvas} itemconfigure ¤ -fill #{quad_data[12]:02x}{quad_data[13]:02x}{quad_data[14]:002x}\n")
                    tcl_code.append(f"{canvas} coords {lenght} {p5[0]} {p5[1]} {p6[0]} {p6[1]} "
                                    f"{p7[0]} {p7[1]} {p8[0]} {p8[1]}\n"
                                    f"{canvas} itemconfigure {lenght} -fill #{quad_data[12]:02x}{quad_data[13]:02x}{quad_data[14]:002x}\n")
            # TODO: make this whole section shorter without functions, as they have proven themselves too slow
            # endregion append geom

            if lenght == 0:
                if self.msg_del % 100 == 0:
                    self.log(f"Polygons on screen exceed polygon pool of {POLYGON_COUNT}"
                             , "YELLOW","ITALIC")
                self.msg_del += 1
                break
            lenght-=1
            #endregion


        #endregion

        for i in range(0, POLYGON_COUNT-len(tcl_code)):
            tcl_code.append(f"{canvas} coords {i} 0 0 0 0 0 0 0 0\n")

        return GameToTK().draw_code("".join(tcl_code))