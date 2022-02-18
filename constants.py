"""Constants

This file contains various constants addressed in forming the visual and logical app structure.
Constants are grouped by type and use.
"""

import configparser
import serial

# File locations from config
config = configparser.ConfigParser()
config.read('config.ini')
config = config['default']

csv_folder = config['csv']
tmp116_csv = config['tmp116_csv']
hdc2010_temp_csv = config['hdc2010_temp_csv']
hdc2010_hum_csv = config['hdc2010_hum_csv']
opt3001_csv = config['opt3001_csv']
dps310_temp_csv = config['dps310_temp_csv']
dps310_pressure_csv = config['dps310_pressure_csv']

# Serial communication info
SERIAL_PORT = 'COM4'
serial = serial.Serial(SERIAL_PORT, 19200, timeout=1)

# Basic application info
headers = ['Vrijeme', 'Senzor', 'Velicina', 'Vrijednost']
MAX_ROWS = 100
NUM_OF_SENSORS = 6
LARGE_FONT = ("Verdana", 16)
APP_NAME = 'Centrala za upravljanje pametnim stanom'

# Coordinates arrays - allow element coordinates depend on number of elements in frame
graph_coords = [[100, 150], [650, 150]]
text_coords = [[100, 600], [100, 625]]
current_coords = [[100, 550], [100, 575]]

# String formation
temp_string = 'temperature'
temp_measurement = ' °C'
hum_string = 'vlažnosti zraka'
hum_measurement = '%'
light_string = 'razine svjetlosti'
light_measurement = ' lux'
pressure_string = 'atmosferskog tlaka'
pressure_measurement = 'Pa'

low_temp_msg = 'Hladno je. '
low_temp_tip = 'Upalite grijanje. '
normal_temp_msg = 'Temperatura je ugodna. '
high_temp_msg = 'Vruće je. '
high_temp_tip = 'Upalite hlađenje. '
low_hum_msg = 'Vlažnost zraka je niska. '

messages = {'low_temp': 'Hladno je. ',
            'low_temp_tip': 'Upalite grijanje. ',
            'normal_temp': 'Temperatura je ugodna. ',
            'high_temp': 'Vruće je. ',
            'high_temp_tip': 'Upalite hlađenje. ',
            'low_hum': 'Vlažnost zraka je niska. ',
            'low_hum_tip': 'Upalite ovlaživač zraka. ',
            'normal_hum': 'Vlažnost zraka je normalna.',
            'high_hum': 'Vlažnost zraka je visoka. ',
            'high_hum_tip': 'Pokušajte prozračiti prostoriju. ',
            'low_light': 'Premračno je. ',
            'low_light_tip': 'Otvorite škure ili upalite svjetlo. ',
            'normal_light': 'Razina svjetlosti je dobra. ',
            'high_light': 'Razina svjetlosti je visoka. ',
            'high_light_tip': 'Zamračite prostoriju. ',
            'low_pressure': 'Atmosferski tlak je nizak. ',
            'low_pressure_tip': 'Mogli biste očekivati kišno vrijeme. ',
            'normal pressure': 'Atmosferski tlak je ugodan. ',
            'high_pressure': 'Atmosferski tlak je visok. ',
            'high_pressure_tip': 'Vrijeme će biti vedro i suho. '}

messages_low = {key: messages[key]
                for key in ['low_temp', 'low_hum', 'low_light', 'low_pressure']}

messages_high = {key: messages[key]
                 for key in ['high_temp', 'high_hum', 'high_light', 'high_pressure']}

# Visual
colors = ['r', 'g', 'b']

# Indicators
TEMP_MIN = 17
TEMP_MAX = 25
HUM_MIN = 30
HUM_MAX = 60
LUX_MIN = 50
LUX_MAX = 900
PRES_MIN = 100000
PRES_MAX = 101400
