#include <Servo.h>
#include <string.h>
Servo servo;

void setup() {
  Serial.begin(9600);
  servo.attach(7);
}

void loop() {
  for (int i = 0; i < 180; i+=2) {
    servo.write(i);
    delay(30);
  }
  for (int j = 180; j > 0; j-=2) {
    servo.write(j);
    delay(30);
  }
}

void sendFromSerialMonitor() {
  while (Serial.available() > 0) {
      int angle = Serial.parseInt();
      if (angle == 0) {}
      else {
        Serial.println("Angle sending: " + String(angle));
        servo.write(angle);
      }
  }
}
