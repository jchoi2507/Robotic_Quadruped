#include <ros/ros.h>
#include <std_msgs/String.h>

int main(int argc, char**argv) {
	ros::init(argc, argv, "cameranode"); // initializing node
	ros::NodeHandle cameranode_handle; // obtaining handle for the ROS node
	ros::Publisher publisher = cameranode_handle.advertise<std_msgs::String>("topic_test", 1); // Topic Name, Queue Size
	ros::Rate rate(10); // 10 Hz

	while(ros::ok()) {
		std_msgs::String testMessage;
		testMessage.data = "HELLO!";
		publisher.publish(testMessage);
		ros::spinOnce(); // Allows for backend to update on every iteration
		rate.sleep();  // Maintains the 10 messages/second frequency rate	
	}
	return 0;
}
