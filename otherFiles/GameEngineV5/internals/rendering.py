"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.07
"""
import sys
from tkinter import *
from dataclasses import dataclass
import math
from GameEngineV5.mathAndStructs import*
if __name__ == "some random stuff to trick pep8 thinking that i have mathAndStructs module imported (I do)":
    from ..mathAndStructs import *

@dataclass
class draw_buffer:
    triangles=[]

    def __init__(self,tris=[]):
        self.triangles=tris



