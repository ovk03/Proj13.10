"""manages interactions with tkinter"""

import tkinter
import _tkinter
import logging
import multiprocessing
import time
import ctypes
from .__main__ import EngineType

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.06
"""


# Dictionary containing the most common 16:9 resolutions, These correspond to specific files in data.
COMMON_SCREEN_RESOLUTIONS= {640:360,1600:900,1920:1080,2560:1440}

class TKMultiProcess(metaclass=EngineType):

    def __init__(self,namespace,events,size):

        # parse args
        self.namespace = namespace
        self.render_event, self.waiting_event, self.stop_event = events
        self.width, self.height = size

        # local vars
        self._cursor_lock = False
        self._fullscreen = False
        self._last_cursor_x = 0
        self._last_cursor_y = 0
        self._avrg_time = 0.02

        # config root
        self.root = tkinter.Tk()
        self.root.configure(bg="#000000")
        self.root.title("3dEngine à la noob")
        self.root.resizable(False,False)
        self.root.geometry(f"{int(self.width)}x{int(self.height)}")
        self.root.geometry(f"+{int((self.root.winfo_screenwidth()-self.root.winfo_width())/4)}"
                           f"+{int((self.root.winfo_screenheight()-self.root.winfo_height())/4)}")

        # config element pool. This way were not recreating widgets ever
        # also this pooling approach makes the FPS consistent, as there is the same amount of work each update
        self.canvas = tkinter.Canvas(self.root,height=self.height+4,width=self.width+4,highlightbackground="#000000")
        self.polygons = tuple([self.canvas.create_polygon(0,0, 0,0, 0,0, 0,0,) for i in range(4096)])

        # TODO: remove tests
        self.set_debug_res()

        # default bindings
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
        self.root.bind('<Escape>',self.toggle_cursor)
        self.root.bind('<F11>',self.toggle_fullscreen)

        # enter the "mainloop"
        logging.getLogger("Internals").debug("Entering mainloop")
        self.buffer_event()
        logging.getLogger("Internals").debug("Exiting mainloop")

        # self.root.mainloop()

    def buffer_event(self,*_):
        self.t = -time.perf_counter()
        while not self.stop_event.is_set():

            # guard clause for closing game
            if self.stop_event.is_set(): break

            self.namespace.mouse_pos_x += self.root.winfo_pointerx()-self._last_cursor_x
            self.namespace.mouse_pos_y += self.root.winfo_pointery()-self._last_cursor_y
            if self._cursor_lock and self.is_windows:
                ctypes.windll.user32.SetCursorPos(int( self.width / 2+self.root.winfo_x()), int(self.height / 2+self.root.winfo_y()))
            self._last_cursor_x = self.root.winfo_pointerx()
            self._last_cursor_y = self.root.winfo_pointery()

            if self.namespace.exec_command != "":
                # exec(self.namespace.exec_command)
                pass
            if self.render_event.is_set():
                code=self.namespace.code
                if len(code) > 0:
                    try:
                        self.root.eval(code)
                    except Exception as e:
                        logging.getLogger("Internals").debug(len(code))
                        logging.getLogger("Internals").exception(e)
                        continue
                self.render_event.clear()
                self.waiting_event.set()
                self.root.dooneevent(_tkinter.ALL_EVENTS)

                self._avrg_time = (self.t + time.perf_counter()) * (1 - .9) + self._avrg_time * .9
                print(1 / self._avrg_time)
                self.t = -time.perf_counter()

    # the ",*_" is for binding inputs to TK. Otherwise, excepted args don't match.
    # This doesn't need the extra args, so it'll just discard them
    def toggle_cursor(self,*_):
        self._cursor_lock = not self._cursor_lock
        if self._cursor_lock:
            self.root.config(cursor="none")
            self.toggle_bar_off()
        else:
            self.root.config(cursor="")
            self.toggle_bar_on()

    # the ",*_" is for binding inputs to TK. Otherwise, the excepted args might not match.
    # This doesn't need the extra args, so it'll just discard them
    def toggle_fullscreen(self, *_):
        self._fullscreen = not self._fullscreen
        if self._fullscreen:
            self.toggle_bar_on()
            self.root.attributes("-fullscreen",True)
            self._realign_elems(self.root.winfo_screenwidth(),self.root.winfo_screenheight())
        else:
            if(self._cursor_lock):
                self.toggle_bar_off()
            self.root.attributes("-fullscreen",False)
            self._realign_elems(self.root.winfo_width(),self.root.winfo_height())

    # the ",*_" is for binding inputs to TK. Otherwise, the excepted args might not match.
    # This doesn't need the extra args, so it'll just discard them
    def toggle_bar_on(self, *_):
        """toggles top bar of tk while not in fullscreen"""
        self.root.overrideredirect(False)

    # the ",*_" is for binding inputs to TK. Otherwise, the excepted args might not match.
    # This doesn't need the extra args, so it'll just discard them
    def toggle_bar_off(self, *_):
        """toggles top bar of tk while not in fullscreen"""
        self.root.overrideredirect(True)

    # the ",*_" is for binding inputs to TK. Otherwise, the excepted args might not match.
    # This doesn't need the extra args, so it'll just discard them
    def set_best_res(self,res=None):
        """Picks best resolution. Set res to max wanted res"""
        res = res or self.root.winfo_screenwidth()
        if COMMON_SCREEN_RESOLUTIONS.__contains__(res):

            # sets size and syncs changes to rendering
            self.root.geometry(F"{res}x{COMMON_SCREEN_RESOLUTIONS[res]}")

            if res==self.root.winfo_screenwidth():
                self._fullscreen = True
                self.root.attributes("-fullscreen",True)
                self._realign_elems(self.root.winfo_screenwidth(),self.root.winfo_screenheight())
            else:
                self._fullscreen = False
                self.root.attributes("-fullscreen",False)
                self._realign_elems(res,COMMON_SCREEN_RESOLUTIONS[res])
        else:
            # goes through the resolutions and selects the biggest, that won't go over screen
            current_best=640
            for key in COMMON_SCREEN_RESOLUTIONS.keys():
                if key < res and key> (current_best or 0):
                    current_best = key

            # sets size and syncs changes to rendering
            self.root.geometry(F"{current_best}x{COMMON_SCREEN_RESOLUTIONS[current_best]}")
            self._fullscreen = False
            self.root.attributes("-fullscreen",False)
            self._realign_elems(current_best,COMMON_SCREEN_RESOLUTIONS[current_best])


    def set_debug_res(self,res=None):
        self.set_best_res(self.root.winfo_screenwidth()-1)

    def _realign_elems(self,width,height):
        self.canvas.config(width=self.root.winfo_width()+4,height=self.root.winfo_height()+4)
        self.namespace.width = self.root.winfo_width()+4
        self.namespace.height = self.root.winfo_height()+4

        # TODO: better way to hide edges of the canvas
        self.canvas.place(x=int((width - self.root.winfo_width())/4)-2,
                          y=int((height- self.root.winfo_height())/4)-2)
        self.root.focus()


    # the ",*_" is for binding inputs to TK. Otherwise, the excepted args might not match.
    # This doesn't need the extra args, so it'll just discard them
    def destroy(self, *_):
        self.stop_event.set()
        self.root.destroy()

class GameToTK(metaclass=EngineType):

    width=2560/2
    height=1440/2
    polygons=[]

    def __init__(self):
        self.stop_event = multiprocessing.Event()
        self.render_event = multiprocessing.Event()
        self.waiting_event = multiprocessing.Event()
        self.manager = multiprocessing.Manager()
        self.namespace = self.manager.Namespace()
        self.namespace.code = ""
        self.namespace.input_buffer = self.manager.Queue()
        self.namespace.mouse_pos_x = 0
        self.namespace.mouse_pos_y = 0
        self.namespace.width = 0
        self.namespace.height = 0
        # FIXME: python exec function is pretty terrible way to implement
        #        propably should use specific event for each function
        self.namespace.exec_command = ""

        self.waiting_event.set()

        multiprocessing.Process(target=TKMultiProcess, daemon=True,
                                args=(self.namespace, (self.render_event, self.waiting_event, self.stop_event),
                                      (self.width, self.height))).start()



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

    def get_data_for_rend(self)->tuple:
        """returns everything needed from TCL to render triangles to TCL code"""
        # FIXME: remove hardcoded canvas name
        return (self.namespace.width, self.namespace.height, ".!canvas")


    def draw_code(self, code: str):
        """ draw next frame

        :param code: 3d things to draw to screen
        """
        if self.stop_event.is_set():
            return False

        # try:
        #     if code[0:4] == "None":
        #         # TODO: figure out why removing this makes the WHOOLE thing not work
        #         # TODO: I cant even replace it with another check
        #
        #         # FIXME: never figured out what caused "self.root.winfo_exists()" to magically fix my project
        #                  getting a random readonly boolean shouldn't have any affect TK screen not appearing
        #         print(self.root.winfo_exists())
        # except Exception: pass

        self.waiting_event.wait(2)
        if code[0:4] != "None":
            self.namespace.code = code

        self.waiting_event.clear()
        self.render_event.set()
        return True
