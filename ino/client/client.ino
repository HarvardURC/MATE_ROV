#include <Wire.h>
#include <Servo.h> 
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define TICKS_PER_WRITE 200

#define PANSERVO 2
#define TILTSERVO 3
#define T1 4
#define T2 5
#define T3 6
#define T4 7
#define T5 8
#define T6 9

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

Adafruit_BNO055 bno = Adafruit_BNO055(55);
int ticks = 0;

Servo panServo;
Servo tiltServo;

Servo thrusters[6];

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
    panServo.attach(PANSERVO);
    tiltServo.attach(TILTSERVO);

    // initialize thrusters
    thrusters[0].attach(T1);
    thrusters[1].attach(T1);
    thrusters[2].attach(T1);
    thrusters[3].attach(T1);
    thrusters[4].attach(T1);
    thrusters[5].attach(T1);
    
    thrusters[0].writeMicroseconds(1500);
    thrusters[1].writeMicroseconds(1500);
    thrusters[2].writeMicroseconds(1500);
    thrusters[3].writeMicroseconds(1500);
    thrusters[4].writeMicroseconds(1500);
    thrusters[5].writeMicroseconds(1500);
    
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
    Serial.print(';');
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
        if(Serial.available() == 0) {
            return 0;
        }
    }

    while (field < 8) {
        while(Serial.available() == 0);
        inChr = Serial.read();
        if ((char)inChr == ';') {
            inString += '\0';
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
            inString += (char) inChr;
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

    /* Sample: Turn all thrusters on. value has to be in between 1100 and 1900
    thrusters[0].writeMicroseconds(1700);
    thrusters[1].writeMicroseconds(1700);
    thrusters[2].writeMicroseconds(1700);
    thrusters[3].writeMicroseconds(1700);
    thrusters[4].writeMicroseconds(1700);
    thrusters[5].writeMicroseconds(1700); */
    
    if (ticks % TICKS_PER_WRITE == 0) {
        //print_orientation(event);
    }
    // read from Serial
    if (read_message(&curMsg)) {
        if (curMsg.cameraTilt > 0) {
            tiltPos+= 10;
        } else if (curMsg.cameraTilt < 0) {
            tiltPos-= 10;
        }
        if (tiltPos > 360) {
            tiltPos = 360;
        } else if (tiltPos < -180) {
            tiltPos = -180;
        }
        
        if (curMsg.cameraPan > 0) {
            panPos+= 10;
        } else if (curMsg.cameraPan < 0) {
            panPos-= 10;
        }
        if (panPos > 360) {
            panPos = 360;
        } else if (panPos < -180) {
            panPos = -180;
        }
  
    }
    Serial.print(panPos);
    Serial.print(" ");
    Serial.println(tiltPos);
    panServo.writeMicroseconds(1100 + panPos*5);
    //tiltServo.write(tiltPos);
    delay(500);
    ticks++;
}
