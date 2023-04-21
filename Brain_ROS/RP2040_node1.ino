/*
RP2040_node1.ino
By: Jacob Choi, David Zhang
Date: 4/15/2023

- Controls 4x servos on the quadruped's RIGHT side
- Establishes serial connection between RPi and Arduino RP2040
- Checks for incoming messages, depending on the message, actuates
  one of 5 movements:
    'f': Forward
    's': Stand
    'l': Turn Left
    'r': Turn Right
    'd': Dance!
*/

#include <Servo.h>

const unsigned int MAX_MESSAGE_BYTE_SIZE = 2; // 1 byte char & 1 terminating byte

Servo R1_1; // Right 1 Joint 1
Servo R1_2; // Right 1 Joint 2
Servo R2_1; // Right 2 Joint 1
Servo R2_2; // Right 2 Joint 2

/* Angle Arrays for Forward Movement */
int joint1_angles_forward[80] = {143,144,143,142,140,139,138,138,138,139,141,142,144,145,147,148,150,151,153,154,156,158,160,162,165,168,172,175,178,180,180,178,177,175,174,172,171,170,168,167,165,164,163,162,160,159,158,156,155,154,153,152,151,149,148,147,146,145,144,143,143, 142, 141, 140, 139, 138, 138, 137, 136, 135, 134, 134, 133, 132, 132, 131, 131, 130, 130, 129};
int joint2_angles_forward[80] = {149,150,154,159,164,170,174,177,179,180,180,179,178,178,177,177,176,175,175,174,173,171,168,164,158,151,143,137,132,128,128,130,131,133,134,135,137,138,139,140,141,142,142,143,144,145,145,146,146,147,147,148,148,148,149,149,149,149,149,149,149, 149, 149, 149, 149, 150, 150, 150, 150, 151, 151, 152, 152, 153, 154, 154, 155, 156, 157, 157};

int joint1_angles_forward_secondary[100] = {143, 142, 141, 140, 139, 138, 138, 137, 136, 135, 134, 134, 133, 132, 132, 131, 131, 130, 130, 129, 143,144,143,142,140,139,138,138,138,139,141,142,144,145,147,148,150,151,153,154,156,158,160,162,165,168,172,175,178,180,180,178,177,175,174,172,171,170,168,167,165,164,163,162,160,159,158,156,155,154,153,152,151,149,148,147,146,145,144,143,143, 142, 141, 140, 139, 138, 138, 137, 136, 135, 134, 134, 133, 132, 132, 131, 131, 130, 130, 129};
int joint2_angles_forward_secondary[100] = {149, 149, 149, 149, 149, 150, 150, 150, 150, 151, 151, 152, 152, 153, 154, 154, 155, 156, 157, 157, 149,150,154,159,164,170,174,177,179,180,180,179,178,178,177,177,176,175,175,174,173,171,168,164,158,151,143,137,132,128,128,130,131,133,134,135,137,138,139,140,141,142,142,143,144,145,145,146,146,147,147,148,148,148,149,149,149,149,149,149,149, 149, 149, 149, 149, 150, 150, 150, 150, 151, 151, 152, 152, 153, 154, 154, 155, 156, 157, 157};

//int joint1_angles[60] = {143,144,143,142,140,139,138,138,138,139,141,142,144,145,147,148,150,151,153,154,156,158,160,162,165,168,172,175,178,180,180,178,177,175,174,172,171,170,168,167,165,164,163,162,160,159,158,156,155,154,153,152,151,149,148,147,146,145,144,143};
//int joint2_angles[60] = {149,150,154,159,164,170,174,177,179,180,180,179,178,178,177,177,176,175,175,174,173,171,168,164,158,151,143,137,132,128,128,130,131,133,134,135,137,138,139,140,141,142,142,143,144,145,145,146,146,147,147,148,148,148,149,149,149,149,149,149};

/* Angle Arrays for Dance Movement */
int joint1_angles_dance[20] = {143,145,147,149,151,153,154,156,158,159,159,158,156,154,153,151,149,147,145,143};
int joint2_angles_dance[20] = {149,153,157,161,165,168,172,175,178,180,180,178,175,172,168,165,161,157,153,149};

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT); // For debugging: RP2040 board LED will flash when data is received
  R1_1.attach(6);
  R1_2.attach(7);
  R2_1.attach(8);
  R2_2.attach(9);
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
      digitalWrite(LED_BUILTIN, HIGH);
      moveStand();
      digitalWrite(LED_BUILTIN, LOW);
      break;
    case 'l':
      moveLeft();
      break;
    case 'r':
      moveRight();
      break;
    case 'd':
      digitalWrite(LED_BUILTIN, HIGH);
      moveDance();
      digitalWrite(LED_BUILTIN, HIGH);
      break;
    default:
      break;
  }
}

void moveForward() {
  int secondary = 0;
  for (int i = 0; i < 80; i++){
    if (i >= 30) {
      R1_1.write(joint1_angles_forward_secondary[secondary]);
      R1_2.write(joint2_angles_forward_secondary[secondary]);
      secondary++; // secondary = 50 at i = 80
    }
    R2_1.write(joint1_angles_forward[i]);
    R2_2.write(joint2_angles_forward[i]);
    delay(15);
  }
  for (int j = 50; j < 100; j++) {
    R1_1.write(joint1_angles_forward_secondary[j]);
    R1_2.write(joint2_angles_forward_secondary[j]);
    delay(15);
  }
}

/*
void moveForward() {
  for (int i = 0; i < 30; i++) {
    R1_1.write(joint1_angles[i]);
    R1_2.write(joint2_angles[i]);
    delay(15);
  }
  for (int j = 0; j < 30; j++) {
    R2_1.write(joint1_angles[j]);
    R2_2.write(joint2_angles[j]);
    delay(15);
  }
  // waiting
  for (int q = 0; q < 30; q++) {
    R1_1.write(joint1_angles[29]);
    R1_2.write(joint2_angles[29]);
    delay(15);
  }
  for (int w = 0; w < 30; w++) {
    R2_1.write(joint1_angles[29]);
    R2_2.write(joint2_angles[29]);
    delay(15);
  }
  // waiting end

  for (int k = 30; k < 60; k++) {
    R1_1.write(joint1_angles[k]);
    R1_2.write(joint2_angles[k]);
    R2_1.write(joint1_angles[k]);
    R2_2.write(joint2_angles[k]);
    delay(15);
  }
}
*/

void moveStand() {
  R1_1.write(143);
  R1_2.write(149);
  R2_1.write(143);
  R2_2.write(149);
  delay(15);
}

void moveLeft() {}
void moveRight() {}
void moveDance() {
  for (int i = 0; i < 2; i++) { // Go up and down 2 times
    for (int j = 0; j < 20; j++) {
      R1_1.write(joint1_angles_dance[j]);
      R2_1.write(joint1_angles_dance[j]);
      R1_2.write(joint2_angles_dance[j]);
      R2_2.write(joint2_angles_dance[j]);
      delay(15);
    }
  }
  for (int i = 0; i < 10; i++) {
    R1_1.write(joint1_angles_dance[i]);
    R2_1.write(joint1_angles_dance[i]);
    R1_2.write(joint2_angles_dance[i]);
    R2_2.write(joint2_angles_dance[i]);
    delay(15);    
  }
  delay(5000);
  for (int i = 10; i < 20; i++) {
    R1_1.write(joint1_angles_dance[i]);
    R2_1.write(joint1_angles_dance[i]);
    R1_2.write(joint2_angles_dance[i]);
    R2_2.write(joint2_angles_dance[i]);
    delay(15);
  }
}
