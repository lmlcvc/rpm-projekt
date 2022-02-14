#include <Wire.h>
#include <ClosedCube_OPT3001.h>
#include "ClosedCube_TMP116.h"
#include <sSense-HDC2010.h>
#include <Dps310.h>

#define OPT3001_ADDRESS 0x44

ClosedCube::Sensor::TMP116 tmp116;
HDC2010 ssenseHDC2010(HDC2010_I2C_ADDR);
ClosedCube_OPT3001 opt3001;
Dps310 Dps310PressureSensor = Dps310();

float TMP_temperature = 0, HDC_temperature = 0, HDC_humidity = 0, OPT_lux = 0, DPS_temperature = 0, DPS_pressure = 0;

void setup() {
	Wire.begin();
	Serial.begin(19200);
  while(!Serial);

    // TMP116 init	
	tmp116.address(0x48); // Sensor I2C address either 0x48 or x49

  //////////

    // HDC2010 init
  delay(1000);
  
  ssenseHDC2010.begin(); // Initialize HDC2010(THS) I2C communication
  ssenseHDC2010.reset(); // Begin with a HDC2010(THS) reset
  // Set up HDC2010(THS) temperature offset, if required
  //ssenseHDC2010.setTemperatureOffset(0b11010111);    //-6.64 degrees Celsius - determine and set your, see definitions and HDC2010 datasheet
 
  // Configure Measurements
  ssenseHDC2010.setMeasurementMode(TEMP_AND_HUMID);  // Set measurements to temperature and humidity
  ssenseHDC2010.setRate(ONE_HZ);                     // Set measurement frequency to 1 Hz
  ssenseHDC2010.setTempRes(FOURTEEN_BIT);
  ssenseHDC2010.setHumidRes(FOURTEEN_BIT);

  delay(1000);

  //begin HDC2010 sensor measuring
  ssenseHDC2010.triggerMeasurement();

  //////////

    // OPT3001 init
  opt3001.begin(OPT3001_ADDRESS);
  delay(500);
  configureSensor();

  //////////

    // DPS310 I2C init
  Dps310PressureSensor.begin(Wire);
}

void loop() {
  TMP_temperature = tmp116.readTemperature();
  Serial.print("TMP116, temperature, ");
  Serial.println(TMP_temperature);
	/*Serial.print("TMP116 temperature: ");
	Serial.print(TMP_temperature);
	Serial.println(" °C");*/

	delay(50);

  //////////

  HDC_temperature = ssenseHDC2010.readTemp();
  HDC_humidity = ssenseHDC2010.readHumidity();

  Serial.print("HDC2010, temperature, ");
  Serial.println(HDC_temperature);

  Serial.print("HDC2010, humidity, ");
  Serial.println(HDC_humidity);

  delay(50);

  //////////
  
  OPT_lux = opt3001.readResult().lux;
  Serial.print("OPT3001, light, ");
  Serial.println(OPT_lux);

  delay(50);

  //////////

  uint8_t oversampling = 7;
  int16_t ret;

  ret = Dps310PressureSensor.measureTempOnce(DPS_temperature, oversampling);

  if (ret != 0) {
    //Something went wrong.
    //Look at the library code for more information about return codes
    Serial.print("FAIL! ret = ");
    Serial.println(ret);
  }
  else {
    Serial.print("DPS310, temperature, ");
    Serial.println(DPS_temperature);
  }

  //Pressure measurement behaves like temperature measurement
  //ret = Dps310PressureSensor.measurePressureOnce(pressure);
  ret = Dps310PressureSensor.measurePressureOnce(DPS_pressure, oversampling);
  if (ret != 0) {
    //Something went wrong.
    //Look at the library code for more information about return codes
    Serial.print("FAIL! ret = ");
    Serial.println(ret);
  }
  else {
    Serial.print("DPS310, pressure, ");
    Serial.println(DPS_pressure);
  }


  delay(2000);
}

void configureSensor() {
  OPT3001_Config newConfig;
  
  newConfig.RangeNumber = B1100;  
  newConfig.ConvertionTime = B0;
  newConfig.Latch = B1;
  newConfig.ModeOfConversionOperation = B11;

  OPT3001_ErrorCode errorConfig = opt3001.writeConfig(newConfig);
}
