"""[insert short description here]"""
"""Onni Kolkka 
150832953 (student number)
created 14.12.2022 0.14
"""

from .game_engine import *
from .__init__ import is_windows

# simple function to define if audio and mouse control is available
# is_windows lambda:True if platform().lower().__contains__("windows")else False
def is_windows():return True if platform().lower().__contains__("windows")else False