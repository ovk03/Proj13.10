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
    polygons=[]

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.canvas = tkinter.Canvas(self.root,height=self.height,width=self.width)
        self.canvas.pack()

        self.polygons=[self.canvas.create_polygon(0,0, 0,0, 0,0, 0,0) for i in range(10000)]
        pass

    # region Dep
    # deprecated
    def rel_to_pix(self,tri):
        """deprecated due to performance"""
        w=self.width
        h=self.height
        # print(w,h)
        # print(tri.vert1)
        # print(tri.vert2)
        # print(tri.vert3)

        # print(rel_tri.vert1)
        # print()
        return (((tri[0][0]+ 1) * w / 2,
                    (tri[0][1] + 1) * h / 2),
                ((tri[1][0] + 1) * w / 2,
                    (tri[1][1] + 1) * h / 2),
                ((tri[2][0] + 1) * w / 2,
                    (tri[2][1] + 1) * h / 2))

    # deprecated
    def flip_y_pack(self,tris):
        """deprecated due to performance"""
        return (tris[0][0],self.height-tris[0][1],
                tris[1][0],self.height-tris[1][1],
                tris[2][0],self.height-tris[2][1])
    # endregion

    def get_width_and_height(self):
        return (self.width,self.height)


    def draw(self, new_buffer: list):
        """ draw next frame

        :param new_buffer: 3d things to draw to screen
        :type new_buffer: DrawBuffer
        """

        # TODO: this is terrible for performance reusing polygons is a necessary improvement for realtime rendering
        # TODO: just deleting everything will do for getting the engine to run for the first time

        try:
            self.root.winfo_exists()
        except Exception:
            return False
        if(len(new_buffer)==0):
            print("no triangles in buffer")

        # method 1
        for tri_and_poly in zip(new_buffer, self.polygons):
            self.canvas.coords(tri_and_poly[1],tri_and_poly[0])

        # method 2
        # self.canvas.delete("all")
        # for tri in new_buffer:
        #     self.canvas.create_polygon(tri)

        self.root.update()
        return True


