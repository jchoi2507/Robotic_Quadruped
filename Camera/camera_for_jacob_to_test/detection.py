# current task: adding what can from apriltags code to detection library
# next: add any main code need to main.py
# then: make import statements only fxns I need so not importing whole libraries

# import public libraries used in main file just in case (idk how Python file dependencies work, like if using a function from here in outside main.py does main.py use the import from main.py or in here?)
import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time
import math

# for distance sensor
from machine import I2C
from vl53l1x import VL53L1X

# ??? do I need the imports in here? or ok if just in the main file?

# messages: 's' = stop, 'f' = forward, 'l' = left, 'r' = right
# at this point don't think need to make code as long as stick to this...


def set_sensors(sensor,april_on):
    # initialize distance (time-of-flight) sensor
    tof = VL53L1X(I2C(2))

    sensor.reset() # Resets the sensor
    sensor.set_pixformat(sensor.RGB565) # Sets the sensor to RGB
    # if using april tags, need to use smaller resolution for camera so don't run out of memory
    if april_on:
        sensor.set_framesize(sensor.QQVGA) # Sets the resolution to 160x120 px (if resolution is bigger may run out of memory w april tags)
    else:
        sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
    sensor.set_vflip(True) # Flips the image vertically
    sensor.set_hmirror(True) # Mirrors the image horizontally
    sensor.skip_frames(time = 2000) # Skip some frames to let the image stabilize
    # the two commands below came with the example, but aren't supported by the Nicla Vision board. Still trying to figure out how to do this with the Nicla Vision, but code works fine for now so maybe not necessary
    #sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
    #sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...

    return tof

# function returns True if orange blob (otherwise inputted msg stays, default from main if 'f')
def is_orange(img,thresholds):
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
        #print(clock.fps()) # Prints the framerate to the serial console, need to import clock if want to do
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

# will try with function this references also defined in library but not sure if need to reference in main.py if main.py doesn't need to know about it if just called within this function
# function to get name of family of a detected tag
def family_name(tag):
    if(tag.family() == image.TAG16H5):
        return "TAG16H5"
    if(tag.family() == image.TAG25H7):
        return "TAG25H7"
    if(tag.family() == image.TAG25H9):
        return "TAG25H9"
    if(tag.family() == image.TAG36H10):
        return "TAG36H10"
    if(tag.family() == image.TAG36H11):

        return "TAG36H11"
    if(tag.family() == image.ARTOOLKIT):
        return "ARTOOLKIT"

# function to detect an april tag
# goal is to find if id is in chosen family (36H11) and within range needed for inputted list of commands (start id's from 0 and go up for as many messages as sending)
# returns: 0 to (+) #'s -- for any april tag in designated family and within range of # of messages
#          -1 -- april tag detected but not in desired family
#          -2 -- no april tags detected at all
def get_april_tag(img,april_tag_msgs): # take in april_msgs just for length to know range of ids looking for, but not actually choosing message within here b/c in main may have other sensors to take into account and would rather choose from all sensors than choose now and override later

    tag_families = 0
    tag_families |= image.TAG36H11 # (default family)

    # 'loop' will only run once if any b/c of return within...only need to id one april tag anyways for now...but could adjust later for two
    # loop through tags (detect in line below)
    for tag in img.find_apriltags(families=tag_families): # defaults to TAG36H11 without "families".
            # comment out when not using IDE
            img.draw_rectangle(tag.rect(), color = (255, 0, 0))
            img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))

            # get useful info about tag detected
            tag_fam = family_name(tag)
            tag_id = tag.id()
            rotation = (180 * tag.rotation()) / math.pi

            # if detected tag is within desired family and has an id within the range of the commands established above, send id #
            if family_name(tag) == "TAG36H11" and tag_id >=0 and tag_id<=(len(april_tag_msgs)-2): # subtract 2 b/c first msg is none (no april tag associated), and sub one to get index from length
                return tag_id
            # to indicate if april tag detected but not within range of ids
            elif family_name(tag) != None:
                return -1

    # if no april tags at all are detected
    return -2

# function to run right before send final message to change led based on final message (after sensor fusion)
# assuming only change led once all sensors taken into account
# this just interprets the code for an led associated with a message to turn the appropriate leds on
# msgs and corresponding leds are chosen in main.py (to allow for some flexibility with colors when testing)
def led_from_message(ledR,ledG,ledB,msg,msgs,leds): # msgs and leds are optional arguments if just want to turn an led on manually based on a letter from the code
    # default msg='n' so if no positional args are passed to this fxn, all the leds turn off
    leds_on = msg # otherwise if msg is not 'n', leds_on will change based on given msg to related led code to turn on proper leds

    # get index of sent message from list of messages
    index = msgs.index(msg)

    # get leds to turn on based on message
    leds_on = leds[index]

    # code for leds list: these are only possible strings I will input
    # g = green, r = red, b = blue, gb = green-blue, gr = green-red, rb = red-blue, n = none (no leds on)
    # maybe would have been more efficient to directly write led objects in but strings are easier to pass I think
    # or do for loop through list of leds to turn on? but just need for one message...
    if leds_on == 'g':
        ledG.on()
        ledR.off()
        ledB.off()
    elif leds_on == 'r':
        ledG.off()
        ledR.on()
        ledB.off()
    elif leds_on == 'b':
        ledG.off()
        ledR.off()
        ledB.on()
    elif leds_on == 'gb':
        ledG.on()
        ledR.off()
        ledB.on()
    elif leds_on == 'gr':
        ledG.on()
        ledR.on()
        ledB.off()
    elif leds_on == 'rb':
        ledG.off()
        ledR.on()
        ledB.on()
    elif leds_on == 'n':
        ledG.off()
        ledR.off()
        ledB.off()


