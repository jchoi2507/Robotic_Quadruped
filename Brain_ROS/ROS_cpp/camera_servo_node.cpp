/*
camera_servo_node.cpp
By: Jacob Choi
Date: 4/25/2023

- Allows keyboard control of the 2 servos that rotate the camera 10 degrees:
	- 'w' input: up
	- 's' input: down
	- 'a' input: left
	- 'd' input: right
- PWM Info
	- PWM Frequency: 50 Hz
	- PWM Pulse Width: 500-2500 microseconds
*/

#include <ros/ros.h>
#include <pigpio.h>
#include <iostream>
#include <string>
#include <unistd.h>

using namespace std;

// BCM GPIO
#define CAMERA_J1 18
#define CAMERA_J2 13

// Pulse Widths (microseconds)
#define MIN 1000
#define CENTER 1500
#define MAX 2000
#define TURN 111 // equal to 20 degrees

void actuateServos(char input);
void print_PW_info(int CAMERA_ID);

int main(int argc, char** argv) {
	if (gpioInitialise() < 0) {
		ROS_ERROR("pigpio setup failed.");
	}

	char input;
	gpioServo(CAMERA_J1, CENTER);
	gpioServo(CAMERA_J2, CENTER);

	while (input != 'q') {
		ROS_INFO("Camera Control: w/a/s/d");
		std::cin >> input;
		actuateServos(input);
		usleep(1000000);
	}
	return 0;
}

void actuateServos(char input) {
	// Current pulse width values
	int currPW_J1 = gpioGetServoPulsewidth(CAMERA_J1);
	int currPW_J2 = gpioGetServoPulsewidth(CAMERA_J2);

	switch (input) {
		case 'w':
			if (currPW_J2 >= MAX - TURN) {ROS_INFO("Already rotated to the max."); break;}

			ROS_INFO("Turning upwards 20 degrees.");
			gpioServo(CAMERA_J2, currPW_J2 + TURN);
			print_PW_info(CAMERA_J2);
			break;
		case 's':
			if (currPW_J2 <= MIN + TURN) {ROS_INFO("Already rotated to the min."); break;}

			ROS_INFO("Turning downwards 20 degrees.");
			gpioServo(CAMERA_J2, currPW_J2 - TURN);
			print_PW_info(CAMERA_J2);
			break;
		case 'a':
			if (currPW_J1 >= MAX - TURN) {ROS_INFO("Already rotated to the max."); break;}

			ROS_INFO("Turning rightwards 20 degrees.");
			gpioServo(CAMERA_J1, currPW_J1 + TURN);
			print_PW_info(CAMERA_J1);
			break;
		case 'd':
			if (currPW_J1 <= MIN + TURN) {ROS_INFO("Already rotated to the min."); break;}

			ROS_INFO("Turning leftwards 20 degrees.");
			gpioServo(CAMERA_J1, currPW_J1 - TURN);
			print_PW_info(CAMERA_J1);
			break;
		default:
			ROS_INFO("Invalid command.");
			break;
	}
}

void print_PW_info(int CAMERA_ID) {
	string display = "Current Pulse Width: " + to_string(gpioGetServoPulsewidth(CAMERA_ID));
	cout << endl << display << endl;
}
