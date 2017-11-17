#include <Wire.h>
#include <Servo.h> 
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define TICKS_PER_WRITE 200

struct message {
    float x;
    float y;
    float z;
    float roll;
    float pitch;
    float yaw;
    float cameraTilt;
    float cameraPan;
};

//Adafruit_BNO055 bno = Adafruit_BNO055(55);
int ticks = 0;

Servo panServo;
Servo tiltServo;
int panPos = 90;
int tiltPos = 90;

struct message curMsg;

void setup(void)
{
    Serial.begin(9600);
  
    // Initialise the IMU 
    if(!bno.begin()) {
        Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
        while(1);
    }
  
    // initialize servos
    panServo.attach(2, 800, 2200);
    tiltServo.attach(10, 800, 2200);
    
    delay(1000);
  
    bno.setExtCrystalUse(true);
}

void print_orientation(sensors_event_t event) {
    Serial.print('$');
    Serial.print(event.orientation.x);
    Serial.print(';');
    Serial.print(event.orientation.y);
    Serial.print(';');
    Serial.print(event.orientation.z);
    Serial.print('\n');
}

int read_message(struct message *msg) {
    if (Serial.available() == 0) {
        return 0;
    }
    int field = 0;
    int inChr;
    String inString = "";
    // Find start
    while(true) {
        inChr = Serial.read();
        if ((char)inChr == '$') {
            break;
        }
    }

    while (field < 8) {
        inChr = Serial.read();
        if ((char)inChr == ';') {
            switch(field) {
                case 0:
                    msg->x = inString.toFloat();
                    break;
                case 1:
                    msg->y = inString.toFloat();
                    break;
                case 2:
                    msg->z = inString.toFloat();
                    break;
                case 3:
                    msg->roll = inString.toFloat();
                    break;
                case 4:
                    msg->pitch = inString.toFloat();
                    break;
                case 5:
                    msg->yaw = inString.toFloat();
                    break;
                case 6:
                    msg->cameraTilt = inString.toFloat();
                    break;
                case 7:
                    msg->cameraPan = inString.toFloat();
                    break;
            }
            field++;
            inString = "";
        } else {
            inString += char(inChr);
        }
    }
    return 1;
}

void loop(void)
{
    // get sensor event
    sensors_event_t event;
    bno.getEvent(&event);
  
    // TODO: run PID
    
    
    if (ticks % TICKS_PER_WRITE == 0) {
        print_orientation(event);
    }
    
    // read from Serial
    if (read_message(&curMsg)) {
        if (curMsg.cameraTilt > 0) {
            tiltPos++;
        } else if (curMsg.cameraTilt < 0) {
            tiltPos--;
        }
        if (tiltPos > 180) {
            tiltPos = 180;
        } else if (tiltPos < 0) {
            tiltPos = 0;
        }
        
        if (curMsg.cameraPan > 0) {
            panPos++;
        } else if (curMsg.cameraPan < 0) {
            panPos--;
        }
        if (panPos > 180) {
            panPos = 180;
        } else if (panPos < 0) {
            panPos = 0;
        }
  
    }
    panServo.write(panPos);
    tiltServo.write(panPos);
    ticks++;
}