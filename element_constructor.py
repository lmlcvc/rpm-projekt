""" Element constructor

This file contains methods used for construction of visual tkinter elements.
The return values of its methods are elements to be placed on pages the methods were called from.

It can also be imported as a module and contains the following
functions:
    * folder_prep - makes CSV folder and/or files on specified location, if necessary
    * wait_for_file_input - waits for file to be not-empty before making plots
    * impl_circular_buffer - treats each sensor's CSV as a circular buffer with MAX_ROWS size
    * store_to_csv - listens to serial port and writes values to appropriate CSV files

This file can also be imported as a module and contains the following
functions:
    * make_plots - returns a figure based on data from passed csv file
    * construct_labels - constructs labels based on current value; can include tips as well
"""

import pandas as pd
from matplotlib import pyplot as plt

import file_handler as fh
from constants import *


def make_plots(filepaths, figsize=None, def_color_idx=-1):
    # TODO: dodati mjernu veličinu na y os, vrijeme prvog i zadnjeg očitanja na x os, bojanje, \
    #  postaviti legende i naslov grafa
    """ Return sensor readings plot as a plt.Figure.

        Arguments:
            filepaths - locations of files whose readings are to be plotted on the figure
            figsize - size of figure; default (5, 4)
            def_color_idx - # TODO: define when colouring is modified
    """

    if figsize is None:  # define default figsize
        figsize = (5, 4)

    for filepath in filepaths:
        fh.wait_for_file_input(filepath)
        fh.impl_circular_buffer(filepath)

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


def construct_labels(temp=None, humidity=None, light=None, pressure=None, tips_wanted=False):
    """ Construct labels with messages about current values and tips (if wanted).

        Arguments:
            temp - temperature value in °C (if available)
            humidity - humidity value in % (if available)
            light - light value in lux (if available)
            pressure - pressure value in Pa (if available)
            tips_wanted - indicate whether to include tips in the message; default - no (False)
    """

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
