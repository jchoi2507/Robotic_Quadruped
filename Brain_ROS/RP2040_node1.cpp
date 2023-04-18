/*
RP2040_node1.cpp
By: Jacob Choi
Date: 4/15/2023

- The node in this file can be thought of a RP2040 node on the ROS network
	- In reality, it only exists in the RPi and interfaces with the RP2040 over serial
- Initializes a subscriber node to listen to topic: "topic_actuate"
- When subscriber queue is filled (size = 1), callback function stores char value
- Sends char value to RP2040 over UART serial
*/

#include <ros/ros.h>
#include <std_msgs/Char.h>
#include <iostream>
#include <wiringSerial.h>
#include <string>

using namespace std;

/* Serial USB Connection to RP2040 Setup */
const char *port_connection = "/dev/ttyACM0"; // Initialize RP2040 <-> RPi 4b USB port connection
				      	      // To figure this out, "clever stack overflow" trick: 1) BEFORE PLUGIN: ls -l /dev > dev.txt
					      //                                                    2) AFTER PLUG IN: ls -l /dev > dev2.txt
					      //                                                    3) Diff the two text files 
int baudrate = 9600; // Initialize baudrate
int serialDeviceID = serialOpen(port_connection, baudrate); // Returns: -1 for any error 

/*
callback()
Callback function executes whenever subscriber queue is non-empty.
	1) Prints out received message to ROS_INFO output stream
	2) Sends received message char over serial to RP2040
	3) Flushes serial stream
*/
void callback(const std_msgs::CharConstPtr& msg) {
	ROS_INFO("Message Received: %c", msg->data);
	serialPutchar(serialDeviceID, msg->data); // Send character to RP2040 over serial
	serialFlush(serialDeviceID);
}

int main(int argc, char** argv) {
	/* ROS Subscriber Node Setup */
	ros::init(argc, argv, "RP2040_node1"); // Initialize node called "RP2040_node1"
	ros::NodeHandle node_handle;
	ros::Subscriber subscriber = node_handle.subscribe("topic_actuate", 1, &callback); // Subscribe to "topic_actuate"

	// Check serial connection
	if (serialDeviceID == -1) {ROS_ERROR("Unable to open serial device."); return 1;}

	/* Main Node Function */
	ros::spin();
	return 0;
}
