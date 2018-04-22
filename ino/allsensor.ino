
/*******************************************************************************************************
The code runs the DHT22, IMU, and Depth Sensor. The DHT22 needs the dht.h library to work. 
The DHT22 data pin (green) is connected to pin 4 (change dataPin to whatever the IMU is connected to). 
The Depth Sensor uses the MS5837.h library, the SCL(white) and SDA(green) of the Depth sensor are
connected to the Arduino SCL and SDA respectively.
The IMU needs the Adafruit_BNO055.h library, utility/imumaths.h, the IMU is connected to the SCL(white)
and SDA(green) of the Arduino.
Note: 1. Connect the SCL (white) wires from the IMU and Depth Sensor, then to the Arduino. 
      2. Connect the SDA (green) wires from the IMU and Depthe Sensor together then to the Arduino.
*********************************************************************************************************/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <DHT.h>
#include <dht.h>
#include "MS5837.h"

#define dataPin 4
dht DHT;

Adafruit_BNO055 bno = Adafruit_BNO055(55);
MS5837 sensor;

void setup() {
  Serial.begin(9600);
  Serial.println("Starting");
  Wire.begin();

  // initialize the Depth Sensor
  sensor.init();
  sensor.setFluidDensity(997); // kg/m^3 (997 freshwater, 1029 for seawater)

  //initialize the IMU sensor
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  delay(1000);
    
  bno.setExtCrystalUse(true);
}

void loop() {
  /* Data from IMU */ 
  sensors_event_t event; 
  bno.getEvent(&event);
  
  /* Display the floating point data */
  Serial.print("X: ");
  Serial.print(event.orientation.x, 4);
  Serial.print("\tY: ");
  Serial.print(event.orientation.y, 4);
  Serial.print("\tZ: ");
  Serial.print(event.orientation.z, 4);
  Serial.println("");
  
  //Data from the Depth Sensor
  sensor.read();
  Serial.print("Pressure: "); 
  Serial.print(sensor.pressure()); 
  Serial.println(" mbar");
  
  Serial.print("Temperature: "); 
  Serial.print(sensor.temperature()); 
  Serial.println(" deg C");
  
  Serial.print("Depth: "); 
  Serial.print(sensor.depth()); 
  Serial.println(" m");
  
  Serial.print("Altitude: "); 
  Serial.print(sensor.altitude()); 
  Serial.println(" m above mean sea level");

  // DHT Sensor
  int readData = DHT.read22(dataPin); // Reads the data from the sensor
  float t = DHT.temperature; // Gets the values of the temperature
  float h = DHT.humidity; // Gets the values of the humidity
  
  // Printing the results on the serial monitor
  Serial.print("Temperature = ");
  Serial.print(t);
  Serial.print(" *C ");
  Serial.print("    Humidity = ");
  Serial.print(h);
  Serial.println(" % ");
  
  delay(2000);
}
