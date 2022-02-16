"""Gui

This file contains the app (Tk) class, and the main method which starts the GUI and serial communication.

Running both simultaneously makes use of multithreading. A separate thread is started to run the app.
This allows for all values to be updatable.

This file is the starting point of the app. It creates the folder and files sensor readings will be stored into,
starts serial communication with the Arduino Micro, and starts the app.
It also defines all methods necessary for runtime app use.
"""

import threading
import time
import tkinter as tk
import matplotlib
from constants import *
import pages as pg
import file_handler as fh

matplotlib.use("TkAgg")


class SensorCentral(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, APP_NAME)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in [pg.StartPage, pg.TMP116Page, pg.HDC2010Page, pg.OPT3001Page, pg.DPS310Page]:
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(pg.StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def thread_gui():
    app = SensorCentral()
    app.mainloop()


if __name__ == '__main__':
    fh.folder_prep()
    serial.reset_input_buffer()
    time.sleep(2)
    threading.Thread(target=thread_gui).start()

    while True:
        fh.store_to_csv()
        time.sleep(1)
