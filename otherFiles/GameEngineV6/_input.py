"""Simple class to read user inputs"""

import time
from ctypes import windll
from .__main__ import *
from ._game_to_tk import *


"""Onni Kolkka 
150832953 (student number)
created 18.12.2022 19.04
"""

WIN_KEY = {
    "Mouse1":0x01,
    "Mouse2":0x01,
    "Mouse3":0x02,
    "BackSpace":0x08,
    "Tab":0x09,
    "Return":0x0D,
    "Shift_L":0x10,
    "Control_L":0x11,
    "Alt_L":0x12,
    "Escape":0x1B,
    "space":0x20,
    "0":0x30,
    "1":0x31,
    "2":0x32,
    "3":0x33,
    "4":0x34,
    "5":0x35,
    "6":0x36,
    "7":0x37,
    "8":0x38,
    "9":0x39,
    "a":0x41,
    "b":0x42,
    "c":0x43,
    "d":0x44,
    "e":0x45,
    "f":0x46,
    "g":0x47,
    "h":0x48,
    "i":0x49,
    "j":0x4A,
    "k":0x4B,
    "l":0x4C,
    "m":0x4D,
    "n":0x4E,
    "o":0x4F,
    "p":0x50,
    "q":0x51,
    "r":0x52,
    "s":0x53,
    "t":0x54,
    "u":0x55,
    "v":0x56,
    "w":0x57,
    "x":0x58,
    "y":0x59,
    "z":0x5A,
    "KP_0":0x60,
    "KP_1":0x61,
    "KP_2":0x62,
    "KP_3":0x63,
    "KP_4":0x64,
    "KP_5":0x65,
    "KP_6":0x66,
    "KP_7":0x67,
    "KP_8":0x68,
    "KP_9":0x69,
    "F1":0x70,
    "F2":0x71,
    "F3":0x72,
    "F4":0x73,
    "F5":0x74,
    "F6":0x75,
    "F7":0x76,
    "F8":0x77,
    "F9":0x78,
    "F10":0x79,
    "F11":0x7A,
    "F12":0x7B}

# short classname to save space on the module users end
class Inp(metaclass=EngineTypeSingleton):
    """Centralized class containing inputs from both keyboard and mouse"""

    def __init__(self):
        self._key_list = {}
        self._change_time = {}
        self._mouse_x = 0
        self._mouse_y = 0
        pass

    def update(self):
        """tells inputs that new update tick has started"""

    # https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
    @ staticmethod
    def key_pos(key):
        """Returns int of key state (0 = off 1 = on 2= pressed now, -1 = released now)"""

        # read the keyboard
        if Inp().is_windows and not USE_TK_INPUT_ONLY:
            down = windll.user32.GetAsyncKeyState(WIN_KEY[key]) != 0
        else:
            down = GameToTK().get_key(key)

        # if key state hasn't changed since last tick, return
        # alternatively if time changed is now, we know key was releasedd
        if Inp()._key_list.get(key,False) == down and not Inp()._change_time.get(key,0)==time.time():
            Inp()._key_list[key] = down
            Inp()._change_time[key]=time.time()
            return int(down)

        # we know key was released or pressed between frames
        elif down:
            Inp()._key_list[key] = down
            return 2
        else:
            Inp()._key_list[key] = down
            return -1

    @staticmethod
    def key_up(key):
        """key was released"""
        return Inp().key_pos(key)==-1

    @staticmethod
    def key_dwn(key):
        """key was pressed"""
        return Inp().key_pos(key)==2

    @staticmethod
    def key(key):
        """key is held down"""
        return Inp().key_pos(key)>0

    @staticmethod
    def mouse_coords(*args):
        val=(0,0)
        if Inp().is_windows and not USE_TK_INPUT_ONLY:
            # TODO: implement windll based input
            Inp().log(windll.user32.GetMousePos(),"BOLD")
        else:
            val= GameToTK().get_mouse_coords()

        if len(args) == 1:
            if args[0].lower == "x": return val[0]
            elif args[0].lower == "y": return val[1]
        else: return val

    @staticmethod
    def mouse(*args):
        val=(0,0)
        if Inp().is_windows and not USE_TK_INPUT_ONLY:
            Inp().log(windll.user32.GetCursorPos(),"BOLD","YELLOW")
            # TODO: implement windll based input
            pass
        else:
            val= GameToTK().get_mouse()

        if len(args) == 1:
            if args[0].lower() == "x": return val[0]
            elif args[0].lower() == "y": return val[1]
        else: return val
