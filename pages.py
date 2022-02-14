"""Pages

This file contains classes used to construct all pages in app,
as tk.Frame objects (child classes of tk.Frame).
"""

import tkinter as tk
import matplotlib
import pandas as pd
import numpy as np
from constants import *
import gui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


class SensorPage(tk.Frame):
    """
        A class used as parent class for various sensor pages
        Is a child class of tk.Frame

        Attributes
        ----------
        graphs : tk.Figure
            Each sensor page contains 1 or 2 graphs for its readings.
            Graph data is stored in csv as a circular buffer.
            Graph figures are drawn using FigureCanvasTkAgg.

        average values : tk.Label
            Average values of sensor readings (from matching csv files).

        Methods
        -------
        init_label(self, sensor_label)
            Makes and places page title (sensor name).

        init_buttons(self, controller)
            Makes and places buttons ("Return" button).

        update_data(self, files, values, measures)
            Makes and places graphs and average values on the page for all sensor readings.
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
            figure = gui.make_plots([file])
            canvas = FigureCanvasTkAgg(figure, self)
            canvas.draw()
            canvas.get_tk_widget().place(x=graph_coords[file_num][0], y=graph_coords[file_num][1])

            data = pd.read_csv(file, names=headers)
            average = str(round(data['Vrijednost'].mean(), 4))
            average_message = 'Prosječna vrijednost ' \
                              + values[file_num] + ': ' \
                              + average + measures[file_num]
            avg_label = tk.Label(self, text=average_message)
            avg_label.place(x=text_coords[file_num][0], y=text_coords[file_num][1])

            file_num += 1

    def init_label(self, sensor_label):
        label = tk.Label(self, text=sensor_label, font=LARGE_FONT)
        label.pack(pady=10, padx=10)

    def init_buttons(self, controller):
        button = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(StartPage))
        button.place(x=50, y=20)

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)


class TMP116Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        TMP116Page.init_label(self, "TMP116")
        TMP116Page.init_buttons(self, controller)
        TMP116Page.update_data(self, [tmp116_csv], [temp_string], [temp_measurement])

        # a button to update TMP116 page
        button_update = tk.Button(self, text="Ažuriraj", command=lambda: SensorPage.update_data(
            self, [tmp116_csv], [temp_string], [temp_measurement]
        ))
        button_update.place(x=100, y=20)

        # Read latest value gotten from TMP116
        # Construct informative message depending on the value
        # Place value and message on page as a Label
        value = pd.read_csv(tmp116_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=gui.construct_labels(temp=value, tips_wanted=True))
        indicator_label.place(x=100, y=650)


class HDC2010Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
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

        # Read latest values gotten from HDC2010
        # Construct informative messages depending on the value
        # Place values and messages on page as a Label
        value = pd.read_csv(hdc2010_temp_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=gui.construct_labels(temp=value, tips_wanted=True))
        indicator_label.place(x=100, y=650)

        value = pd.read_csv(hdc2010_hum_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=gui.construct_labels(humidity=value, tips_wanted=True))
        indicator_label.place(x=100, y=675)


class OPT3001Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        OPT3001Page.init_label(self, "OPT3001")
        OPT3001Page.init_buttons(self, controller)
        OPT3001Page.update_data(self, [opt3001_csv], [light_string], [light_measurement])

        # a button to update OPT3001 page
        button_update = tk.Button(self, text="Ažuriraj", command=lambda: SensorPage.update_data(
            self, [opt3001_csv], [light_string], [light_measurement]))
        button_update.place(x=100, y=20)

        # Read latest value gotten from OPT3001
        # Construct informative message depending on the value
        # Place value and message on page as a Label
        value = pd.read_csv(opt3001_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=gui.construct_labels(light=value, tips_wanted=True))
        indicator_label.place(x=100, y=650)


class DPS310Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
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

        # Read latest values gotten from DPS310
        # Construct informative messages depending on the value
        # Place values and messages on page as a Label
        value = pd.read_csv(dps310_temp_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=gui.construct_labels(temp=value, tips_wanted=True))
        indicator_label.place(x=100, y=650)

        value = pd.read_csv(dps310_pressure_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=gui.construct_labels(pressure=value, tips_wanted=True))
        indicator_label.place(x=100, y=675)


class StartPage(tk.Frame):
    # TODO: update grafova na početnoj strani
    # TODO: općenito - nazivi grafova, legende, boje
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
        figure = gui.make_plots([tmp116_csv, hdc2010_temp_csv, dps310_temp_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=250)

        # humidity graph
        figure = gui.make_plots([hdc2010_hum_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=400, y=250)

        # light levels graph
        figure = gui.make_plots([opt3001_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=700, y=250)

        # atmospheric pressure graph
        figure = gui.make_plots([dps310_pressure_csv], (3, 3))
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
        indicator_label = tk.Label(self, text=gui.construct_labels(temp=temp_value, humidity=hum_value, light=light_value,
                                                                   pressure=pressure_value, tips_wanted=True))
        indicator_label.place(x=100, y=675)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
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

        button_update = tk.Button(self, text="Ažuriraj", command=lambda: StartPage.update_start_data(self))
        button_update.place(x=100, y=20)
