""" File handler

This file contains methods used for file and directory handling, for purposes of running this application.

It can also be imported as a module and contains the following
methods:
    * folder_prep - makes CSV folder and/or files on specified location, if necessary
    * wait_for_file_input - waits for file to be not-empty before making plots
    * impl_circular_buffer - treats each sensor's CSV as a circular buffer with MAX_ROWS size
    * store_to_csv - listens to serial port and writes values to appropriate CSV files
    * write_to_config - updates config.ini (and app functionalities) when called
"""
import os
import threading
from configparser import SafeConfigParser
import time
from datetime import datetime

import serial.tools.list_ports

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

    while ((os.path.exists(filepath) and os.path.getsize(filepath) == 0)
           or not os.path.exists(filepath)):
        pass


def impl_circular_buffer(filepath, buff_size=constants.MAX_ROWS):
    """ Treat csv file as a circular buffer.

        Arguments:
            filepath - location of the file being modified
            buff_size - size of buffer depending on sampling frequency; default MAX_ROWS
    """

    # light and pressure measures require higher sampling rates (more records)
    if (filepath == constants.opt3001_csv) or (filepath == constants.dps310_pressure_csv):
        buff_size = constants.MAX_ROWS_OPT_PRES

    # open file, store its lines to list
    with open(filepath, 'r') as file:
        lines = []
        for row in file.readlines():
            lines.append(row)
        num_rows = len(lines)
    file.close()

    # remove any oldest lines that exceed maximum buffer size and write result to file
    if num_rows > buff_size:
        extra_rows = num_rows - buff_size
        with open(filepath, 'w') as file:
            file.writelines(lines[:1] + lines[(extra_rows + 1):])
    file.close()
    return


def store_to_csv():
    """ Store lines from serial port to respective CSV files. """

    with open(constants.tmp116_csv, 'a', newline='') as tmp116_file, \
            open(constants.hdc2010_temp_csv, 'a', newline='') as hdc2010_temp_file, \
            open(constants.hdc2010_hum_csv, 'a', newline='') as hdc2010_hum_file, \
            open(constants.opt3001_csv, 'a', newline='') as opt3001_file, \
            open(constants.dps310_temp_csv, 'a', newline='') as dps310_temp_file, \
            open(constants.dps310_pressure_csv, 'a', newline='') as dps310_pressure_file:

        for i in range(constants.NUM_OF_SENSORS):  # TODO: change to while-loop because of different sampling rates
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


def thread_serial():
    """ Thread used to continuously store incoming values from serial to csv if device connected """

    while True:
        store_to_csv()


def connect_to_serial():
    """ Connect to serial port if available. """

    # check if port defined as SERIAL_PORT has a device connected to it
    ports = [tuple(p)[0] for p in list(serial.tools.list_ports.comports())]
    arduino_port = [port for port in ports if constants.SERIAL_PORT in port]

    # start serial communication if connected
    if arduino_port:
        constants.serial.reset_input_buffer()  # clear input serial buffer

        time.sleep(1)  # small delay to stabilise
        threading.Thread(target=thread_serial).start()  # start thread

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