""" File handler

This file contains methods used for file and directory handling, for purposes of running this application.

It can also be imported as a module and contains the following
methods:
    * folder_prep - makes CSV folder and/or files on specified location, if necessary
    * wait_for_file_input - waits for file to be not-empty before making plots
    * impl_circular_buffer - treats each sensor's CSV as a circular buffer with BUFFER_MINUTES length
    * store_to_csv - listens to serial port and writes values to appropriate CSV files
    * write_to_config - updates config.ini (and app functionalities) when called
    * check_serial_connection - check if SERIAL_PORT Arduino communication available
    * connect_to_serial - connect to Arduino communication on SERIAL_PORT if available
    * check_pressure_diffs - detects significant pressure differences that could mean door/window opening
"""
import os
import threading
from configparser import SafeConfigParser
import time
from datetime import datetime

import pandas as pd
import serial.tools.list_ports
from future.backports.datetime import timedelta

import constants
import element_constructor as ec


def folder_prep():
    """ Prepare and/or modify folder and file locations for sensor readings. """

    # make csv folder if it doesn't exist
    if not os.path.exists(constants.csv_folder):
        os.makedirs(constants.csv_folder)

    # populate csv folder with specified files if it's empty
    if len(os.listdir(constants.csv_folder)) == 0:
        open(constants.tmp116_csv, 'a').close()
        open(constants.hdc2010_temp_csv, 'a').close()
        open(constants.hdc2010_hum_csv, 'a').close()
        open(constants.opt3001_csv, 'a').close()
        open(constants.dps310_temp_csv, 'a').close()
        open(constants.dps310_pressure_csv, 'a').close()


def wait_for_file_input(filepath):
    """ Wait for file to be non-empty before plotting its data.
        This is to avoid a possible bug when plotting

        Arguments:
            filepath - location of the file waiting for input
    """

    while ((os.path.exists(filepath) and os.stat(filepath).st_size == 0)
           or not os.path.exists(filepath)):
        pass


def check_pressure_diffs():
    """ Detect significant pressure differences that could mean door/window opening. """

    # read pressure csv and convert values to datetime
    pressure_data = pd.read_csv(constants.dps310_pressure_csv, names=constants.headers)
    pressure_data['Vrijeme'] = pd.to_datetime(pressure_data['Vrijeme'], format='%d/%m/%Y %H:%M:%S')

    # construct PRESSURE_INTERVAL_SECS duration datetime object to be added to times
    seconds_delta = timedelta(seconds=constants.PRESSURE_INTERVAL_SECS)

    # add PRESSURE_INTERVAL_SECONDS to 'Vrijeme' in all rows
    pressure_data['Vrijeme'] = pressure_data['Vrijeme'] + seconds_delta

    # filter out readings from last PRESSURE_INTERVAL_SECS seconds
    pressure_data_nsecs = pressure_data[pressure_data['Vrijeme'] > datetime.now()]

    # filter out rows with min and max pressure values
    max_value_row = pressure_data_nsecs[pressure_data_nsecs['Vrijednost'] == pressure_data_nsecs['Vrijednost'].max()]
    min_value_row = pressure_data_nsecs[pressure_data_nsecs['Vrijednost'] == pressure_data_nsecs['Vrijednost'].min()]

    # return at what time the dip/increase in pressure happened
    if not max_value_row.empty and not min_value_row.empty:

        # there can be multiple rows w/ same min/max value
        # return the first one because the HH:MM value would be same either way
        if max_value_row['Vrijednost'].iloc[0] - min_value_row['Vrijednost'].iloc[0] > constants.PRESSURE_DIFF_PA:

            # return the sooner timestamp in HH:MM format or '' if not applicable
            if max_value_row['Vrijeme'].iloc[0] < min_value_row['Vrijeme'].iloc[0]:
                return max_value_row['Vrijeme'].iloc[0].strftime('%H:%M')
            else:
                return min_value_row['Vrijeme'].iloc[0].strftime('%H:%M')
        else:
            return ''
    return ''


def impl_circular_buffer(filepath):
    """ Treat csv file as a circular buffer with BUFFER_MINUTES size.

        Arguments:
            filepath - location of the file being modified
    """

    # open file, store lines newer than 10 minutes to list
    # discard older lines
    with open(filepath, 'r') as file:
        lines = []  # list of file lines
        now = datetime.now()  # current time

        for row in file.readlines():
            data = row.split(',')
            timestamp = datetime.strptime(data[0], '%d/%m/%Y %H:%M:%S')  # get timestamp from row

            time_delta = now - timestamp  # calculate difference between row time and current time
            seconds_delta = time_delta.total_seconds()  # -> to seconds
            minutes_delta = seconds_delta / 60  # -> to minutes

            # append to lines only rows newer than BUFFER_MINUTES minutes
            if minutes_delta < constants.BUFFER_MINUTES:
                lines.append(row)
    file.close()

    # write lines to file
    with open(filepath, 'w') as file:
        file.writelines(lines)


def store_to_csv():
    """ Store lines from serial port to respective CSV files. """

    with open(constants.tmp116_csv, 'a', newline='') as tmp116_file, \
            open(constants.hdc2010_temp_csv, 'a', newline='') as hdc2010_temp_file, \
            open(constants.hdc2010_hum_csv, 'a', newline='') as hdc2010_hum_file, \
            open(constants.opt3001_csv, 'a', newline='') as opt3001_file, \
            open(constants.dps310_temp_csv, 'a', newline='') as dps310_temp_file, \
            open(constants.dps310_pressure_csv, 'a', newline='') as dps310_pressure_file:

        try:
            line = constants.serial.readline()  # read a byte string

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            if line:
                string = line.decode()  # convert the byte string to a unicode string
                split_string = string.split(', ')

                # choose write file location based on sensor name and value
                # add current time to record
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
        except AttributeError:
            return


def thread_serial():
    """ Thread used to continuously store incoming values from serial to csv if device connected """

    while True:
        if check_serial_connection():
            store_to_csv()


def check_serial_connection():
    """ Return True if SERIAL_PORT active, False if not. """

    # check if port defined as SERIAL_PORT has a device connected to it
    ports = [tuple(p)[0] for p in list(serial.tools.list_ports.comports())]
    arduino_port = [port for port in ports if constants.SERIAL_PORT in port]

    # start serial communication if connected
    if arduino_port:
        return True

    return False


def connect_to_serial():
    """ Connect to serial port if available. """

    # check if port defined as SERIAL_PORT has a device connected to it
    if check_serial_connection():
        constants.serial.reset_input_buffer()  # clear input serial buffer

        time.sleep(1)  # small delay to stabilise
        threading.Thread(target=thread_serial, daemon=True).start()  # start thread

    # if not, print a message to console
    else:
        print(f'Serial port {constants.SERIAL_PORT} unavailable. '
              f'Connect your device to {constants.SERIAL_PORT} or redefine SERIAL_PORT.')


def write_to_config(values):
    """ Stores values from Update Page to config.ini.
        Calls for reload of constants.py module where necessary in order to update whole app.

        Parameters
        ----------
            values : dict
            A dictionary of {min/max reading : min/max value, serial_port : port name}.
    """

    config_parser = SafeConfigParser()
    config_parser.read('config.ini')

    serial_port_old = config_parser['updatable']['serial_port']  # old serial port in case of port reconnection

    # set values in [updatable] section to those passed as argument
    for key, value in values.items():
        config_parser.set('updatable', key, value)

    # write changes to 'config.ini'
    with open('config.ini', 'w') as configfile:
        config_parser.write(configfile)

    ec.reload_constants()  # update values (min/max) for element construction

    # if serial port changed, reconnect to new port
    serial_port_new = config_parser['updatable']['serial_port']
    if serial_port_old != serial_port_new:
        connect_to_serial()
