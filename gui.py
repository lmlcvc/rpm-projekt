"""Gui

This file contains methods used in app, and the main method which starts the GUI and serial communication.

Running both simultaneously makes use of multithreading. A separate thread is started to run the app.
This allows for all values to be updatable.

This file is the starting point of the app. It creates the folder and files sensor readings will be stored into,
starts serial communication with the Arduino Micro, and starts the app.
It also defines all methods necessary for runtime app use.

This file can also be imported as a module and contains the following
functions:
    * folder_prep - makes CSV folder and/or files on specified location, if necessary
    * wait_for_file_input - waits for file to be not-empty before making plots
    * impl_circular_buffer - treats each sensor's CSV as a circular buffer with MAX_ROWS size
    * make_plots - returns a figure based on data from passed csv file
    * construct_labels - constructs labels based on current value; can include tips as well
    * store_to_csv - listens to serial port and writes values to appropriate CSV files
"""

import os
import threading
import time
import tkinter as tk
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import serial
from constants import *
import pages as pg


matplotlib.use("TkAgg")


def folder_prep():
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    if len(os.listdir(csv_folder)) == 0:
        open(tmp116_csv, 'a').close()
        open(hdc2010_temp_csv, 'a').close()
        open(hdc2010_hum_csv, 'a').close()
        open(opt3001_csv, 'a').close()
        open(dps310_temp_csv, 'a').close()
        open(dps310_pressure_csv, 'a').close()


def wait_for_file_input(filepath):
    while ((os.path.exists(filepath) and os.path.getsize(filepath) == 0)
           or not os.path.exists(filepath)):
        pass


# Read file and remove oldest redundant records
def impl_circular_buffer(path):
    # TODO: budući da je ovo csv, sigurno postoji neka pametnija pandas metoda za saznat koliko ima redova
    with open(path, 'r') as file:
        lines = []
        for row in file.readlines():
            lines.append(row)
        num_rows = len(lines)
    file.close()

    if num_rows > MAX_ROWS:
        extra_rows = num_rows - MAX_ROWS
        with open(path, 'w') as file:
            file.writelines(lines[:1] + lines[(extra_rows + 1):])
    file.close()
    return


def make_plots(filepaths, figsize=None, def_color_idx=-1):
    if figsize is None:
        figsize = (5, 4)

    for filepath in filepaths:
        wait_for_file_input(filepath)
        impl_circular_buffer(filepath)

    df_list = [pd.read_csv(filepath, names=headers) for filepath in filepaths]
    figure = plt.Figure(figsize=figsize, dpi=100)
    ax = figure.add_subplot(111)
    # line = FigureCanvasTkAgg(figure, app)
    # line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    for i in range(len(df_list)):
        # TODO: znam zašto radi ali je ružno
        if def_color_idx == -1:
            color_idx = i
        else:
            color_idx = def_color_idx
        df_list[i].plot(kind='line', legend=True, ax=ax, color=colors[color_idx], fontsize=10)
    # ax.set_title(SENZOR + VRIJEDNOST)

    return figure


# TODO: optimizirati ovo?
def construct_labels(temp=None, humidity=None, light=None, pressure=None, tips_wanted=False):
    label = ''
    if temp is not None:
        label += f'{temp} °C - '
    if temp is not None and temp < TEMP_MIN:
        label += messages['low_temp']
        if tips_wanted:
            label += messages['low_temp_tip']
    elif temp is not None and TEMP_MIN < temp < TEMP_MAX:
        label += messages['normal_temp']
    elif temp is not None and temp > TEMP_MAX:
        label += messages['high_temp']
        if tips_wanted:
            label += messages['high_temp_tip']
    if temp is not None:
        label += '\n'

    if humidity is not None:
        label += f'{humidity}% - '
    if humidity is not None and humidity < HUM_MIN:
        label += messages['low_hum']
        if tips_wanted:
            label += messages['low_hum_tip']
    elif humidity is not None and HUM_MIN < humidity < HUM_MAX:
        label += messages['normal_hum']
    elif humidity is not None and humidity > HUM_MAX:
        label += messages['high_hum']
        if tips_wanted:
            label += messages['high_hum_tip']
    if humidity is not None:
        label += '\n'

    if light is not None:
        label += f'{light} lux - '
    if light is not None and light < LUX_MIN:
        label += messages['low_light']
        if tips_wanted:
            label += messages['low_light_tip']
    elif light is not None and LUX_MIN < light < LUX_MAX:
        label += messages['normal_light']
    elif light is not None and light > LUX_MAX:
        label += messages['high_light']
        if tips_wanted:
            label += messages['high_light_tip']
    if light is not None:
        label += '\n'

    if pressure is not None:
        label += f'{pressure} Pa - '
    if pressure is not None and pressure < LUX_MIN:
        label += messages['low_pressure']
        if tips_wanted:
            label += messages['low_pressure_tip']
    elif pressure is not None and LUX_MIN < pressure < LUX_MAX:
        label += messages['normal_pressure']
    elif pressure is not None and pressure > LUX_MAX:
        label += messages['high_pressure']
        if tips_wanted:
            label += messages['high_pressure_tip']
    if pressure is not None:
        label += '\n'

    return label


def store_to_csv():
    with open(tmp116_csv, 'a', newline='') as tmp116_file, \
            open(hdc2010_temp_csv, 'a', newline='') as hdc2010_temp_file, \
            open(hdc2010_hum_csv, 'a', newline='') as hdc2010_hum_file, \
            open(opt3001_csv, 'a', newline='') as opt3001_file, \
            open(dps310_temp_csv, 'a', newline='') as dps310_temp_file, \
            open(dps310_pressure_csv, 'a', newline='') as dps310_pressure_file:

        for i in range(NUM_OF_SENSORS):
            line = serial.readline()  # read a byte string

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            if line:
                string = line.decode()  # convert the byte string to a unicode string
                split_string = string.split(', ')
                if split_string[0] == 'TMP116':
                    tmp116_file.write(dt_string + ', ' + string)
                elif split_string[0] == 'HDC2010' and split_string[1] == 'temperature':
                    hdc2010_temp_file.write(dt_string + ', ' + string)
                elif split_string[0] == 'HDC2010' and split_string[1] == 'humidity':
                    hdc2010_hum_file.write(dt_string + ', ' + string)
                elif split_string[0] == 'OPT3001':
                    opt3001_file.write(dt_string + ', ' + string)
                elif split_string[0] == 'DPS310' and split_string[1] == 'temperature':
                    dps310_temp_file.write(dt_string + ', ' + string)
                elif split_string[0] == 'DPS310' and split_string[1] == 'pressure':
                    dps310_pressure_file.write(dt_string + ', ' + string)

                print(string)


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
    folder_prep()
    serial = serial.Serial('COM4', 19200, timeout=1)
    serial.reset_input_buffer()
    time.sleep(2)
    threading.Thread(target=thread_gui).start()

    while True:
        store_to_csv()
        time.sleep(1)
