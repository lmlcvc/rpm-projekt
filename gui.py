import configparser
import os
import threading
import time
import tkinter as tk
from datetime import datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")

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
LARGE_FONT = ("Verdana", 12)
APP_NAME = 'Centrala za upravljanje pametnim stanom'


def create_folder():
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)


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
    return figure


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


class TMP116Page(tk.Frame):

    def update_plots(self):
        figure = make_plots(tmp116_csv)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=150)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="TMP 116", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(StartPage))
        button.pack()

        TMP116Page.update_plots(self)

        button_update = tk.Button(self, text="Ažuriraj", command=lambda: TMP116Page.update_plots(self))
        button_update.place(x=100, y=20)


class HDC2010Page(tk.Frame):

    def update_plots(self):
        figure = make_plots(hdc2010_temp_csv)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=150)

        figure = make_plots(hdc2010_hum_csv)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=650, y=150)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="HDC 2010", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(StartPage))
        button.pack()

        HDC2010Page.update_plots(self)

        button_update = tk.Button(self, text="Ažuriraj", command=lambda: HDC2010Page.update_plots(self))
        button_update.place(x=100, y=20)


class OPT3001Page(tk.Frame):

    def update_plots(self):
        figure = make_plots(opt3001_csv)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=150)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="OPT3001", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(StartPage))
        button.pack()

        OPT3001Page.update_plots(self)

        button_update = tk.Button(self, text="Ažuriraj", command=lambda: OPT3001Page.update_plots(self))
        button_update.place(x=100, y=20)


class DPS301Page(tk.Frame):

    def update_plots(self):
        figure = make_plots(dps310_temp_csv)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=150)

        figure = make_plots(dps310_pressure_csv)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=650, y=150)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="DPS301", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(StartPage))
        button.pack()

        DPS301Page.update_plots(self)

        button_update = tk.Button(self, text="Ažuriraj", command=lambda: DPS301Page.update_plots(self))
        button_update.place(x=100, y=20)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        # tmp_page = TMP116Page(self)

        button_tmp = tk.Button(self, text="TMP116 očitanja", command=lambda: controller.show_frame(TMP116Page))
        button_tmp.pack()

        button_hdc = tk.Button(self, text="HDC2010 očitanja", command=lambda: controller.show_frame(HDC2010Page))
        button_hdc.pack()

        button_opt = tk.Button(self, text="OPT3001 očitanja", command=lambda: controller.show_frame(OPT3001Page))
        button_opt.pack()

        button_dps = tk.Button(self, text="DPS301 očitanja", command=lambda: controller.show_frame(DPS301Page))
        button_dps.pack()


class SensorCentral(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, APP_NAME)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in [StartPage, TMP116Page, HDC2010Page, OPT3001Page, DPS301Page]:
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def thread_gui():
    app = SensorCentral()
    # app.after(1, store_to_csv())
    app.mainloop()


if __name__ == '__main__':
    serial = serial.Serial('COM4', 19200, timeout=1)
    serial.reset_input_buffer()
    time.sleep(2)
    threading.Thread(target=thread_gui).start()
    # thread.start_new_thread(thread_gui(), ())

    while 1:
        store_to_csv()
        time.sleep(1)
