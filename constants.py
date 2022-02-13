import configparser

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

# Basic application info
headers = ['Vrijeme', 'Senzor', 'Velicina', 'Vrijednost']
MAX_ROWS = 100
NUM_OF_SENSORS = 6
LARGE_FONT = ("Verdana", 16)
APP_NAME = 'Centrala za upravljanje pametnim stanom'

# Coordinates arrays - allow element coordinates depend on number of elements in frame
graph_coords = [[100, 150], [650, 150]]
text_coords = [[100, 600], [100, 625]]

# String formation
temp_string = 'temperature'
temp_measurement = ' °C'
hum_string = 'vlažnosti zraka'
hum_measurement = '%'
light_string = 'razine svjetlosti'
light_measurement = ' lux'
pressure_string = 'atmosferskog tlaka'
pressure_measurement = 'Pa'

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
