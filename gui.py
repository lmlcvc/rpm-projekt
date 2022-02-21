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
import serial.tools.list_ports

import file_handler as fh
import pages as pg
from constants import *

matplotlib.use("TkAgg")


class SensorCentral(tk.Tk):
    """
        A class used to create the root of Tk interface.

        Attributes
        ----------
        frames : dict
            Contains all pages in app.
            key - SensorPage or StartPage (child) object
            value - instance of that page in app

        Methods
        -------
        show_frame(self, content)
            Raise the frame passed as 'content'.

        timed_update(self)
            Call StartPage's update (every 60s, as specified in main app loop).
    """

    frames = {}

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, APP_NAME)

        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for page in [pg.StartPage, pg.TMP116Page, pg.HDC2010Page, pg.OPT3001Page, pg.DPS310Page]:
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(pg.StartPage)

    def show_frame(self, content):
        frame = self.frames[content]
        frame.tkraise()

    def timed_update(self):
        pg.StartPage.update_start_data(self.frames[pg.StartPage])


def call_repeatedly(interval, func, *args):
    """ Call func(*args) every {interval} seconds. """
    stopped = threading.Event()

    def loop():
        while not stopped.wait(interval):  # the first call is in `interval` secs
            func(*args)

    threading.Thread(target=loop).start()
    return stopped.set


def thread_serial():
    """ Thread used to continuously store incoming values from serial to csv if device connected """

    while True:
        fh.store_to_csv()


if __name__ == '__main__':
    fh.folder_prep()  # prepare csv folder

    # check if port defined as SERIAL_PORT has a device connected to it
    ports = [tuple(p)[0] for p in list(serial.tools.list_ports.comports())]
    arduino_port = [port for port in ports if SERIAL_PORT in port]

    # start serial communication if connected
    if arduino_port:
        serial.reset_input_buffer()  # clear input serial buffer

        time.sleep(1)  # small delay to stabilise
        threading.Thread(target=thread_serial).start()  # start thread

    app = SensorCentral()  # start the app
    cancel_future_calls = call_repeatedly(10, app.timed_update, )  # call for repeated app update
    app.mainloop()  # enter main app loop after repeated calls instantiated

    cancel_future_calls()  # cancel future calls after window closes
