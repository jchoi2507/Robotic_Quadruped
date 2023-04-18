/*
RP2040_node2.ino
By: Jacob Choi, David Zhang
Date: 4/18/2023

- Controls 4x servos on the quadruped's LEFT side
- Establishes serial connection between RPi and Arduino RP2040
- Checks for incoming messages, depending on the message, actuates
  one of 5 movements:
    'f': Forward
    's': Stop/stand still
    'l': Turn Left **
    'r': Turn Right **
    'd': Dance! **
*/

#include <Servo.h>

const unsigned int MAX_MESSAGE_BYTE_SIZE = 2; // 1 byte char & 1 terminating byte

Servo L1_1; // Left 1 Joint 1
Servo L1_2; // Left 1 Joint 2
Servo L2_1; // Left 2 Joint 1
Servo L2_2; // Left 2 Joint 2

/* Angle Arrays for Forward Movement */
int joint1_angles[60] = {37,36,37,38,40,41,42,42,42,41,39,38,36,35,33,32,30,29,27,26,24,22,20,18,15,12,8,5,2,0,0,2,3,5,6,8,9,10,12,13,15,16,17,18,20,21,22,24,25,26,27,28,29,31,32,33,34,35,36,37};
int joint2_angles[60] = {31,30,26,21,16,10,6,3,1,0,0,1,2,2,3,3,4,5,5,6,7,9,12,16,22,29,37,43,48,52,52,50,49,47,46,45,43,42,41,40,39,38,38,37,36,35,35,34,34,33,33,32,32,32,31,31,31,31,31,31};

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT); // For debugging: RP2040 board LED will flash when data is received
  L1_1.attach(6);
  L1_2.attach(7);
  L2_1.attach(8);
  L2_2.attach(9);
}

void loop() {
  if (Serial.available() > 0) {
    char read = Serial.read();
    if (read == '\n') {} // Terminating byte read, ignore current iteration
    else {
      actuateRobot(read);
    }
  }
}

void actuateRobot(char read) {
  switch(read) {
    case 'f':
      digitalWrite(LED_BUILTIN, HIGH); // Flash onboard LED to signal successful transmission
      moveForward();
      digitalWrite(LED_BUILTIN, LOW);
      break;
    case 's':
      digitalWrite(LED_BUILTIN, HIGH); // Flash onboard LED to signal successful transmission
      moveStop();
      digitalWrite(LED_BUILTIN, LOW);
      break;
    case 'l':
      moveLeft();
      break;
    case 'r':
      moveRight();
      break;
    case 'd':
      moveDance();
      break;
    default:
      break;
  }
}

void moveForward() {
  for (int i = 0; i < 60; i++){
    if (i >= 30) {
      L1_1.write(joint1_angles[i-30]);
      L1_2.write(joint2_angles[i-30]);
    }
    L2_1.write(joint1_angles[i]);
    L2_2.write(joint2_angles[i]);
    delay(15);
  }
  for (int j = 30; j < 60; j++) {
    L1_1.write(joint1_angles[j]);
    L1_2.write(joint2_angles[j]);
    delay(15);
  }
}

void moveStop() {
  L1_1.write(37);
  L1_2.write(31);
  L2_1.write(37);
  L2_2.write(31);
  delay(15);
}

void moveLeft() {}
void moveRight() {}
void moveDance() {}
