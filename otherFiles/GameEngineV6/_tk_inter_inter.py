"""manages interactions with tkinter"""
import pathlib
import tkinter
import _tkinter
import logging
import multiprocessing
import time
import ctypes
from .__main__ import *

"""Onni Kolkka 
150832953 (student number)
created 10.12.2022 15.06
"""


class TKMultiProcess(metaclass=EngineTypeSingleton):

    def __init__(self,namespace,events,size):

        # parse args
        self.namespace = namespace
        self.render_event, self.waiting_event, self.stop_event, self.command_event = events
        self.width, self.height = size
        self.control_mouse_out_of_focus = False

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

        # config element pool. This way were not recreating widgets ever
        # also this pooling approach makes the FPS consistent, as there is the same amount of work each update
        self.canvas = tkinter.Canvas(self.root,height=self.height+4,width=self.width+4,highlightbackground="#000000")
        self.polygons = tuple([self.canvas.create_polygon(0,0, 0,0, 0,0, 0,0,) for i in range(POLYGON_COUNT)])

        # TODO: remove test label
        self.canvas.create_text(100,100,text="TEST")
        print(pathlib.Path(__file__).parent.joinpath("Untitled.png"))
        photo = tkinter.PhotoImage(file=pathlib.Path(__file__).parent.joinpath("Untitled.png"))
        self.canvas.create_image(100,100,image=photo)

        # set correct resolution
        if(self.debug):
            self.set_debug_res()
        else:
            self.set_best_res()

        # default bindings
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
        self.root.bind('<Escape>',self.toggle_cursor)
        self.root.bind('<F11>',self.toggle_fullscreen)

        # enter the "mainloop"
        self.log("Entering Mainloop()","GREEN","UNDERLINE")
        self.main_loop()
        self.log("Extiting Mainloop()","GREEN","UNDERLINE")

        # self.root.mainloop()

    def _should_lock_mouse(self):
        return self._cursor_lock \
           and self.is_windows \
           and self.root.winfo_exists() \
           and self.root.focus_displayof() is not None

    def main_loop(self, *_):
        self.t = -time.perf_counter()

        i=0
        # checks if should stop updating TK
        while not self.stop_event.is_set() and self.root.winfo_exists():
            # calculates mouse input
            if self._should_lock_mouse():
                self.namespace.mouse_pos_x += self.root.winfo_pointerx()-self._last_cursor_x
                self.namespace.mouse_pos_y += self.root.winfo_pointery()-self._last_cursor_y

                ctypes.windll.user32.SetCursorPos(int( self.width / 2+self.root.winfo_x()),
                                                  int(self.height / 2+self.root.winfo_y()))

                self._last_cursor_x = self.root.winfo_pointerx()
                self._last_cursor_y = self.root.winfo_pointery()
            elif self.control_mouse_out_of_focus:
                self.namespace.mouse_pos_x += self.root.winfo_pointerx()-self._last_cursor_x
                self.namespace.mouse_pos_y += self.root.winfo_pointery()-self._last_cursor_y
                self._last_cursor_x = self.root.winfo_pointerx()
                self._last_cursor_y = self.root.winfo_pointery()

            # FIXME: maybe a security vulnerability. Should be fixed (maybe)
            if self.namespace.exec_command != "":
                self.command_event.clear()
                self.namespace.exec_command=""
                exec(self.namespace.exec_command)


            if self.render_event.is_set():
                #clear flags
                self.render_event.clear()
                self.waiting_event.set()

                # try render game data
                code=self.namespace.code
                try:
                    if len(code) > 0 and code[0:4] != "None":
                        self.canvas.delete("3d")
                        self.root.eval(code)
                except Exception as e:
                    logging.getLogger("Internals").debug(len(code))
                    logging.getLogger("Internals").exception(e)
                    self.destroy()

                # main update
                self.root.dooneevent(_tkinter.ALL_EVENTS)

                # logging framerae
                self._avrg_time = (self.t + time.perf_counter()) * (1 - .9) + self._avrg_time * .9
                i+=1
                if(i%FRAME_RATE_LOG_FREQUENCY==0):
                    self.log(f"FPS: {1 / self._avrg_time:.1f}","GREEN")
                self.t = -time.perf_counter()

    # the ",*_" is for binding inputs to TK. Otherwise, excepted args don't match. This doesn't need the extra args, so it'll just discard them
    def toggle_cursor(self,*_):
        # FIXME possible to bug tkinter out of taskbar, if called WAY too much in sort period
        self._cursor_lock = not self._cursor_lock
        if self._cursor_lock:
            self.root.config(cursor="none")
            self.toggle_bar_off()
        else:
            self.root.config(cursor="")
            self.toggle_bar_on()

    # the ",*_" is for binding inputs to TK. Otherwise, excepted args don't match. This doesn't need the extra args, so it'll just discard them
    def toggle_fullscreen(self, *_):
        # FIXME possible to bug tkinter out of taskbar, if called WAY too much in sort period
        self._fullscreen = not self._fullscreen
        if self._fullscreen:
            self.set_best_res()
            self.toggle_bar_on()
            self.root.attributes("-fullscreen", True)
        else:
            self.set_debug_res()

    def toggle_bar_on(self):
        """toggles top bar of tk while not in fullscreen"""
        self.root.overrideredirect(False)

    def toggle_bar_off(self):
        """toggles top bar of tk while not in fullscreen"""
        self.root.overrideredirect(True)

    def set_best_res(self,res=None):
        """Picks the best resolution. Set res to max wanted res"""
        res = res or self.root.winfo_screenwidth()
        if COMMON_SCREEN_RESOLUTIONS.__contains__(res):

            # sets size and syncs changes to rendering
            self.root.geometry(F"{res}x{COMMON_SCREEN_RESOLUTIONS[res]}")

            if res == self.root.winfo_screenwidth():
                self._fullscreen = True
                self.root.attributes("-fullscreen", True)
                self._realign_elements(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
            else:
                self._fullscreen = False
                self.root.attributes("-fullscreen", False)
                self._realign_elements(res, COMMON_SCREEN_RESOLUTIONS[res])
        else:
            # goes through the resolutions and selects the biggest, that won't go over screen
            current_best=640
            for key in COMMON_SCREEN_RESOLUTIONS.keys():
                if (current_best or 0) < key < res:
                    current_best = key

            # sets size and syncs changes to rendering
            self.root.geometry(F"{current_best}x{COMMON_SCREEN_RESOLUTIONS[current_best]}")
            self._fullscreen = False
            self.root.attributes("-fullscreen",False)
            self._realign_elements(current_best, COMMON_SCREEN_RESOLUTIONS[current_best])


    def set_debug_res(self,res=None):
        """sets resolution to one level lower than best res"""
        if (self._cursor_lock):
            self.toggle_bar_off()
        self.set_best_res(self.root.winfo_screenwidth()-1)

    def _realign_elements(self, width, height):
        self.root.dooneevent(0)
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
        self.is_working = False
        self.root.destroy()
        del self

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
        self.namespace.exec_command = ""

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
