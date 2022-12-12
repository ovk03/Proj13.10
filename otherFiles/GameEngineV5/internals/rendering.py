"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.07
"""

from tkinter import *
from dataclasses import dataclass
import math
from ..mathAndStructs import *

@dataclass
class draw_buffer:
    triangles=[]

    def __init__(self,tris=[]):
        self.triangles=tris



