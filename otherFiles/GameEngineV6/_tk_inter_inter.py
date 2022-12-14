"""manages interactions with tkinter"""


"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.06
"""

from .structures import *
import tkinter

class Interpeter:

    buffer = None
    root = None
    is_running = True
    width=1920
    height=1080

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.canvas = tkinter.Canvas()
        pass

    def rel_to_pix(self,tri):
        w=self.width
        h=self.height
        # print(w,h)
        # print(tri.vert1)
        # print(tri.vert2)
        # print(tri.vert3)
        rel_tri=[
            [(tri[0][0]+ 1) * w / 2,
                    (tri[0][1] + 1) * h / 2],
            [(tri[1][0] + 1) * w / 2,
                    (tri[1][1] + 1) * h / 2],
            [(tri[2][0] + 1) * w / 2,
                    (tri[2][1] + 1) * h / 2]]

        # print(rel_tri.vert1)
        # print()
        return rel_tri

    def flip_y_array(self,tris):
        new=[]
        for i in tris:

            new.extend([i[0],self.height-i[1]])
        return new


    def draw(self, new_buffer: list):
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
        self.canvas=tkinter.Canvas(self.root,height=self.height,width=self.width)
        if(len(new_buffer)==0):
            print("no triangles in buffer")

        for i in range(0,len(new_buffer),3):
            tri = new_buffer[i:i+3]
            tri = self.rel_to_pix(tri)
            self.canvas.create_polygon(self.flip_y_array(tri))
        self.canvas.pack()
        self.root.update()
        return True


