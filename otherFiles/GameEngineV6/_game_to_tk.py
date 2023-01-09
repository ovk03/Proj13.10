"""Manages interactions with tkinter"""

from ._tk_multiprocess import *
from .__main__ import *

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.06
"""


class GameToTK(metaclass=EngineTypeSingleton):
    """Manager between tk and rest of the module"""

    """=============Extrernal funcs==============="""
    # region Ext
    @ staticmethod
    def start():
        self=GameToTK()
        multiprocessing.Process(target=TKMultiProcess, daemon=True,
                                args=(self.namespace,
                                     # events
                                     (self.render_event, self.waiting_event, self.stop_event,
                                      self.command_event, self.key_event, self.set_res_event,
                                      self.set_fullscreen_event, self.set_override_event),
                                     # configs
                                     (self.width, self.height))).start()

    @ staticmethod
    def get_screen_data()->tuple:
        """returns everything needed from TCL to module

        returns a tuple containing:
        [0] width of the window
        [1] height of the window
        [2] x coord of top left corner
        [3] y coord of top left corner"""
        self=GameToTK()
        # FIXME: remove hardcoded canvas name
        self.log("Removew namespace ref","RED","UNDERLINE")
        return (self.namespace.canv_width, self.namespace.canv_height,
                self.namespace.offset_width, self.namespace.offset_height)

    def set_res(self,width):
        self.set_res_event.set()
        pass

    def set_fullscreen(self,boolean):
        self.set_fullscreen_event.set()
        pass

    def set_override(self,boolean):
        self.set_override_event.set()
        pass

    def get_key(self,keycode):
        if self.key_event.is_set():
            self._key_list = self.namespace.key_list
            self.key_event.clear()
        return self._key_list.get(keycode,False)

    def get_mouse(self):
        """used for mouse position while mouse is locked"""
        return (self.namespace.mouse_pos_y,self.namespace.mouse_pos_x)

    def get_mouse_coords(self):
        """used for mouse position on screeen space"""
        return (self.namespace.mouse_coords_y,self.namespace.mouse_coords_x)

    def draw_code(self, code: str):
        """ draw next frame """
        # guard clause

        if self.stop_event.is_set():
            self.is_working = False
            self.log("Draw failed. Window was probably closed","YELLOW")
            del self
            return False

        self.waiting_event.wait(2)
        self.namespace.code = code
        self.waiting_event.clear()
        self.render_event.set()
        return True
    # endregion Ext


    """=============Internal funcs============="""
    def __init__(self):

        self.width = 2560
        self.height = 1440
        self.polygons = []

        self.stop_event = multiprocessing.Event()
        self.render_event = multiprocessing.Event()
        self.waiting_event = multiprocessing.Event()
        self.command_event = multiprocessing.Event()
        self.key_event = multiprocessing.Event()
        self.set_res_event = multiprocessing.Event()
        self.set_fullscreen_event = multiprocessing.Event()
        self.set_override_event = multiprocessing.Event()

        self.manager = multiprocessing.Manager()
        self.namespace = self.manager.Namespace()

        self.namespace.mouse_pos_x = 0
        self.namespace.mouse_pos_y = 0
        self.namespace.mouse_coords_x = 0
        self.namespace.mouse_coords_y = 0
        self.namespace.canv_width = 0
        self._canv_width = 0
        self.namespace.canv_height = 0
        self._canv_height = 0
        self.namespace.offset_width = 0
        self._offset_width = 0
        self.namespace.offset_height = 0
        self._offset_height = 0

        self.namespace.key_list = {}
        self.namespace.code = ""

        self._key_list = {}

        # FIXME: python exec function is pretty terrible way to implement
        #        propably should use specific event for each function
        self.namespace.exec_command = " "

        self.waiting_event.set()

    def _check_namespace(self):
        self._canv_width = self.namespace.canv_width
        self._canv_height = self.namespace.canv_height
        self._offset_width = self.namespace.offset_width
        self._offset_height = self.namespace.offset_height