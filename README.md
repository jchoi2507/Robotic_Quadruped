# Table of Contents

1. Demo
2. Process
    1. Mechanical Stuff
    2. Electrical Stuff
    3. Software Stuff
3. Extra
    1. Repo Folder Tree
    2. Bloopers

# 1. Demo

<table>
<tr><td>
<img width=1000>
<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_0325.jpeg" width="100%">
</td><td>
<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_0318.jpeg" width="100%" img align="top">
</br> <br>
<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/quadruped_walking_one_cycle.gif" width="100%" img align="top">
</td></tr> </table>

----

###### <p align="center"> *Clicking the thumbnails will redirect the current tab—these images are deceptively NOT embedded* </p>

| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/camera_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=gz5IpHd0LCQ) | [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/walking_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=fqAFdLbydDc) |
|:--:| :--: | 
| *Controlling Camera Servos* | *Forward Walking* |
| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/dancing_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=6Ijx8-6ygXU)| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/dancing_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=6Ijx8-6ygXU) |
| *Dancing!* | *TBD* |

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
