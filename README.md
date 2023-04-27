# Final Demo

<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_0325.jpeg" width="49%" img align="left">
<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_0318.jpeg" width="49%" img align="top">
<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/quadruped_walking_one_cycle.gif" width="49%" img align="top">
<br clear="both"/>

# Overlay Demos
###### *Clicking the thumbnails will redirect the current tab—these images are deceptively NOT embedded*

| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/camera_yt_player.png" width="100%" img align="center">](https://www.youtube.com/watch?v=gz5IpHd0LCQ) | [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/walking_yt_player.png" width="100%" img align="center">](https://www.youtube.com/watch?v=fqAFdLbydDc) |
|:--:| :--: | 
| *Controlling Camera Servos* | *Forward Walking* |

| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/dancing_yt_player.png" width="100%" img align="center">](https://www.youtube.com/watch?v=6Ijx8-6ygXU)| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/dancing_yt_player.png" width="100%" img align="center">](https://www.youtube.com/watch?v=6Ijx8-6ygXU) |
|:--:| :--: | 
| *Dancing!* | *TBD* |

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
