"""Runs tk itself in a dedicated core
This way global interpreter lock won't slow it down
unlike if it was only multi threaded"""

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
created 18.12.2022 2.53
"""


class TKMultiProcess(metaclass=EngineTypeSingleton):

    def init_variables(self, namespace, events, size):
        # parse args
        self.namespace = namespace
        self.render_event, self.waiting_event, self.stop_event, \
        self.command_event, self.key_event = events
        self.width, self.height = size
        self.control_mouse_out_of_focus = False

        # local vars
        self._cursor_lock = False
        self._fullscreen = False
        self._last_cursor_x = 0
        self._last_cursor_y = 0
        self._avrg_time = 0.02
        self._last_cursor_x = 0
        self._last_cursor_y = 0
        self.canvas_width=0
        self.canvas_height=0
        self._key_list = {}

    def init_TK(self):
        # config root
        self.root = tkinter.Tk()
        self.root.configure(bg="#000000")
        self.root.title("3dEngine à la noob")
        # self.root.resizable(False, False)
        self.canvas = tkinter.Canvas(self.root, highlightbackground="#000000")
        p = [self.canvas.create_polygon(0,0,0,0,0,0,0,0) for i in range(POLYGON_COUNT)]
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)


        # TODO: remove test label
        self.canvas.create_text(100, 100, text="TEST")
        photo = tkinter.PhotoImage(file=pathlib.Path(__file__).parent.joinpath("Untitled.png"))
        self.canvas.create_image(100, 100, image=photo)


        # default bindings


        self.root.bind('<Escape>',self.toggle_cursor)
        self.root.bind('<F11>',self.toggle_fullscreen)
        if not self.is_windows or USE_TK_INPUT_ONLY:
            # TODO: TKinter will spam these functions until the game will freeze. This is a big disadvantage for non windows
            self.root.bind('<KeyPress>',self.reg_key_down)
            self.root.bind('<ButtonPress-1>',self.reg_button_down)
            self.root.bind('<ButtonPress-2>',self.reg_button_down)
            self.root.bind('<ButtonPress-3>',self.reg_button_down)
            self.root.bind('<KeyRelease>',self.reg_key_up)
            self.root.bind('<ButtonRelease-1>',self.reg_button_up)
            self.root.bind('<ButtonRelease-2>',self.reg_button_up)
            self.root.bind('<ButtonRelease-3>',self.reg_button_up)

        # set correct resolution
        if self.is_debug:
            self.set_debug_res()
        else:
            self.set_best_res()
        self.root.update()
        self.root.overrideredirect(True)

    def __init__(self,*args):

        self.init_variables(*args)
        self.init_TK()

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
        for i in range(20):
            self.root.dooneevent(_tkinter.WINDOW_EVENTS)
        i=0
        tot_time=0
        proc_time=0
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

            elif self.control_mouse_out_of_focus or not self.is_windows:
                self.namespace.mouse_pos_x += self.root.winfo_pointerx()-self._last_cursor_x
                self.namespace.mouse_pos_y += self.root.winfo_pointery()-self._last_cursor_y
                self._last_cursor_x = self.root.winfo_pointerx()
                self._last_cursor_y = self.root.winfo_pointery()

            # FIXME: maybe a security vulnerability. Should be fixed (maybe)
            if self.command_event.is_set():
                if self.namespace.exec_command.strip() == "":
                    continue
                self.log(self.namespace.exec_command,"YELLOW","COLORBG")
                self.link()
                self.command_event.clear()
                self.namespace.exec_command=""
                exec(self.namespace.exec_command)


            if self.render_event.is_set():
                #clear flags
                proc_time-=time.perf_counter()
                self.render_event.clear()
                self.waiting_event.set()

                # self.canvas.delete("3d")

                # try render game data
                code=self.namespace.code
                if len(code) > 0 and code[0:4] != "None":
                    try:
                         self.root.eval(code)
                    except Exception as e:
                        self.log(len(code),"RED","COLORBG")
                        self.link()
                        logging.getLogger().exception(e)
                        self.destroy()

                # self.root.dooneevent(0)
                self.root.update()

                # logging framerae
                self._avrg_time = (self.t + time.perf_counter()) * (1 - .9) + self._avrg_time * .9
                tot_time+=self.t + time.perf_counter()
                i+=1
                proc_time += time.perf_counter()
                if(i%FRAME_RATE_LOG_FREQUENCY==0):
                    self.log(f"FPS: {1 / self._avrg_time:.1f}","GREEN")
                self.t = -time.perf_counter()
        self.log(f"time rendering: {proc_time:.3f}. time total: {tot_time:.3f}","CYAN")

    # the ",*_" is for discarding unwanted args.
    def destroy(self, *_):
        self.stop_event.set()
        self.is_working = False
        self.root.destroy()
        del self

    # region input

    def reg_key_up(self, args):
        if len(args.keysym) == 1:
            key = args.keysym.lower()
        else:
            key = args.keysym
        self._key_list[key] = False
        self.namespace.key_list = self._key_list
        self.key_event.set()

    def reg_key_down(self, args):
        if len(args.keysym) == 1:
            key = args.keysym.lower()
        else:
            key = args.keysym
        if self._key_list.get(key, False):
            return
        self._key_list[key] = True
        self.namespace.key_list = self._key_list
        self.key_event.set()

    def reg_button_up(self, args):
        key = "Mouse"+str(args.num)
        self._key_list[key] = False
        self.namespace.key_list = self._key_list
        self.key_event.set()

    def reg_button_down(self, args):
        key = "Mouse"+str(args.num)
        if self._key_list.get(key, False):
            return
        self._key_list[key] = True
        self.namespace.key_list = self._key_list
        self.key_event.set()

    # endregion

    # *_ discards args
    def toggle_cursor(self,*_):
        self._cursor_lock = not self._cursor_lock
        if self._cursor_lock:
            self.root.config(cursor="none")
            # self.toggle_bar_off()
        else:
            self.root.config(cursor="")
            # self.toggle_bar_on()

    def update_fullscreen(self):
        if self._fullscreen:
            self.root.overrideredirect(False)
            self.root.attributes("-fullscreen", True)
            self.root.overrideredirect(True)
        else:
            self.root.overrideredirect(False)
            self.root.attributes("-fullscreen", False)
            self.root.overrideredirect(True)
        self._realign_elements()

    # *_ discards args
    def toggle_fullscreen(self,*_):
        self._fullscreen = not self._fullscreen
        self.update_fullscreen()

    def set_best_res(self,res=None):
        """Picks the best resolution. Set res to max wanted res"""
        res = res or self.root.winfo_screenwidth()
        if COMMON_SCREEN_RESOLUTIONS.__contains__(res):

            # sets size and syncs changes to rendering
            self.root.geometry(F"{res}x{COMMON_SCREEN_RESOLUTIONS[res]}")
            self.canvas_width=res
            self.canvas_height=COMMON_SCREEN_RESOLUTIONS[res]

            if res == self.root.winfo_screenwidth():
                self._fullscreen=  True
                self.update_fullscreen()
                self._realign_elements()
            else:
                self._fullscreen = False
                self.update_fullscreen()
                self._realign_elements()
            self.canvas.configure(width=self.canvas_width,height=self.canvas_height)
        else:
            # goes through the resolutions and selects the biggest, that won't go over screen
            current_best=640
            for key in COMMON_SCREEN_RESOLUTIONS.keys():
                if (current_best or 0) < key < res:
                    current_best = key

            # sets size and syncs changes to rendering
            self.root.geometry(F"{current_best}x{COMMON_SCREEN_RESOLUTIONS[current_best]}")
            self.canvas_width=current_best
            self.canvas_height=COMMON_SCREEN_RESOLUTIONS[current_best]
            self._fullscreen = False
            self.update_fullscreen()
            self.canvas.configure(width=self.canvas_width,height=self.canvas_height)
            self._realign_elements()


    def set_debug_res(self):
        """sets resolution to one level lower than best res"""
        self.set_best_res(self.root.winfo_screenwidth()-1)

    def _realign_elements(self):
        self.canvas.config(width=self.root.winfo_width()+4,height=self.root.winfo_height()+4)

        self.namespace.width = self.root.winfo_width()
        self.namespace.height = self.root.winfo_height()
        self.namespace.offset_width = int((self.root.winfo_screenwidth() -self.root.winfo_width())/ 2)
        self.namespace.offset_height= int((self.root.winfo_screenheight()-self.root.winfo_height())/2)

        self.root.geometry(f"+{int((self.root.winfo_width()-self.root.winfo_screenwidth())/ 4)}"
                           f"+{int((self.root.winfo_height()-self.root.winfo_screenheight())/4)}")
        self.log(self.root.geometry)
        self.canvas.place(x=int(self.canvas.winfo_width()-self.root.winfo_width())/2,
                          y=int(self.canvas.winfo_height()-self.root.winfo_height())/2)
        self.canvas.configure(width=self.canvas_width, height=self.canvas_height)
        # TODO: better way to hide edges of the canvas
