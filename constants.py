"""Constants

This file contains various constants addressed in forming the visual and logical app structure.
Constants are grouped by type and use.
"""

import configparser
import serial

# File locations from config
configp = configparser.ConfigParser()
configp.read('config.ini')
config = configp['default']
uconfig = configp['updatable']

csv_folder = config['csv']
tmp116_csv = config['tmp116_csv']
hdc2010_temp_csv = config['hdc2010_temp_csv']
hdc2010_hum_csv = config['hdc2010_hum_csv']
opt3001_csv = config['opt3001_csv']
dps310_temp_csv = config['dps310_temp_csv']
dps310_pressure_csv = config['dps310_pressure_csv']

# Serial communication info
SERIAL_PORT = uconfig['serial_port']
try:
    serial = serial.Serial(SERIAL_PORT, 19200, timeout=1)
except serial.serialutil.SerialException:
    pass

# Basic application info
headers = ['Vrijeme', 'Senzor', 'Velicina', 'Vrijednost']
MAX_ROWS = 100
MAX_ROWS_OPT_PRES = 500
NUM_OF_SENSORS = 6
LARGE_FONT = ("Verdana", 16)
APP_NAME = 'Centrala za upravljanje pametnim stanom'
ICON_PATH = uconfig['icon_path']

# Coordinates arrays - allow element coordinates depend on number of elements in frame
graph_coords = [[100, 150], [650, 150]]
text_coords = [[100, 600], [100, 625]]
current_coords = [[100, 650], [100, 675]]

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
            'normal_pressure': 'Atmosferski tlak je ugodan. ',
            'high_pressure': 'Atmosferski tlak je visok. ',
            'high_pressure_tip': 'Vrijeme će biti vedro i suho. '}

messages_low = {key: messages[key]
                for key in ['low_temp', 'low_hum', 'low_light', 'low_pressure']}

messages_high = {key: messages[key]
                 for key in ['high_temp', 'high_hum', 'high_light', 'high_pressure']}

# Visual
colors = ['r', 'g', 'b', 'deepskyblue', 'orange', 'darkorchid']


# Indicators
TEMP_MIN = float(uconfig['temp_min'])
TEMP_MAX = float(uconfig['temp_max'])
HUM_MIN = float(uconfig['hum_min'])
HUM_MAX = float(uconfig['hum_max'])
LUX_MIN = float(uconfig['lux_min'])
LUX_MAX = float(uconfig['lux_max'])
PRES_MIN = float(uconfig['pres_min'])
PRES_MAX = float(uconfig['pres_max'])
