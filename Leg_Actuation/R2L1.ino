#include <Servo.h>

Servo servoR1_1;  // create servo object to control a servo
Servo servoR1_2;
Servo servoR2_1;
Servo servoR2_2;
Servo servoL1_1;
Servo servoL1_2;
Servo servoL2_1;
Servo servoL2_2;
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int angle1R[60] = {143,144,143,142,140,139,138,138,138,139,141,142,144,145,147,148,150,151,153,154,156,158,160,162,165,168,172,175,178,180,180,178,177,175,174,172,171,170,168,167,165,164,163,162,160,159,158,156,155,154,153,152,151,149,148,147,146,145,144,143
};
int angle2R[60] = {149,150,154,159,164,170,174,177,179,180,180,179,178,178,177,177,176,175,175,174,173,171,168,164,158,151,143,137,132,128,128,130,131,133,134,135,137,138,139,140,141,142,142,143,144,145,145,146,146,147,147,148,148,148,149,149,149,149,149,149
};
int angle1L[60] = {37,36,37,38,40,41,42,42,42,41,39,38,36,35,33,32,30,29,27,26,24,22,20,18,15,12,8,5,2,0,0,2,3,5,6,8,9,10,12,13,15,16,17,18,20,21,22,24,25,26,27,28,29,31,32,33,34,35,36,37
};
int angle2L[60] = {31,30,26,21,16,10,6,3,1,0,0,1,2,2,3,3,4,5,5,6,7,9,12,16,22,29,37,43,48,52,52,50,49,47,46,45,43,42,41,40,39,38,38,37,36,35,35,34,34,33,33,32,32,32,31,31,31,31,31,31
};

void setup() {
  servoR2_1.attach(8);
  servoR2_2.attach(9);
  servoL1_1.attach(10);
  servoL1_2.attach(11);
}

void loop() {

// R2&L1
  for (int i = 0; i < 60; i++){
    servoR2_1.write(angle1R[i]);
    servoR2_2.write(angle2R[i]);
    servoL1_1.write(angle1L[i]);
    servoL1_2.write(angle2L[i]);
    delay(15);
  }

// // Reseting legs
//   servoR1_1.write(143);
//   servoR1_2.write(149);
//   servoR2_1.write(143);
//   servoR2_2.write(149);
//   servoL1_1.write(37);
//   servoL1_2.write(31);
//   servoL2_1.write(37);
//   servoL2_2.write(31);
}
