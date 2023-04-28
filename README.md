<p>
    <img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_0325.jpeg" width="48%" img align="left">
    <img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_0318.jpeg" width="48%" img align="top">
</p>
<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/quadruped_walking_one_cycle.gif" width="48%" img align="top">
<br clear="both"/>

# 1. Overlay Demo

#### <p align="left"> Clicking the thumbnails will redirect the current tab—these images are deceptively NOT embedded </p>

| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/camera_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=gz5IpHd0LCQ) | [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/walking_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=fqAFdLbydDc) |
|:--:| :--: | 
| Controlling Camera Servos | Forward Walking |
| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/dancing_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=6Ijx8-6ygXU)| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/dancing_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=6Ijx8-6ygXU) |
| Dancing! | *TBD* |

# 2. Process

## i) Mechanical Stuff
- laser cut wood (body)
- double-layered laser cut acryllic (legs)

## ii) Electrical Stuff
- pictures
- component specs
- wiring diagram

## iii) Software Stuff
- ros node tree
    - explanation
- dev view explanation
- image processing stuff
    - april tag, tennis ball, stop sensor
<img src="https://github.com/jchoi2507/catkin_ws/blob/main/bin/Screenshot%202023-04-26%20at%203.11.01%20PM.png" width="80%">
    
# 3. Extra

## i) Repo Folder Tree
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
`/Brain_ROS`: Arduino RP2040 code (servo control), C++ ROS code, node & UART setup <br/>
`/Camera`: Arduino Nicla Camera image processing code <br/>
`/Inverse_Kinematics`: Path-planning code <br/>
`/Leg_Actuation`: Servo angles <br/>
`/catkin_ws`: ROS catkin workspace folder <br/>

## ii) Bloopers
