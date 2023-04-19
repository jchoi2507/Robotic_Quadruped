/*
RP2040_Serial_Receive.ino
By: Jacob Choi
Date: 4/15/2023

- Establishes serial connection between RPi and Arduino RP2040
- Checks for incoming messages, depending on the message, actuates
  one of 5 movements:
    'f': Forward
    's': Stop
    'l': Turn Left
    'r': Turn Right
    'd': Dance!
*/

const unsigned int MAX_MESSAGE_BYTE_SIZE = 2; // 1 byte char & 1 terminating byte

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT); // For debugging: RP2040 board LED will flash when data is received
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
      delay(10000); // for debugging only--remove later
      digitalWrite(LED_BUILTIN, LOW);
      break;
    case 's':
      moveStop();
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
void moveForward() {}
void moveStop() {}
void moveLeft() {}
void moveRight() {}
void moveDance() {}
