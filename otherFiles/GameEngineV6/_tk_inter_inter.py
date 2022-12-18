"""manages interactions with tkinter"""

import multiprocessing
import time

from ._tk_multiprocess import *
from .__main__ import *

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.06
"""



class GameToTK(metaclass=EngineTypeSingleton):

    width=2560/2
    height=1440/2
    polygons=[]

    def __init__(self):
        self.stop_event = multiprocessing.Event()
        self.render_event = multiprocessing.Event()
        self.waiting_event = multiprocessing.Event()
        self.command_event = multiprocessing.Event()
        self.manager = multiprocessing.Manager()
        self.namespace = self.manager.Namespace()
        self.namespace.code = ""
        self.namespace.mouse_pos_x = 0
        self.namespace.mouse_pos_y = 0
        self.namespace.width = 0
        self.namespace.height = 0

        # FIXME: python exec function is pretty terrible way to implement
        #        propably should use specific event for each function
        self.namespace.exec_command = " "

        self.waiting_event.set()

        multiprocessing.Process(target=TKMultiProcess, daemon=True,
                                args=(self.namespace, (self.render_event, self.waiting_event, self.stop_event,self.command_event),
                                      (self.width, self.height))).start()

    def get_data_for_rend(self)->tuple:
        """returns everything needed from TCL to render triangles to TCL code"""
        # FIXME: remove hardcoded canvas name
        return (self.namespace.width, self.namespace.height, ".!canvas")

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

        # try:
        #     if code[0:4] == "None":
        #         # TODO: figure out why removing this makes the WHOOLE thing not work
        #         # TODO: I cant even replace it with another check
        #
        #         # FIXME: never figured out what caused "self.root.winfo_exists()" to magically fix my project
        #                  getting a random readonly boolean shouldn't have any affect TK screen not appearing
        #         print(self.root.winfo_exists())
        # except Exception: pass
