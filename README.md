# Final Demo

<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_0325.jpeg" width="49%" img align="left">
<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_0318.jpeg" width="49%" img align="top">
<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_8518.jpg" width="49%" img align="top">

<br clear="both"/>

<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/quadruped_walking_one_cycle.gif" width="49%" img align="left">

<br clear="both"/>

# Mechanical Setup

# Electrical Setup

# Software Setup

# Folder Tree
```bash
├── Brain_ROS
    ├── Arduino_cpp
    ├── ROS_cpp
    └── test_files
├── Camera
    ├── camera_for_jacob_to_test
    ├── rough_imageprocessing_examples
    └── tested_imageprocessing_examples
├── Inverse_Kinematics
├── Leg_Actuation
└── catkin_ws
```
`/Brain_ROS`: Arduino RP2040 code (servo control), C++ ROS code, node & UART setup <br />
`/Camera`: Arduino Nicla Camera image processing code <br />
`/Inverse_Kinematics`: Path-planning code <br />
`/Leg_Actuation`: Servo angles <br />
`/catkin_ws`: ROS catkin workspace folder <br />
