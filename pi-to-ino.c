int x;
int y;
int z;
int roll;
int pitch;
int yaw;
int cameraTilt;
int cameraPan;

int vals[8];

// Serial data will come in this form: "x;y;z;roll;pitch;yaw;cameraTilt;cameraPan;\0"

boolean newData = false;

void setup() {
    Serial.begin(9600);
}

void loop() {
    recvWithEndMarker();
}

void recvWithEndMarker() {
    static byte ndx = 0;
    static byte inCtr = 0;
    char endMarker = '\0';
    char nextMarker = ';';
    char rc;
    char intBuf[32];

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc == nextMarker) {
            char* s = "";
            for (int i = 0; i < inCtr; i++) {
                s += intBuf[i];
            } 
            vals[ndx] = atoi(s);
            inCtr = 0;
            ndx++;
        }
        else if (rc != endMarker) {
            intBuf[inCtr] = rc;
            inCtr++;
        }
        else {
            ndx = 0;
            newData = true;
        }
    }

    translate();

}

void translate() {
    x = vals[0];
    y = vals[1];
    z = vals[2];
    roll = vals[3];
    pitch = vals[4];
    yaw = vals[5];
    cameraTilt = vals[6];
    cameraPan = vals[7];
}
