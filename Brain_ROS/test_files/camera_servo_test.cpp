#include <wiringPi.h>
#include <pigpio.h>
#include <unistd.h>
#include <iostream>
#include <string>

using namespace std;

#define CAMERA_J1_SERVO_GPIO 18 // BCM GPIO 18
#define CAMERA_J2_SERVO_GPIO 13 // BCM GPIO 13

void print_info(int GPIO_ID) {
	cout << "Joint " << to_string(GPIO_ID) << " PWM duty cycle, frequency, range is: " << to_string(gpioGetPWMdutycycle(GPIO_ID)) << " " + to_string(gpioGetPWMfrequency(GPIO_ID)) << " " + to_string(gpioGetPWMrange(GPIO_ID)) << endl;
}

int main(int argc, char** argv) {
	if (gpioInitialise() < 0) {
		std::cerr << "pigpio setup failed." << endl;
		return 1;
	}

	// Custom set to: 50 Hz (output PWM frequency)
		// Originally: 800, 800
	//std::cout << "PWM Frequency of servo J1: " << to_string(gpioGetPWMfrequency(CAMERA_J1_SERVO_GPIO)) << endl;
	//std::cout << "PWM Frequency of servo J2: " << to_string(gpioGetPWMfrequency(CAMERA_J2_SERVO_GPIO)) << endl;

	// Custom set to: 0 - 2000 microseconds (duty cycle)
		// Originally: 255, 255
	//std::cout << "PWM Range of servo J1: " << to_string(gpioGetPWMrange(CAMERA_J1_SERVO_GPIO)) << endl;
	//std::cout << "PWM Range of servo J2: " << to_string(gpioGetPWMrange(CAMERA_J2_SERVO_GPIO)) << endl;

	//gpioSetPWMfrequency(CAMERA_J1_SERVO_GPIO, 800);
	//gpioSetPWMfrequency(CAMERA_J2_SERVO_GPIO, 800);

	//gpioSetPWMrange(CAMERA_J1_SERVO_GPIO, 2000);
	//gpioSetPWMrange(CAMERA_J2_SERVO_GPIO, 2000);

	//gpioPWM(CAMERA_J1_SERVO_GPIO, 0);
	//gpioPWM(CAMERA_J2_SERVO_GPIO, 0);


	//cout << "Starting position (0)" << endl;
	//print_info(CAMERA_J1_SERVO_GPIO);
	//print_info(CAMERA_J2_SERVO_GPIO);

	//usleep(3000000);

	//cout << "Joint 1 servo pulse width is: " << to_string(gpioGetServoPulsewidth(CAMERA_J1_SERVO_GPIO)) << endl;

	//cout << "Halfway position (1000)" << endl;
	//gpioPWM(CAMERA_J1_SERVO_GPIO, 1000);
	//print_info(CAMERA_J1_SERVO_GPIO);

	//usleep(3000000);

	//cout << "Full position (2000)" << endl;
	//gpioPWM(CAMERA_J1_SERVO_GPIO, 2000);
	//print_info(CAMERA_J1_SERVO_GPIO);

	//usleep(1000000);

	/*

	cout << "Setting J1 to center" << endl;
	gpioServo(CAMERA_J1_SERVO_GPIO, 1500);
	usleep(5000000);

	cout << "Setting J1 to most anti clockwise" << endl;
	gpioServo(CAMERA_J1_SERVO_GPIO, 1000);
	usleep(1000000);

	cout << "Setting J1 to most clockwise" << endl;
	gpioServo(CAMERA_J1_SERVO_GPIO, 2000);
	usleep(1000000);

	*/

	cout << "Setting J2 to center" << endl;
	gpioServo(CAMERA_J2_SERVO_GPIO, 1500);
	usleep(1000000);

	cout << "Setting J2 to all the way down" << endl;
	gpioServo(CAMERA_J2_SERVO_GPIO, 1000);
	usleep(5000000);

	cout << "Setting J2 to all the way up" << endl;
	gpioServo(CAMERA_J2_SERVO_GPIO, 2000);
	usleep(3000000);

	return 0;
}

/* TESTING WITH WIRINGPI LIBRARY
int main(int argc, char** argv) {
	if (wiringPiSetupGpio() < 0) {
		std::cerr << "wiringPi setup failed." << endl;
	}
	pinMode(1, PWM_OUTPUT);
	//pinMode(CAMERA_J2_SERVO_GPIO, PWM_OUTPUT);

	std::cout << "Pi rev board is: " << piBoardRev() << endl;

	for (int i = 0; i < 1024; i = i + 100) {
		std::cout << "Moving to position: " << i << endl;
		pwmWrite(1, i);
		usleep(1000000);
	}

	return 0;
}
*/
