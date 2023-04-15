/*
serial_receive_test.cpp
By: Jacob Choi
Date: 4/15/2023

- Used to test ROS node <-> RP2040 serial communication interface
- Initializes a publisher node to topic: "topic_test"
- Outputs to cout if serial data is received from RP2040
*/

#include <ros/ros.h>
#include <std_msgs/String.h>
#include <iostream>
#include <wiringSerial.h>
#include <string>

using namespace std;

const char *port_connection = "/dev/ttyACM0"; // initialize RP2040 <-> RPi 4b USB port connection
				      	      // to figure this out, "clever stack overflow" trick: 1) BEFORE PLUGIN: ls -l /dev > dev.txt
					      //                                                    2) AFTER PLUG IN: ls -l /dev > dev2.txt
					      //                                                    3) diff the two text files 
int baud_rate = 9600; // initialize baudrate

// Callback function--this function is called every time a message is received in the topic from the subscriber node
void callback(const std_msgs::StringConstPtr& msg) {
	std::cout << msg->data << std::endl;
}

int main(int argc, char** argv) {
	ros::init(argc, argv, "talker_node"); // initialize node called "talker_node"
	ros::NodeHandle node_handle; // node handle
	ros::Publisher publisher = node_handle.advertise<std_msgs::String>("topic_test", 1);
	ros::Rate rate(1); // 1 Hz rate

	int serialDeviceID = 0;
	char input;

	serialDeviceID = serialOpen(port_connection, baud_rate); // Returns: -1 for any error
	if (serialDeviceID == -1) { std::cout << "Unable to open serial device." << std::endl; return 1;}

	while (ros::ok()) {
		if (serialDataAvail(serialDeviceID > 0)) { 
			input = serialGetchar(serialDeviceID);
			//message.data = std::string() + input;
			std::cout << "MESSAGE RECEIVED!!!! " << input << std::endl;
			//publisher.publish(message);
		}
		serialFlush(serialDeviceID);
		ros::spinOnce();
		rate.sleep();
	}

	return 0;
}

