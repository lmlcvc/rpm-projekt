import serial
import time
from datetime import datetime
import configparser
import matplotlib.pyplot as plt
import pandas as pd
import os
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

config = configparser.ConfigParser()
config.read('config.ini')
config = config['default']

# directory = config['transformed_location']
csv_folder = config['csv']
tmp116_csv = config['tmp116_csv']
hdc2010_temp_csv = config['hdc2010_temp_csv']
hdc2010_hum_csv = config['hdc2010_hum_csv']
opt3001_csv = config['opt3001_csv']
dps310_temp_csv = config['dps310_temp_csv']
dps310_pressure_csv = config['dps310_pressure_csv']

headers = ['Vrijeme', 'Senzor', 'Velicina', 'Vrijednost']
MAX_ROWS = 100


def create_folder():
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)


def store_to_csv():
    with open(tmp116_csv, 'a', newline='') as tmp116_file, \
            open(hdc2010_temp_csv, 'a', newline='') as hdc2010_temp_file, \
            open(hdc2010_hum_csv, 'a', newline='') as hdc2010_hum_file, \
            open(opt3001_csv, 'a', newline='') as opt3001_file, \
            open(dps310_temp_csv, 'a', newline='') as dps310_temp_file, \
            open(dps310_pressure_csv, 'a', newline='') as dps310_pressure_file:

        for i in range(30):
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


# TODO: nazivi datoteka, mjerne jedinice itd., nije tragedija
# Read file and remove oldest redundant records
def impl_circular_buffer(path):
    with open(path, 'r') as file:
        lines = []
        for row in file.readlines():
            lines.append(row)
        num_rows = len(lines)
        print(lines, num_rows)
    file.close()

    if num_rows > MAX_ROWS:
        extra_rows = num_rows - MAX_ROWS
        print(extra_rows)
        with open(path, 'w') as file:
            file.writelines(lines[:1] + lines[(extra_rows + 1):])
    file.close()
    return


def make_plots(filepath):
    with open(filepath) as f:
        impl_circular_buffer(filepath)

        df = pd.read_csv(f, names=headers)
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        # line = FigureCanvasTkAgg(figure, app)
        # line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df.plot(kind='line', legend=True, ax=ax, color='r', marker='o', fontsize=10)
        ax.set_title(df[headers[1]][0] + ' ' + df[headers[2]][0])

    """figures = []
    for filename in os.listdir(csv_folder):
        with open(os.path.join(csv_folder, filename), 'r') as f:
            impl_circular_buffer(os.path.join(csv_folder, filename))

            df = pd.read_csv(f, names=headers)
            figure = plt.Figure(figsize=(5, 4), dpi=100)
            ax = figure.add_subplot(111)
            line = FigureCanvasTkAgg(figure, app)
            line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
            df.plot(kind='line', legend=True, ax=ax, color='r', marker='o', fontsize=10)
            ax.set_title(df[headers[1]][0] + ' ' + df[headers[2]][0])

            figures.append(figure)
    return figures"""
    return figure


if __name__ == "__main__":
    # TODO: dal se .ino može pokreniti iz pythona bez otvaranja svih onih programa
    create_folder()

    # make sure the 'COM#' is set according the Windows Device Manager
    serial = serial.Serial('COM4', 19200, timeout=1)
    serial.reset_input_buffer()
    time.sleep(2)

    store_to_csv()  # TODO: promijeniti logiku da se stalno vrti
    # ser.close()

    """root = tk.Tk()
    while True:
        store_to_csv()
        make_plots()
        root.mainloop()"""

    # make_plots()
