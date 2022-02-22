""" Element constructor

This file contains methods used for construction of visual tkinter elements.
The return values of its methods are elements to be placed on pages the methods were called from.

This file can also be imported as a module and contains the following
functions:
    * make_plots - returns a figure based on data from passed csv file
    * construct_labels - constructs labels based on current value; can include tips as well
"""
import importlib
import pandas as pd
from matplotlib import pyplot as plt

import file_handler as fh
import constants


def reload_constants():
    """ Reload constants.py module to make all values used updated. """
    importlib.reload(constants)


def make_plots(filepaths, figsize=None, title=None, unit=None, def_color_idx=-1):
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

    df_list = [pd.read_csv(filepath, names=constants.headers) for filepath in filepaths]
    figure = plt.Figure(figsize=figsize, dpi=100)
    ax = figure.add_subplot(111)

    for i in range(len(df_list)):
        # TODO: znam zašto radi ali je ružno
        if def_color_idx == -1:
            color_idx = i
        else:
            color_idx = def_color_idx
        df_list[i].plot(ax=ax, kind='line', color=constants.colors[color_idx], fontsize=10)

    ax.legend([df.Senzor[0] for df in df_list])
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_ylabel(unit, rotation=0)
    ax.set_xlabel('vrijeme', rotation=0)
    ax.ticklabel_format(useOffset=False)
    ax.yaxis.set_label_coords(-0.05, 1.02)

    return figure


def construct_labels(measure=None, value=None, temp=None, humidity=None, light=None, pressure=None, tips_wanted=False):
    """ Construct labels with messages about current values and tips (if wanted).

        Arguments:
            temp - temperature value in °C (if available)
            humidity - humidity value in % (if available)
            light - light value in lux (if available)
            pressure - pressure value in Pa (if available)
            tips_wanted - indicate whether to include tips in the message; default - no (False)
    """

    if measure == constants.temp_string: temp = value
    if measure == constants.hum_string: humidity = value
    if measure == constants.light_string: light = value
    if measure == constants.pressure_string: pressure = value

    label = ''
    if temp is not None:
        label += f'{temp} °C - '
    if temp is not None and temp < constants.TEMP_MIN:
        label += constants.messages['low_temp']
        if tips_wanted:
            label += '\n' + constants.messages['low_temp_tip']
    elif temp is not None and constants.TEMP_MIN < temp < constants.TEMP_MAX:
        label += constants.messages['normal_temp']
    elif temp is not None and temp > constants.TEMP_MAX:
        label += constants.messages['high_temp']
        if tips_wanted:
            label += '\n' + constants.messages['high_temp_tip']
    if temp is not None:
        label += '\n\n'

    if humidity is not None:
        label += f'{humidity}% - '
    if humidity is not None and humidity < constants.HUM_MIN:
        label += constants.messages['low_hum']
        if tips_wanted:
            label += '\n' + constants.messages['low_hum_tip']
    elif humidity is not None and constants.HUM_MIN < humidity < constants.HUM_MAX:
        label += constants.messages['normal_hum']
    elif humidity is not None and humidity > constants.HUM_MAX:
        label += constants.messages['high_hum']
        if tips_wanted:
            label += '\n' + constants.messages['high_hum_tip']
    if humidity is not None:
        label += '\n\n'

    if light is not None:
        label += f'{light} lux - '
    if light is not None and light < constants.LUX_MIN:
        label += constants.messages['low_light']
        if tips_wanted:
            label += '\n' + constants.messages['low_light_tip']
    elif light is not None and constants.LUX_MIN < light < constants.LUX_MAX:
        label += constants.messages['normal_light']
    elif light is not None and light > constants.LUX_MAX:
        label += constants.messages['high_light']
        if tips_wanted:
            label += '\n' + constants.messages['high_light_tip']
    if light is not None:
        label += '\n\n'

    if pressure is not None:
        label += f'{pressure} Pa - '
    if pressure is not None and pressure < constants.PRES_MIN:
        label += constants.messages['low_pressure']
        if tips_wanted:
            label += '\n' + constants.messages['low_pressure_tip']
    elif pressure is not None and constants.PRES_MIN < pressure < constants.PRES_MAX:
        label += constants.messages['normal_pressure']
    elif pressure is not None and pressure > constants.PRES_MAX:
        label += constants.messages['high_pressure']
        if tips_wanted:
            label += '\n' + constants.messages['high_pressure_tip']
    if pressure is not None:
        label += '\n'

    return label
