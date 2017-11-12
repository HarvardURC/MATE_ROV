#include <Wire.h>
#include "MS5837.h"

MS5837 sensor;

void setup() {
  
  Serial.begin(9600)
  
  Wire.begin();
  
  sensor.init();
  // Set the density of the working fluid to freshwater
  sensor.setModel(997); 
}

void loop() {

  sensor.read();
  // put your main code here, to run repeatedly:
  float pressure = sensor.pressure();
  float temperature = sensor.temperature();
  float depth = sensor.depth();
  float altitude = sensor.altitude();

  Serial.println(pressure);
  Serial.println(temperature);
  Serial.println(depth);
  Serial.println(altitude);
}
