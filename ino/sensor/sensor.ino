#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define TICKS_PER_WRITE 200

Adafruit_BNO055 bno = Adafruit_BNO055(55);
int ticks = 0;

void setup(void)
{
  Serial.begin(9600);

  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);

  bno.setExtCrystalUse(true);
}

void print_orientation(sensors_event_t event) {
  Serial.write('$');
  Serial.write(event.orientation.x);
  Serial.write(';');
  Serial.write(event.orientation.y);
  Serial.write(';');
  Serial.write(event.orientation.z);
  Serial.write('\n');
}

void loop(void)
{
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);
  if (ticks % TICKS_PER_WRITE == 0) {
    print_orientation(event);
  }
  ticks++;
}
