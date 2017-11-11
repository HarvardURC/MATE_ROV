/********************************************************
 * Reads in an input value from 0 to 1 and controls speed
 * Adapted from PID Basic Example found at
 * https://playground.arduino.cc/Code/PIDLibaryBasicExample
 ********************************************************/

#include <PID_v1.h>

// Library documentation found at https://playground.arduino.cc/Code/PIDLibrary
// Library must be downloaded using the Library Manager
// (see https://www.arduino.cc/en/Guide/Libraries#toc3)

// Define variables we'll be connecting to:
// set point is what we want the result to be
// input is what the current value is
// output is what the PID says our input to the motor should be

double setpoint, input, output;
// the values for the PID
// if we want to change these while running, we need to use SetTunings(newkp, newki, newkd)
double kp = 2;
double ki = 5;
double kd = 1;
double speed = 100;

// Specify the links and initial tuning parameters
PID myPID(&input, &output, &setpoint, kp, ki, kd, DIRECT);

void setup()
{
  // initialize the variables we're linked to
  input = getSpeedFromIMU();
  
  // the setpoint should be changed every once in a while once the joystick moves
  setpoint = getSpeedFromJoystick();

  // turn the PID on
  myPID.SetMode(AUTOMATIC);
}

void loop()
{
  input = getSpeedFromIMU();
  // changes the value of output
  myPID.Compute();
  analogWrite(motorPin,output);
}