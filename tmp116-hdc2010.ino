#include "ClosedCube_TMP116.h"
#include <sSense-HDC2010.h>

ClosedCube::Sensor::TMP116 tmp116;
HDC2010 ssenseHDC2010(HDC2010_I2C_ADDR);

float TMP_temperature = 0, HDC_temperature = 0, HDC_humidity = 0;

void setup() {
	Wire.begin();
	Serial.begin(19200);

    // TMP116 init
  delay(100);
	
	tmp116.address(0x48); // Sensor I2C address either 0x48 or x49

	Serial.print("Device ID: 0x");
	Serial.println(tmp116.readDeviceId(), HEX); // Device ID = 0x116	

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

  /*Serial.print("HDC2010 temperature: ");
  Serial.print(HDC_temperature);
  Serial.println(" °C");

  Serial.print("HDC2010 %RH: ");
  Serial.println(HDC_humidity);*/
  
  // Wait 2 second for the next reading
  delay(2000);
}
