import serial
import time
from datetime import datetime
import configparser
import matplotlib.pyplot as plt
import pandas as pd
import os

config = configparser.ConfigParser()
config.read('config.ini')
config = config['default']

# directory = config['transformed_location']
csv = config['csv']
tmp116_csv = config['tmp116_csv']
hdc2010_temp_csv = config['hdc2010_temp_csv']
hdc2010_hum_csv = config['hdc2010_hum_csv']

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM4', 19200, timeout=1)
time.sleep(2)

headers = ['Vrijeme', 'Senzor', 'Velicina', 'Vrijednost']


def create_folder():
    if not os.path.exists(csv):
        os.makedirs(csv)


def store_to_csv():
    with open(tmp116_csv, 'a') as tmp116_file, open(hdc2010_temp_csv, 'a') as hdc2010_temp_file, \
            open(hdc2010_hum_csv, 'a') as hdc2010_hum_file:
        for i in range(60):
            line = ser.readline()  # read a byte string

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
                else:
                    print('Wrong sensor name value')

                print(string)


# TODO: nazivi datoteka, mjerne jedinice itd., nije tragedija
def make_plots():
    for filename in os.listdir(csv):
        with open(os.path.join(csv, filename), 'r') as f:
            df = pd.read_csv(f, names=headers)
            print(df)

            x = df['Vrijeme']
            y = df['Vrijednost']

            # plot
            plt.plot(x, y)
            # beautify the x-labels
            plt.gcf().autofmt_xdate()

            plt.show()


if __name__ == "__main__":
    create_folder()

    store_to_csv() # TODO: promijeniti logiku da se stalno vrti
    ser.close()

    make_plots()
