# import the fxns for diff methods of detection and keep this simple communication code?
# get the image here and use as param for function within detection file then get direction as result
# should I be doing classes???
# will having separate files on board take up more space than all code in one file?
# like would types of the class be orange, apple, april tag1, apriltag2, etc? but not sure if really need classes for that...
# is this even helpful if I'm not doing it the right/most efficient way??? maybe I should just ask jacob the cs major what he thinks how to organize it

#?? add stuff from this april tags version to thresholds

from pyb import USB_VCP

# for distance sensor
from machine import I2C
from vl53l1x import VL53L1X

# !!! change to from ___ import __
import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time
import math

# import detection stuff
import detection # self-created library
from thresholds import thresholdsOrange, STOP_MAX

# --- set-up leds, clock ---
# ??? ctrl leds from here once get final message, or within library? I guess harder to change on the fly if in library but then simpler code here...
ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led
ledBlue = pyb.LED(3) # Initiates the blue led

clock = time.clock() # Instantiates a clock object
# --------------------------

# set-up usb for serial communication
usb = USB_VCP()

# toggle to change how code executes (prints if testing, sends over usb if connected to brain)
testing = True

# toggle based on if detecting april tags below b/c when setting up sensors need to use lower resolution to have enough memory when using april tags
# !!! could later implement way if code can detect itself if april tag functions from my library are being used to turn on the right resolution
# i.e. once I import from the libraries, if can somehow detect that find_aprils was imported so don't have to remember to change here when changing detection methods in demo live
# or maybe when implementing all stuff will find need more memory so just use lower resolution all the time, though I haven't tested non-april tag stuff w the lower resolution not sure
# i.e. blob_detect_clementine uses higher QVGA
using_april_tags = True

# toggle to chnage if want robot to stop if ANYTHING is too close, no matter what the close object is
e_stop = True

# --- set up detection stuff ---
# ??? could this be done inside detection library ???
tof = detection.set_sensors(sensor,using_april_tags) # ??? should I always setup tof in case need? b/c seems more efficient than initialize every loop of while True when call command, but also seems inefficient to setup here then pass along later if needed...
# list of discrete commands to send to brain
# just use index (0, 1, 2, 3, etc.) as the april tag id
# (april tag ids go from 0 - whatever #, so say first command in list has id=0, second has id=1, etc., instead of making a list of ids...)
msgs = ['s', 'f', 'd'] # stop, forward, dance
leds = ['r', 'g', 'b'] # list of led colors to choose related to each message -- g = green, r = red, b = blue, gb = green-blue, gr = green-red, rb = red-blue
# ?? should do in 2d array? could be more edge-case friendly to check that these are same length...but I trust myself to write the code hopefully, and take care of incorrect characters but not possible b/c no user input only I hardcoding and I would find error
# ??? should names be diff btwn here and libraries???
# -----------------------

# loop forever
while True:

    # initialize message to edit based on info from sensors
    message = msgs[0] # default is stopped

    clock.tick() # Advances the clock

    # take image and save in memory
    img = sensor.snapshot()

    # --- get info from sensors ---
    # !!! if using april tags remember to change boolean above so cam resolution is set small enough to have enough memory

    # check for direction based on color detected
    ####is_orange = detection.is_orange(img,[thresholdsOrange]) # add more thresholds imported inside [] if applicable

    # check if anything is too close (always override any other message if something is too close so robot will stop)
    is_too_close = detection.is_too_close(tof,STOP_MAX)

    april_id = detection.get_april_tag(img,msgs) # 0 to len(april_msgs)-1 if tag detected in 36H11 family and within range of # of messages, -1 if april tag but not in right family, -2 if no april tags at all
    # -----------------------------

    # not sure if it makes sense to put this message decision in main b/c could have just sent this message from the function b/c already have if statement like this within the get_april_tags() function
    # but want to maintain deciding message out here in case other factors with april tag for message though not sure if this will happen
    if april_id >= 0:
        # get message correlated with index of messages in list above
        message = msgs[april_id]

    # --- choose message based on fusion of sensor info ---
    # possible messages: 'f' = forward, 's' = stop, 'd' = dance (this is what is physically feasible with the dog)

    '''
    # if color is detected, start slowing down (object is in field of view)
    if is_orange:
        message = 'x'

        # if this object is too close, stop the robot
        if is_too_close:
            message = 's'
    '''
    # -----------------------------------------------------
    # toggle emergency stop so that if ANYTHING is too close, stop the robot
    # leave off if only want to stop if certain objects are too close
    if e_stop:
        if is_too_close:
            message = msgs[0] # 's' = stop
            print("too close")


    # --- manage leds based on final message ---
    # ??? should I switch to do within specific sensors?
    detection.led_from_message(msgs,leds,message,ledRed,ledGreen,ledBlue)
    # ------------------------------------------


    # --- send message ---
    time_btwn_msgs = .1 # [s]
    # for when connected to brain
    if not testing:
        # if usb is connected, send serial message
        if (usb.isconnected()):
            usb.write(message) # message is type str
            time.sleep(time_btwn_msgs)
    # for testing just w Nicla (not connected to brain)
    else:
        # for testing just w nicla
        print(message)
        time.sleep(time_btwn_msgs)
    # -------------------

