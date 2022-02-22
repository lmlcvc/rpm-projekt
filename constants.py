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
BUFFER_MINUTES = 10
NUM_OF_SENSORS = 6
LARGE_FONT = ("Verdana", 16)
MID_FONT = ("Verdana", 11)
APP_NAME = 'Centrala za upravljanje pametnim stanom'
START_NAME = 'Početna stranica'
ICON_PATH = uconfig['icon_path']
PRESSURE_INTERVAL_SECS = 10
PRESSURE_DIFF_PA = 5

# Coordinates arrays - allow element coordinates depend on number of elements in frame
graph_coords = [[100, 150], [650, 150]]
text_coords = [[100, 650], [700, 650]]
current_coords = [[100, 675], [700, 675]]
start_text_coords = {'x': 1125, 'y': 400}
period_coords = {'x': 1125, 'y': 200}
period_sensorpage_coords = {'x': 550, 'y': 100}
button_update_coords = {'x': 170, 'y': 70}
button_back_coords = {'x': 100, 'y': 70}

# Graph formation
temp_name = 'Temperatura'
hum_name = 'Vlažnost zraka'
light_name = 'Svjetlina'
pressure_name = 'Atmosferski tlak'

# Measurement formation
temp_measurement = ' °C'
hum_measurement = '%'
light_measurement = ' lux'
pressure_measurement = ' Pa'

# String formation
temp_string = 'temperature'
hum_string = 'vlažnosti zraka'
light_string = 'razine svjetlosti'
pressure_string = 'atmosferskog tlaka'

low_temp_msg = 'Hladno je. '
low_temp_tip = 'Upalite grijanje. '
normal_temp_msg = 'Temperatura je ugodna. '
high_temp_msg = 'Vruće je. '
high_temp_tip = 'Upalite hlađenje. '
low_hum_msg = 'Vlažnost zraka je niska. '

messages = {'low_temp': 'Hladno je. ',
            'low_temp_tip': '\u26A0 Upalite grijanje. ',
            'normal_temp': 'Temperatura je ugodna. ',
            'high_temp': 'Vruće je. ',
            'high_temp_tip': '\u26A0 Upalite hlađenje. ',
            'low_hum': 'Vlažnost zraka je niska. ',
            'low_hum_tip': '\u26A0 Upalite ovlaživač zraka. ',
            'normal_hum': 'Vlažnost zraka je normalna.',
            'high_hum': 'Vlažnost zraka je visoka. ',
            'high_hum_tip': '\u26A0 Pokušajte prozračiti prostoriju. ',
            'low_light': 'Premračno je. ',
            'low_light_tip': '\u26A0 Otvorite škure ili upalite svjetlo. ',
            'normal_light': 'Razina svjetlosti je dobra. ',
            'high_light': 'Razina svjetlosti možda je previsoka. ',
            'high_light_tip': '\u26A0 Zamračite prostoriju. ',
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
