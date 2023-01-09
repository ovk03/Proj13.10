"""Simple class to read user inputs"""

import ctypes.wintypes
import time
from .__main__ import *
from ._game_to_tk import *


# for mouse inputs and mouse lock
from ctypes import windll, Structure, c_ulong, byref
class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


"""Onni Kolkka 
150832953 (student number)
created 18.12.2022 19.04
"""

# short classname to save space on the module users end
class Input(metaclass=EngineTypeSingleton):
    """Centralized class containing inputs from both keyboard and mouse"""

    """=============Extrernal funcs==============="""
    # region Ext

    @ staticmethod
    def update():
        """tells inputs that new update tick has started"""
        Input()._handle_mouse_lock()

    # region keyboard
    @ staticmethod
    def key_pos(key):
        """Returns int of key state (0 = off 1 = on 2= pressed now, -1 = released now)"""

        # read the keyboard
        if Input().is_windows and not USE_TK_INPUT_ONLY:
            down = windll.user32.GetAsyncKeyState(WIN_KEY[key]) != 0
        else:
            down = GameToTK().get_key(key)

        # if key state hasn't changed since last tick, return
        # alternatively if time changed is now, we know key was releasedd
        if Input()._key_list.get(key, False) == down and not Input()._change_time.get(key, 0) == time.time():
            Input()._key_list[key] = down
            Input()._change_time[key]=time.time()
            return int(down)

        # we know key was released or pressed between frames
        elif down:
            Input()._key_list[key] = down
            return 2
        else:
            Input()._key_list[key] = down
            return -1

    @staticmethod
    def key_up(key):
        """key was released"""
        return Input().key_pos(key) == -1

    @staticmethod
    def key_dwn(key):
        """key was pressed"""
        return Input().key_pos(key) == 2

    @staticmethod
    def key(key):
        """key is held down"""
        return Input().key_pos(key) > 0

    # endregion keyboard

    # region mouse position
    @staticmethod
    def mouse_coords(*args):
        val=(0,0)
        if Input().is_windows and not USE_TK_INPUT_ONLY:
            point = POINT()
            result = windll.user32.GetCursorPos(byref(point))
            if result:
                val= (point.x, point.y)
            else:
                val= GameToTK().get_mouse_coords()
        else:
            val= GameToTK().get_mouse_coords()
        if len(args) == 1:
            if args[0].lower() == "x": return val[0]
            elif args[0].lower() == "y": return val[1]
        # else:
        return val


    @staticmethod
    def mouse(*args):
        val=(Input()._mouse_x, Input()._mouse_y)
        if len(args) == 1:
            if args[0].lower() == "x": return val[0]
            elif args[0].lower() == "y": return val[1]
        # else:
        return val

    # endregion mouse position

    # region mouse lock and visibility
    @staticmethod
    def mouse_lock(boolean):
        """sets mouse lock"""
        self=Input()
        if boolean:
            self.is_mouse_hidden = True
            self.is_mouse_locked = True
        else:
            self.is_mouse_locked = False
            self.is_mouse_hidden = False

    @staticmethod
    def mouse_lock_switch():
        """toggles mouse lock"""
        self=Input()
        if self.is_mouse_locked:
            self.is_mouse_locked = False
            self.is_mouse_hidden = False
        else:
            self.is_mouse_locked = True
            self.is_mouse_hidden = True

    @staticmethod
    def mouse_hide(boolean):
        """sets mouse visibility (and mouse lock)"""
        self=Input()
        if boolean:
            self.is_mouse_hidden = True
        else:
            self.is_mouse_hidden = False

    @staticmethod
    def mouse_hide_switch():
        """toggles mouse visibility (and mouse lock)"""
        self=Input()
        if self.is_mouse_hidden:
            self.is_mouse_hidden = False
        else:
            self.is_mouse_hidden = True

    # endregion mouse lock and visibility

    # endregion Ext

    """=============Internal funcs============="""
    def __init__(self):
        self._key_list = {}
        self._change_time = {}
        self._mouse_x = 0
        self._mouse_y = 0
        self._last_mouse_x = 0
        self._last_mouse_y = 0
        self.is_mouse_hidden = False
        self.is_mouse_locked = False
        pass

    def _handle_mouse_lock(self):
        # todo: this
        if not USE_TK_INPUT_ONLY and self.is_windows and self.is_mouse_locked:

            self._mouse_x = self.mouse_coords('X') - self._last_mouse_x
            self._mouse_y = self.mouse_coords('Y') - self._last_mouse_y

            w,h,x,y=GameToTK.get_screen_data()

            ctypes.windll.user32.SetCursorPos(int(w/2+x),
                                              int(h/2+y))

            self._last_mouse_x, self._last_mouse_y = self.mouse_coords()
        else:
            self._mouse_x = 0
            self._mouse_y = 0
            self._last_mouse_x, self._last_mouse_y = self.mouse_coords()

# https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
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
