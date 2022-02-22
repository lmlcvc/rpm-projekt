#include <Wire.h>
#include <ClosedCube_OPT3001.h>
#include "ClosedCube_TMP116.h"
#include <sSense-HDC2010.h>
#include <Dps310.h>

#define OPT3001_ADDRESS 0x44

#define PERIOD_TEMP 10
#define PERIOD_HUM 10
#define PERIOD_LUX 0.5
#define PERIOD_PRES 0.5

ClosedCube::Sensor::TMP116 tmp116;
HDC2010 ssenseHDC2010(HDC2010_I2C_ADDR);
ClosedCube_OPT3001 opt3001;
Dps310 Dps310PressureSensor = Dps310();

float TMP_temperature = 0, HDC_temperature = 0, HDC_humidity = 0, OPT_lux = 0, DPS_temperature = 0, DPS_pressure = 0;
int16_t DPS_ret = 0;
uint8_t oversampling = 7;
unsigned long int temp_duration = 0, hum_duration = 0, lux_duration = 0, press_duration = 0;

void setup() {
	Wire.begin();
	Serial.begin(19200);
  while(!Serial);

    // TMP116 init
	tmp116.address(0x48); // Sensor I2C address either 0x48 or x49

  //////////

    // HDC2010 init
  delay(10);

  ssenseHDC2010.begin(); // Initialize HDC2010(THS) I2C communication
  ssenseHDC2010.reset(); // Begin with a HDC2010(THS) reset
  // Set up HDC2010(THS) temperature offset, if required
  //ssenseHDC2010.setTemperatureOffset(0b11010111);    //-6.64 degrees Celsius - determine and set your, see definitions and HDC2010 datasheet

  // Configure Measurements
  ssenseHDC2010.setMeasurementMode(TEMP_AND_HUMID);  // Set measurements to temperature and humidity
  ssenseHDC2010.setRate(TWO_HZ);                     // Set measurement frequency to 2 Hz
  ssenseHDC2010.setTempRes(FOURTEEN_BIT);
  ssenseHDC2010.setHumidRes(FOURTEEN_BIT);

  delay(10);

  //begin HDC2010 sensor measuring
  ssenseHDC2010.triggerMeasurement();

  //////////

    // OPT3001 init
  opt3001.begin(OPT3001_ADDRESS);
  delay(10);
  configureSensor();

  //////////

    // DPS310 I2C init
  Dps310PressureSensor.begin(Wire);
}

void loop() {
  if (lux_duration > millis()) {
    lux_duration = 0;
    press_duration = 0;
    temp_duration = 0;
    hum_duration = 0;
  }

  // Temperature
  if (millis() - temp_duration >= (PERIOD_TEMP * 1000)) {  // check if (PERIOD_TEMP * 1000) milliseconds have passed
    temp_duration = millis();

    // trigger all temperature readings and send to serial

    // TMP116
    TMP_temperature = tmp116.readTemperature();
    Serial.print("TMP116, temperature, ");
    Serial.println(TMP_temperature);

    // HDC2010
    HDC_temperature = ssenseHDC2010.readTemp();
    Serial.print("HDC2010, temperature, ");
    Serial.println(HDC_temperature);

    // DPS310
    DPS_ret = Dps310PressureSensor.measureTempOnce(DPS_temperature, oversampling);

    if (DPS_ret != 0) {
      //Something went wrong.
      //Look at the library code for more information about return codes
      Serial.print("FAIL! ret = ");
      Serial.println(DPS_ret);
    }
    else {
      Serial.print("DPS310, temperature, ");
      Serial.println(DPS_temperature);
    }
  }

  // Humidity
  if (millis() - hum_duration >= (PERIOD_HUM * 1000)) {
    hum_duration = millis();

    HDC_humidity = ssenseHDC2010.readHumidity();
    Serial.print("HDC2010, humidity, ");
    Serial.println(HDC_humidity);
    }

  // Light
  if (millis() - lux_duration >= (PERIOD_LUX * 1000)) {
    lux_duration = millis();

    OPT_lux = opt3001.readResult().lux;
    Serial.print("OPT3001, light, ");
    Serial.println(OPT_lux);
  }

  // Pressure
  if (millis() - press_duration >= (PERIOD_PRES * 1000)) {
    press_duration = millis();

    DPS_ret = Dps310PressureSensor.measurePressureOnce(DPS_pressure, oversampling);
    if (DPS_ret != 0) {
      //Something went wrong.
      //Look at the library code for more information about return codes
      Serial.print("FAIL! ret = ");
      Serial.println(DPS_ret);
    }
    else {
      Serial.print("DPS310, pressure, ");
      Serial.println(DPS_pressure);
    }
    }
}

void configureSensor() {
  OPT3001_Config newConfig;

  newConfig.RangeNumber = B1100;
  newConfig.ConvertionTime = B0;
  newConfig.Latch = B1;
  newConfig.ModeOfConversionOperation = B11;

  OPT3001_ErrorCode errorConfig = opt3001.writeConfig(newConfig);
}