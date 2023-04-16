/*
talker.cpp
By: Jacob Choi
Date: 4/15/2023

- Initializes a publisher node to publish to topic: "topic_actuate"
- Receives data from Arduino Nicla over UART serial
- Publishes data to "topic_actuate"
*/

#include <ros/ros.h>
#include <std_msgs/Char.h>
#include <iostream>
#include <wiringSerial.h>
#include <string>

using namespace std;

/* Serial USB Connection from Arduino Nicla Setup */
const char *port_connection = "/dev/";
int baudrate = 9600;
int serialDeviceID = serialOpen(port_connection, baudrate);

int main(int argc, char** argv) {
	ros::init(argc, argv, "talker"); // Initialize node called "talker"
	ros::NodeHandle node_handle;
	ros::Publisher publisher = node_handle.advertise<std_msgs::Char>("topic_actuate", 1); // Topic name, publisher queue size
	//ros::Rate rate(10); // 10 Hz

	while(ros::ok()) {
		std_msgs::Char msg;
		//msg.data = "";
		publisher.publish(msg);
		ros::spinOnce(); // Allows for backend to update on every iteration
	//	rate.sleep();  // Maintains the 10 messages/second frequency rate	
	}
	return 0;
}
