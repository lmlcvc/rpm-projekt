# Smart Home Sensor Central

## Project Description
This program represents a central for managing a smart home based on various sensor readings.
From the user's perspective, it is run as a GUI representing real-time sensor readings and their meaning. \
All readings are gotten through I2C communication with an Arduino Micro device 
connected to a BOOSTXL-BASSENSORS (sensors TMP116, HDC2010, OPT3001) and a DPS301 board.  \

This program represents a central for managing a smart home based on various sensor readings. From the user's
perspective, it is run as a GUI representing real-time sensor readings and their meaning. \
All readings are gotten through I2C communication with an Arduino Micro device connected to a BOOSTXL-BASSENSORS (
sensors TMP116, HDC2010, OPT3001) and a DPS301 board.  \
\
The wiring scheme for this setup is provided in `wiring-scheme.png`.\
\
Sensor readings are stored in csv format and used as such throughout the program.

## Installing and running

1. Download all contents of this repository to your device.
2. Open arduino IDE and include all libraries in `/arduino/libraries` to your project.
3. Run the arduino code (make sure serial port is not occupied by Serial Monitor/Serial Plotter because the python
   program will not be able to listen to it).
4. Run and use the python gui by calling `python gui.py` or simply running the main method. \
   \
   For optimal performance, do not tamper with the files in your `csv` folder yourself and let the program do all the
   work.

## Using the app

* When the app is first started, you will see a start page with graphed sensor readings throughout the last 10 minutes,
  listed average values in the last minute, and other information.
* From there, you can access 4 pages, for each of the sensors. This lets you focus on just one sensor more easily and
  view its readings in higher detail on a bigger graph.
* You can update all pages of this app manually by clicking the update button at any time ("Ažuriraj").
* The start page is automatically updated every 10 seconds.

## Project structure

##### arduino/projekt/projekt.ino
The arduino code used for reading all 4 sensors' data. Before running `gui.py`, this
code should be up and running on your Arduino board. \

The arduino code used for reading all 4 sensors' data. Before running `gui.py`, this code should be up and running on
your Arduino board. \
All code in `projekt.ino` is constructed using examples and libraries mentioned in
`arduino/disclaimer.md`.

##### config.ini *(set up before running)*
The `config.ini` file stores the locations of folders used in running this program.
You should match the paths in `config.ini` to the paths in your computer where you want to store those items.

The `config.ini` file stores the locations of folders used in running this program. You should match the paths
in `config.ini` to the paths in your computer where you want to store those items.

* `csv` - the folder you want to store CSVs in
* `sensorName_sensorValue_csv` - csv files for respective sensors and their values
* `serial_port` - the port your Arduino device is connected to (e.g. COM4)

##### gui.py

This file runs the entire program. To do so, it makes use of multithreading.
* One thread is the main one, which constantly listens to the serial port and
stores values communicated through it accordingly.

* One thread is the main one, which constantly listens to the serial port and stores values communicated through it
  accordingly.
* The other one starts and runs the gui, and makes sure it updates every 10 seconds.

##### constants.py
This file stores all the constants used throughout the program, and 
allows for their easier modification. The constants are grouped by function.\

This file stores all the constants used throughout the program, and allows for their easier modification. The constants
are grouped by function.\
If changing anything in the code, you should do it through `constants.py`
rather than by directly putting numbers and strings into the code.

##### file_handler.py
Here you can find methods used for modifying csv files the project works with and 
the directory they are stored in. App updatability and other runtime functionalities
rely heavily on data accessed and modified through this module.

Here you can find methods used for modifying csv files the project works with and the directory they are stored in. App
updatability and other runtime functionalities rely heavily on data accessed and modified through this module.

##### pages.py

This is a file that declares the classes for all pages in the app.

* `StartPage` - the main page in the app and its starting point
* `SensorPage` (its child classes) - define pages for each of the sensors in this setup
* `UpdatePage` - page for desired values range and serial port configuration

##### element_constructor.py

Various tkinter on the pages are constructed and modified by using this module's methods.


## Credits

All code in `/arduino/` is constructed using the help of libraries and examples mentioned
in [disclaimer](/arduino/disclaimer.md).
