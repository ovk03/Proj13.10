"""manages interactions with tkinter"""
import tkinter

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.06
"""

from .structures import *


class Interpeter:

    buffer = None
    root = None
    is_running = True
    width=1920
    height=1080

    def __init__(self):
        self.root = Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.buffer = DrawBuffer()
        self.canvas = tkinter.Canvas()
        pass

    def rel_to_pix(self,tri):
        w=self.width
        h=self.height
        # print(w,h)
        # print(tri.vert1)
        # print(tri.vert2)
        # print(tri.vert3)
        rel_tri=Triangle2d(
            (tri.vert1.vec2()+Vector2(1,1))*(0.5*(w+h)/2),
            (tri.vert2.vec2()+Vector2(1,1))*(0.5*(w+h)/2),
            (tri.vert3.vec2()+Vector2(1,1))*(0.5*(w+h)/2)
        )
        # print(rel_tri.vert1)
        # print()
        return rel_tri

    def flip_y_array(self,args):
        new=[]
        for number,value in enumerate(args,start=0):
            if(number%2==1):
                new.append(self.height-value)
            else:
                new.append(value)
        return new


    def draw(self, new_buffer: DrawBuffer = buffer):
        """ draw next frame

        :param new_buffer: 3d things to draw to screen
        :type new_buffer: DrawBuffer
        """

        # TODO: this is terrible for performance reusing polygons is a necessary improvement for realtime rendering
        # TODO: just deleting everything will do for getting the engine to run for the first time

        try:
            self.canvas.destroy()
        except Exception:
            return False
        self.canvas=Canvas(self.root,height=self.height,width=self.width)
        if(len(new_buffer.triangles)==0):
            print("no triangles in buffer")

        for i in range(len(new_buffer.triangles)):
            tri: Triangle2d = new_buffer.triangles[i]
            tri = self.rel_to_pix(tri)
            self.canvas.create_polygon(self.flip_y_array(tri.toArray()))
        self.canvas.pack()
        self.root.update()
        return True


