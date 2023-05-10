# Robotic Quadruped with ROS and OpenMV
<p>
    <img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_0325.jpeg" width="48%" img align="left">
    <img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/quadruped_walking_one_cycle.gif" width="48%" img align="top">
</p>
<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_0318.jpeg" width="48%" img align="top">

Full writeup and documentation is [here.](https://organic-diadem-cec.notion.site/Final-Robotic-Quadruped-Dog-with-ROS-and-OpenMV-f2feed3d056e45b3b69db89706526826)

## 1. Overlay Demo
<p align="left"> Clicking the thumbnails will redirect the current tab—these images are deceptively NOT embedded </p>

| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/camera_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=gz5IpHd0LCQ) | [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/walking_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=fqAFdLbydDc) |
|:--:| :--: | 
| Controlling Camera Servos | Forward Walking |
| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/dancing_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?v=6Ijx8-6ygXU)| [<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/apriltags_yt_player.png" width="95%" img align="center">](https://www.youtube.com/watch?app=desktop&v=cIhGNEBhQTE) |
| Dancing! | April Tag Movements |

## 2. Process

#### i) Electrical Stuff
<p>
    <img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/IMG_8485.jpeg" width="35%" img align="left">

| Component | Notes | QTY
| :--: | :--: | :--: |
| 2S 35C 2200 mAh 7.4V LiPo | Servo power | 2 |
| 5V 3A 10000mAh Portable Charger | Microcontroller power | 1 |
| MG996R servos | Leg actuation | 8 |
| Micro SG90 servos | Tail & camera actuation | 3 |
| DC buck converter | 8A rating | 2 |
| Power distribution block | 16A rating | 2 |
| Raspberry Pi 4b | Brain microcontroller | 1 |
| Arduino Nicla | Camera vision microcontroller | 1 |
| Arduino Nano RP2040 | Legs microcontroller | 2 | 
</p>

<br clear="all">

#### ii) Software Stuff
<img src="https://github.com/jchoi2507/Robotic_Quadruped/blob/main/Pictures/341983223_616872927138395_8193758385470865206_n.jpeg" width="80%">
Each microcontroller represents a node in our ROS network. The only microcontroller actually running ROS is the Raspberry Pi, which then interfaces with the other microcontrollers through the RPi’s USB ports that allow serial communication over UART.
<br> <br>
The Nicla node publishes commands to the topic: topic_actuate that the two RP2040 nodes are subscribed to. The keyboard node also publishes to the same topic, and allows for external manual control of the robot. The camera servo node is the only node not connected to the other nodes, because it controls the microservos that are directly hooked up to the Raspberry Pi’s GPIO pins.
<br> <br>
Once a subscriber node receives a message on the topic, it serially sends a corresponding command to the respective microcontroller to actuate the command.
<br> <br>
<img src="https://github.com/jchoi2507/catkin_ws/blob/main/bin/Screenshot%202023-04-26%20at%203.11.01%20PM.png" width="80%">
Overlay explanation:
<br> <br>
1. Main roscore node: master node that handles all node communication <br>
2. Camera servo node: to manually control camera position with keystroke inputs <br>
3. Keyboard node: to manually control leg actuation with keystroke inputs <br>
4. Arduino Nicla node: camera vision input <br>
5. RP2040 node #1: RP2040 that controls right legs (4 servos) <br>
6. RP2040 node #2: RP2040 that controls left legs (4 servos) <br>
    
## 3. Extra

#### i) Repo Folder Tree
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

#### ii) Bloopers
[Bloopers!](https://www.youtube.com/watch?v=gSAcY2aBXqs) <br>
[Dancing to Tennis Ball](https://www.youtube.com/watch?app=desktop&v=MWfQW3u1T5w)
