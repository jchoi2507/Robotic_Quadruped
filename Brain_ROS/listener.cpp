#include <ros/ros.h>
#include <std_msgs/String.h>
#include <iostream>

// Callback function--this function is called every time a message is received in the topic from the subscriber node
void callback(const std_msgs::StringConstPtr& msg) {
	std::cout << msg->data << std::endl;
}

int main(int argc, char** argv) {
	ros::init(argc, argv, "listener"); // initialize node called "listener"
	ros::NodeHandle node_handle; // node handle
	ros::Subscriber subscriber = node_handle.subscribe("topic_test", 1, &callback); // subscriber object, subscribed to topic "topic_test"

	ros::spin(); // spin() will keep looping, running the node until the node is shutdown explicitly

	return 0;
}

