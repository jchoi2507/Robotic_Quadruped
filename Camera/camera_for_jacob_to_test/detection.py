# import public libraries used in main file just in case (idk how Python file dependencies work, like if using a function from here in outside main.py does main.py use the import from main.py or in here?)
import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time

# for distance sensor
from machine import I2C
from vl53l1x import VL53L1X

# ??? do I need the imports in here? or ok if just in the main file?

# messages: 's' = stop, 'f' = forward, 'l' = left, 'r' = right
# at this point don't think need to make code as long as stick to this...


def set_sensors(sensor):
    # initialize distance (time-of-flight) sensor
    tof = VL53L1X(I2C(2))

    sensor.reset() # Resets the sensor
    sensor.set_pixformat(sensor.RGB565) # Sets the sensor to RGB
    sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
    sensor.set_vflip(True) # Flips the image vertically
    sensor.set_hmirror(True) # Mirrors the image horizontally
    sensor.skip_frames(time = 2000) # Skip some frames to let the image stabilize

    return tof

# function returns True if orange blob (otherwise inputted msg stays, default from main if 'f')
def is_orange(clock,img,thresholds):
    # message is default 'forward' -- only stop (send 's') if see orange
    msg = False

    # Find blobs with a minimal area of 50x50 = 2500 px
    # Overlapping blobs will be merged
    # ?? not sure if need to edit areaThreshold
    blobs = img.find_blobs(thresholds, area_threshold=2500, merge=True)

    # if blob found, change message to 'stop', draw blob on screen (get rid of for real dog, only for testing w IDE), turn on green led
    if len(blobs) > 0:
        msg = True

        ''' taken care of in final msg
        # Turn on green LED if a blob was found (stop)
        ledR.on()
        ledG.off()
        '''

        # Draw blobs (ONLY FOR TESTING)
        for blob in blobs:
            # Draw a rectangle where the blob was found
            img.draw_rectangle(blob.rect(), color=(0,255,0))
            # Draw a cross in the middle of the blob
            img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))

    ''' taken care of in final msg
    # turn on green led if blob not found (keep moving forward)
    else:
        # Turn the red LED on if no blob was found
        ledR.off()
        ledG.on()

        pyb.delay(50) # Pauses the execution for 50ms
        #print(clock.fps()) # Prints the framerate to the serial console
        #print("x", blob.cx(), "y", blob.cy())
    '''

    return msg

# function returns True if anything is detected within 150mm of distance sensor on board (otherwise inputted msg stays, default from main if 'f')
def is_too_close(tof,STOP_DIST):
    # default nothing too close, keep moving forward
    # take in current message, will stay same if nothing too close, will override with stop if something too close
    msg = False

    # get distance of board from closest object (using time-of-flight sensor)
    dist = tof.read() # [mm]

    # distance when an object becomes too close, so should stop robot
    # (roughly tested so far, sensor gets some error as move away from things)
    # updates could include doing some math based on speed to change STOP_MAX based on how fast robot is going to ensure sufficient time to stop motors
    # (i.e. if going faster, increase STOP_MAX so send stop command sooner since robot is going faster and will cover more distance while stopping than if it were moving slower)

    # if robot is close to an obstacle, tell it to stop
    # (for now just have print statement, for future send command to brain for brain to tell motors to stop)
    if dist < STOP_DIST:
        #print("too close")
        # if something is too close, override any message to tell robot to stop
        msg = True

    return msg

# function to run right before send final message to change led based on final message (after sensor fusion)
# assuming only change led once all sensors taken into account
def led_from_message(msg,ledR,ledG,ledB):
    if msg == 'f':
        ledG.on()
        ledR.off()
        ledB.off()
    elif msg == 'x':
        ledB.on()
        ledR.off()
        ledG.off()
    elif msg == 's':
        ledR.on()
        ledB.off()
        ledG.off()


