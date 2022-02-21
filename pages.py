"""Pages

This file contains classes used to construct all pages in app,
as tk.Frame objects (child classes of tk.Frame).
"""
import tkinter as tk
from tkinter import messagebox

import matplotlib
import pandas as pd
import numpy as np
import re

from constants import *
import element_constructor as ec
import file_handler as fh
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


def validate_entries(values):
    """ Validates entries on Update page and returns True if valid,
        raises warning messagebox if not.
    """

    try:
        if (float(values['TEMP_MIN']) and float(values['TEMP_MAX'])
                and float(values['HUM_MIN']) and float(values['HUM_MAX'])
                and float(values['LUX_MIN']) and float(values['LUX_MAX'])
                and float(values['PRES_MIN']) and float(values['PRES_MAX'])
                and re.match("COM[0-9][0-9]?$", values['SERIAL_PORT'])):
            return True
        else:
            messagebox.showerror('Neispravan unos!', 'Molimo, pokušajte ponovo.')
        return False
    except ValueError:
        messagebox.showerror('Neispravan unos!', 'Molimo, pokušajte ponovo.')
        return False


class UpdatePage(tk.Frame):
    """
        A class for a page used to update MIN, MAX values and serial port.
        This is achieved by fetching new data from the GUI, and calling file_handler.py
        method write_to_config(values) to change the config.ini file.

        Attributes
        ----------
        temp_min, temp_max, hum_min, ... : tk.StringVar
            Variables that hold the string values of min/max values of different types of sensor readings.

        serial_port : tk.StringVar
            Holds the string value of the port your Arduino device should be connected to.

        labels : tk.Label
            Indicate the values to be modified through Entries.

        entries : tk.Entry
            Editable text boxes that allow the user to modify values.
            Each entry is matched to one value.

        buttons : tk.Button
            Update and Back


        Methods
        -------
        init_labels(self, page_label)
            Initialises page title label and labels indicating Entries' functions.

        init_buttons(self, controller)
            Initialises Back and Update button and their commands.

        init_entries(self)
            Initialises Entry elements on the page and their functions.

        update_config(self)
            Makes a dict of {min/max reading : min/max value, serial_port : port name}
            and calls fh.write_to_config with it as parameter, to rewrite the config.ini file with new values.

        update_data(self, controller)
            Is called on click of Update button.
            Calls update_config upon self and controller (app)'s update via app_update().

    """

    def update_data(self, controller):
        self.update_config()
        controller.app_update()

    def update_config(self):
        values = {'TEMP_MIN': self.temp_min.get(),
                  'TEMP_MAX': self.temp_max.get(),
                  'HUM_MIN': self.hum_min.get(),
                  'HUM_MAX': self.hum_max.get(),
                  'LUX_MIN': self.light_min.get(),
                  'LUX_MAX': self.light_max.get(),
                  'PRES_MIN': self.pres_min.get(),
                  'PRES_MAX': self.pres_max.get(),
                  'SERIAL_PORT': self.serial_port.get()}

        if validate_entries(values):
            fh.write_to_config(values)

    def init_labels(self, page_label):
        label = tk.Label(self, text=page_label, font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label_temp_min = tk.Label(self, text='Minimalna temperatura [°C]: ')
        label_temp_min.place(x=100, y=125)

        label_temp_max = tk.Label(self, text='Maksimalna temperatura [°C]: ')
        label_temp_max.place(x=100, y=150)

        label_hum_min = tk.Label(self, text='Minimalna vlažnost [%]: ')
        label_hum_min.place(x=100, y=200)

        label_hum_max = tk.Label(self, text='Maksimalna vlažnost [%]: ')
        label_hum_max.place(x=100, y=225)

        label_light_min = tk.Label(self, text='Minimalna količina svjetla [lux]: ')
        label_light_min.place(x=100, y=275)

        label_light_max = tk.Label(self, text='Maksimalna količina svjetla [lux]: ')
        label_light_max.place(x=100, y=300)

        label_pres_min = tk.Label(self, text='Minimalni atmosferski tlak [Pa]: ')
        label_pres_min.place(x=100, y=350)

        label_pres_max = tk.Label(self, text='Maksimalni atmosferski tlak [Pa]: ')
        label_pres_max.place(x=100, y=375)

        label_serial = tk.Label(self, text='Serial port: ')
        label_serial.place(x=100, y=425)

    def init_buttons(self, controller):
        button = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(StartPage))
        button.place(x=50, y=20)

        button_calc = tk.Button(self, text="Ažuriraj", command=lambda: self.update_data(controller))
        button_calc.pack()

    def init_entries(self):
        entry_temp_min = tk.Entry(self, textvariable=self.temp_min)
        entry_temp_min.place(x=375, y=125)

        entry_temp_max = tk.Entry(self, textvariable=self.temp_max)
        entry_temp_max.place(x=375, y=150)

        entry_hum_min = tk.Entry(self, textvariable=self.hum_min)
        entry_hum_min.place(x=375, y=200)

        entry_hum_max = tk.Entry(self, textvariable=self.hum_max)
        entry_hum_max.place(x=375, y=225)

        entry_light_min = tk.Entry(self, textvariable=self.light_min)
        entry_light_min.place(x=375, y=275)

        entry_light_max = tk.Entry(self, textvariable=self.light_max)
        entry_light_max.place(x=375, y=300)

        entry_pres_min = tk.Entry(self, textvariable=self.pres_min)
        entry_pres_min.place(x=375, y=350)

        entry_pres_max = tk.Entry(self, textvariable=self.pres_max)
        entry_pres_max.place(x=375, y=375)

        entry_serial = tk.Entry(self, textvariable=self.serial_port)
        entry_serial.place(x=375, y=425)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_labels('Ažuriranje vrijednosti')
        self.init_buttons(controller)

        self.temp_min = tk.StringVar(value=TEMP_MIN)
        self.temp_max = tk.StringVar(value=TEMP_MAX)
        self.hum_min = tk.StringVar(value=HUM_MIN)
        self.hum_max = tk.StringVar(value=HUM_MAX)
        self.light_min = tk.StringVar(value=LUX_MIN)
        self.light_max = tk.StringVar(value=LUX_MAX)
        self.pres_min = tk.StringVar(value=PRES_MIN)
        self.pres_max = tk.StringVar(value=PRES_MAX)
        self.serial_port = tk.StringVar(value=SERIAL_PORT)

        self.init_entries()


class SensorPage(tk.Frame):
    """
        A class used as parent class for various sensor pages
        Is a child class of tk.Frame

        Attributes
        ----------
        average_message : tk.StringVar
            Variable message about the average value in matching sensor reading buffer.

        current_message : tk.StringVar
            Variable message about the latest value in matching sensor reading buffer.

        graphs : tk.Figure
            Each sensor page contains 1 or 2 graphs for its readings.
            Graph data is stored in csv as a circular buffer.
            Graph figures are drawn using FigureCanvasTkAgg.

        average values : tk.Label
            Label(s) containing average_message(s).

        current values : tk.Label
            Label(s) containing current_message(s).

        Methods
        -------
        init_label(self, sensor_label)
            Makes and places page title (sensor name).

        init_buttons(self, controller)
            Makes and places buttons ("Return" button).

        update_data(self, files, values, measures)
            Makes and places graphs and average and current values on the page for all sensor readings.
            Allows values to be updated interactively by clicking update button.
    """

    def update_data(self, files, values, measures):
        """Updates graphs and labels on page

            Parameters
            ----------
            self : SensorPage

            files : list(str)
                list of files the data will be generated from

            values : list(str)
                list of names of values being measured to construct labels (in Croatian)

            measures : list(str)
                list of measures ('°C', '%', ...) to construct labels
        """

        file_num = 0
        for file in files:
            figure = ec.make_plots([file])
            canvas = FigureCanvasTkAgg(figure, self)
            canvas.draw()
            canvas.get_tk_widget().place(x=graph_coords[file_num][0], y=graph_coords[file_num][1])

            # Calculate average value from file and place label accordingly.
            data = pd.read_csv(file, names=headers)
            average = str(round(data['Vrijednost'].mean(), 4))
            self.average_message.set('Prosječna vrijednost '
                                     + values[file_num] + ': '
                                     + average + measures[file_num])
            avg_label = tk.Label(self, textvariable=self.average_message)
            avg_label.place(x=text_coords[file_num][0], y=text_coords[file_num][1])

            # Use last value from file as current value and place label accordingly
            value = data.iloc[-1]['Vrijednost']
            self.current_message.set(ec.construct_labels(
                measure=values[file_num], value=value))
            indicator_label = tk.Label(self, textvariable=self.current_message)
            indicator_label.place(x=current_coords[file_num][0], y=current_coords[file_num][1])

            file_num += 1

    def init_label(self, sensor_label):
        label = tk.Label(self, text=sensor_label, font=LARGE_FONT)
        label.pack(pady=10, padx=10)

    def init_buttons(self, controller):
        button = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(StartPage))
        button.place(x=50, y=20)

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.average_message = tk.StringVar()
        self.current_message = tk.StringVar()


class TMP116Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.average_message = tk.StringVar()
        self.current_message = tk.StringVar()

        TMP116Page.init_label(self, "TMP116")
        TMP116Page.init_buttons(self, controller)
        TMP116Page.update_data(self, [tmp116_csv], [temp_string], [temp_measurement])

        # a button to update TMP116 page
        button_update = tk.Button(self, text="Ažuriraj", command=lambda: SensorPage.update_data(
            self, [tmp116_csv], [temp_string], [temp_measurement]
        ))
        button_update.place(x=100, y=20)


class HDC2010Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.average_message = tk.StringVar()
        self.current_message = tk.StringVar()

        HDC2010Page.init_label(self, "HDC2010")
        HDC2010Page.init_buttons(self, controller)
        HDC2010Page.update_data(self, [hdc2010_temp_csv, hdc2010_hum_csv],
                                [temp_string, hum_string], [temp_measurement, hum_measurement])

        # a button to update HDC2010 page
        button_update = tk.Button(self, text="Ažuriraj",
                                  command=lambda: SensorPage.update_data(self, [hdc2010_temp_csv, hdc2010_hum_csv],
                                                                         [temp_string, hum_string],
                                                                         [temp_measurement, hum_measurement]))
        button_update.place(x=100, y=20)


class OPT3001Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.average_message = tk.StringVar()
        self.current_message = tk.StringVar()

        OPT3001Page.init_label(self, "OPT3001")
        OPT3001Page.init_buttons(self, controller)
        OPT3001Page.update_data(self, [opt3001_csv], [light_string], [light_measurement])

        # a button to update OPT3001 page
        button_update = tk.Button(self, text="Ažuriraj", command=lambda: SensorPage.update_data(
            self, [opt3001_csv], [light_string], [light_measurement]))
        button_update.place(x=100, y=20)


class DPS310Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.average_message = tk.StringVar()
        self.current_message = tk.StringVar()

        DPS310Page.init_label(self, "DPS301")
        DPS310Page.init_buttons(self, controller)
        DPS310Page.update_data(self, [dps310_temp_csv, dps310_pressure_csv],
                               [temp_string, pressure_string], [temp_measurement, pressure_measurement])

        # a button to update DPS310 page
        button_update = tk.Button(self, text="Ažuriraj",
                                  command=lambda: SensorPage.update_data(self, [dps310_temp_csv, dps310_pressure_csv],
                                                                         [temp_string, pressure_string],
                                                                         [temp_measurement, pressure_measurement]))
        button_update.place(x=100, y=20)


class StartPage(tk.Frame):
    # TODO: update grafova na početnoj strani
    # TODO: općenito - nazivi grafova, legende, boje, vrijeme očitanja
    # TODO: jel trebamo i tu ispisivati prosječne vrijednosti ili je dovoljno trenutne?

    """
        A class used to represent the app's start page
        Is a child class of tk.Frame

        Attributes
        ----------
        graphs : tk.Figure
            Contains 4 graphs, one for each value.
            Values measured using multiple sensors are represented on same graph (e.g. temperature),
            using different colour lines.

        current values : tk.Label
            Contains latest measure values and appropriate messages.
            Messages also contain tips (telling the user to heat the room, let light in, etc.).
            Current values, if measured by multiple sensors, are calculated as their average.

        buttons : tk.Button
            update button - updates all updateable data on page
            sensor buttons - open respective sensor pages

        Methods
        -------
        update_start_data(self)
            Makes and places graphs and current values on the page for all sensors' readings.
            Allows values to be updated interactively by clicking update button.
    """

    def update_start_data(self):
        # temperature graph (3 sensors' values)
        figure = ec.make_plots([tmp116_csv, hdc2010_temp_csv, dps310_temp_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=250)

        # humidity graph
        figure = ec.make_plots([hdc2010_hum_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=400, y=250)

        # light levels graph
        figure = ec.make_plots([opt3001_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=700, y=250)

        # atmospheric pressure graph
        figure = ec.make_plots([dps310_pressure_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=1000, y=250)

        # current values
        temp_value = round(np.average([pd.read_csv(tmp116_csv, names=headers)['Vrijednost'].iloc[-1],
                                       pd.read_csv(hdc2010_temp_csv, names=headers)['Vrijednost'].iloc[-1],
                                       pd.read_csv(dps310_temp_csv, names=headers)['Vrijednost'].iloc[-1]]), 4)
        hum_value = pd.read_csv(hdc2010_hum_csv, names=headers)['Vrijednost'].iloc[-1]
        light_value = pd.read_csv(opt3001_csv, names=headers)['Vrijednost'].iloc[-1]
        pressure_value = pd.read_csv(dps310_pressure_csv, names=headers)['Vrijednost'].iloc[-1]

        self.indicator_message.set(ec.construct_labels(temp=temp_value, humidity=hum_value, light=light_value,
                                                       pressure=pressure_value, tips_wanted=True))
        indicator_label = tk.Label(self, textvariable=self.indicator_message)
        indicator_label.place(x=100, y=675)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.indicator_message = tk.StringVar()
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        StartPage.update_start_data(self)

        button_tmp = tk.Button(self, text="TMP116 očitanja", command=lambda: controller.show_frame(TMP116Page))
        button_tmp.pack()

        button_hdc = tk.Button(self, text="HDC2010 očitanja", command=lambda: controller.show_frame(HDC2010Page))
        button_hdc.pack()

        button_opt = tk.Button(self, text="OPT3001 očitanja", command=lambda: controller.show_frame(OPT3001Page))
        button_opt.pack()

        button_dps = tk.Button(self, text="DPS301 očitanja", command=lambda: controller.show_frame(DPS310Page))
        button_dps.pack()

        button_updatepage = tk.Button(self, text="Ažuriranje vrijednosti",
                                      command=lambda: controller.show_frame(UpdatePage))
        button_updatepage.pack()

        button_update = tk.Button(self, text="Ažuriraj", command=lambda: StartPage.update_start_data(self))
        button_update.place(x=100, y=20)
