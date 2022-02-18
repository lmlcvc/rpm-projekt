# Smart Home Sensor Central

### Project Description
This program represents a central for managing a smart home based on various sensor readings.
From the user's perspective, it is run as a GUI representing real-time sensor readings and their meaning. \
All readings are gotten through I2C communication with an Arduino Micro device 
connected to a BOOSTXL-BASSENSORS (sensors TMP116, HDC2010, OPT3001) and a DPS301 board.  \
\
The wiring scheme for this setup is provided in `wiring-scheme.png`.\
\
Sensor readings are stored in csv format and used as such throughout the program.


### Project structure and usage
##### arduino/projekt/projekt.ino
The arduino code used for reading all 4 sensors' data. Before running `gui.py`, this
code should be up and running on your Arduino board. \
All code in `projekt.ino` is constructed using examples and libraries mentioned in
`arduino/disclaimer.md`.

##### config.ini *(set up before running)*
The `config.ini` file stores the locations of folders used in running this program.
You should match the paths in `config.ini` to the paths in your computer where you want to store those items.
* `csv` - the folder you want to store CSVs in
* `sensorName_sensorValue_csv` - csv files for respective sensors and their values
* `serial_port` - the port your Arduino device is connected to (e.g. COM4)

##### gui.py
This file runs the entire program. To do so, it makes use of multithreading.
* One thread is the main one, which constantly listens to the serial port and
stores values communicated through it accordingly.
* The other one starts and runs the gui, and makes sure it updates every 10 seconds.

##### constants.py
##### file_handler.py
##### pages.py
##### element_constructor.py