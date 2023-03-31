# Modified from example on OpenMV IDE for distance sensor built-in to the Nicla Vision camera
# by Rose Kitz
# last updated 3/31/23

from machine import I2C
from vl53l1x import VL53L1X
import time
import pyb # for built-in board capabilities (besides camera)

# initialize distance (time-of-flight) sensor
tof = VL53L1X(I2C(2))

redLED = pyb.LED(1) # built-in red LED

# function to blink the built-in red LED once, with 10ms delay in between
def blink_red():
    redLED.on()
    pyb.delay(10)
    redLED.off()

while True:
    # get distance of board from closest object (using time-of-flight sensor)
    dist = tof.read() # [mm]

    # distance when an object becomes too close, so should stop robot
    # (roughly tested so far, sensor gets some error as move away from things)
    # updates could include doing some math based on speed to change STOP_MAX based on how fast robot is going to ensure sufficient time to stop motors
    # (i.e. if going faster, increase STOP_MAX so send stop command sooner since robot is going faster and will cover more distance while stopping than if it were moving slower)
    STOP_MAX = 150 # [mm]

    # if robot is close to an obstacle, tell it to stop
    # (for now just have print statement, for future send command to brain for brain to tell motors to stop)
    if dist < STOP_MAX:
        # replace this line below with message to brain to tell the motors to stop
        print("Stop! Something is", dist, "mm away.")
        # blink built-in red LED to visually indicate the robot is close to something
        # (could replace with external LED later that is easier to see once the camera is mounted on the robot)
        blink_red()
    else:
        pyb.delay(10) # since have 10ms delay if blink if object detected want same delay if not? so loop always has same time? or is this just making the loop less efficient?
    #print(f"Distance: {tof.read()}mm")
    time.sleep_ms(50)

