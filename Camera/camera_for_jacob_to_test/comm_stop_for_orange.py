# is there a way to just import the code for diff methods of detection and keep this simple communication code?
# get the image here and use as param for function within detection file then get direction as result
# should I be doing classes???
# will having separate files on board take up more space than all code in one file?
# like would types of the class be orange, apple, april tag1, apriltag2, etc? but not sure if really need classes for that...
# is this even helpful if I'm not doing it the right/most efficient way??? maybe I should just ask jacob the cs major what he thinks how to organize it

from pyb import USB_VCP

import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time

# --- detection stuff ---
import detection # self-created library
from thresholds import thresholdsOrange
# ??? could this be done inside detection library ???
detection.set_sensors(sensor)
# -----------------------

# --- set-up leds, clock ---
ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led

clock = time.clock() # Instantiates a clock object
# --------------------------

# set-up usb for serial communication
usb = USB_VCP()

# loop forever
while True:
    clock.tick() # Advances the clock

    # take image and save in memory
    img = sensor.snapshot()

    # --- get message (str) based on detection (input image and any other necessary info) ---
    message = detection.command_from_blobs(clock,img,[thresholdsOrange],ledRed,ledGreen) # add more thresholds imported inside [] if applicable

    ''' for when connected to brain
    # if usb is connected, send serial message
    if (usb.isconnected()):
        usb.write(message) # message is type str
        time.sleep(5)
    '''
    # for testing just w nicla
    print(message)
    time.sleep(1)
