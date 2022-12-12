"""manages interactions with tkinter"""
import tkinter

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.06
"""


from tkinter import *
from dataclasses import dataclass
import math
from GameEngineV5.mathAndStructs import*
if __name__ == "some random stuff to trick pep8 thinking that i have mathAndStructs module imported (I do)":
    from ..mathAndStructs import *

from .rendering import *



class interpeter:
    buffer = draw_buffer()
    root = Tk()
    canvas = tkinter.Canvas()
    is_running = True

    def __init__(self):
        pass

    def draw(self, new_buffer: draw_buffer = buffer):
        """ draw next frame

        :param new_buffer: 3d things to draw to screen
        :type new_buffer: draw_buffer
        """

        # TODO: this is terrible for performance reusing polygons is a necessary improvement for realtime rendering
        # TODO: just deleting everything will do for getting the engine to run for the first time

        try:
            self.canvas.delete("all")
        except Exception:
            return False

        for i in range(len(new_buffer.triangles)):
            tri: Triangle2d = new_buffer.triangles[i]
            self.canvas.create_polygon(tri.toArray())
        self.canvas.pack()
        print(self.canvas.find_all())
        self.root.update()
        return True
