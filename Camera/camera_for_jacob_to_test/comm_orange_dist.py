# is there a way to just import the code for diff methods of detection and keep this simple communication code?
# get the image here and use as param for function within detection file then get direction as result
# should I be doing classes???
# will having separate files on board take up more space than all code in one file?
# like would types of the class be orange, apple, april tag1, apriltag2, etc? but not sure if really need classes for that...
# is this even helpful if I'm not doing it the right/most efficient way??? maybe I should just ask jacob the cs major what he thinks how to organize it

from pyb import USB_VCP

# for distance sensor
from machine import I2C
from vl53l1x import VL53L1X

# !!! change to from ___ import __
import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time

# --- detection stuff ---
import detection # self-created library
from thresholds import thresholdsOrange, STOP_MAX
# ??? could this be done inside detection library ???
tof = detection.set_sensors(sensor) # ??? should I always setup tof in case need? b/c seems more efficient than initialize every loop of while True when call command, but also seems inefficient to setup here then pass along later if needed...
# ??? should names be diff btwn here and libraries???
# -----------------------

# --- set-up leds, clock ---
ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led
ledBlue = pyb.LED(3) # Initiates the blue led

clock = time.clock() # Instantiates a clock object
# --------------------------

# set-up usb for serial communication
usb = USB_VCP()

# toggle to change how code executes (prints if testing, sends over usb if connected to brain)
testing = True

# toggle to chnage if want robot to stop if ANYTHING is too close, no matter what the close object is
e_stop = False

# loop forever
while True:

    # initialize message to edit based on info from sensors
    message = 'f' # default is forward

    clock.tick() # Advances the clock

    # take image and save in memory
    img = sensor.snapshot()

    # --- get info from sensors ---
    # check for direction based on color detected
    is_orange = detection.is_orange(clock,img,[thresholdsOrange]) # add more thresholds imported inside [] if applicable
    # check if anything is too close (always override any other message if something is too close so robot will stop)
    is_too_close = detection.is_too_close(tof,STOP_MAX)
    # -----------------------------


    # --- choose message based on fusion of sensor info ---
    # possible messages: 's' = stop, 'x' = 'slow down', 'f' = forward, 'l' = left, 'r' = right

    # if color is detected, start slowing down (object is in field of view)
    if is_orange:
        message = 'x'

        # if this object is too close, stop the robot
        if is_too_close:
            message = 's'
    # -----------------------------------------------------
    # toggle emergency stop so that if ANYTHING is too close, stop the robot
    # leave off if only want to stop if certain objects are too close
    if e_stop:
        if is_too_close:
            message = 's'


    # --- manage leds based on final message ---
    # ??? should I switch to do within specific sensors?
    detection.led_from_message(message,ledRed,ledGreen,ledBlue) # red = stop, blue = slow down, green = go forward
    # ------------------------------------------


    # --- send message ---
    time_btwn_msgs = .5 # [s]
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
