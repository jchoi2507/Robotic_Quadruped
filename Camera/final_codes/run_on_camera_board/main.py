'''
main.py
By: Rose Kitz
Edited by: jacob :)
Date: 4/21/2023

- Image processing code for robotic quadruped, to be used with Arduino Nicla vision camera
- Camera vision inputs & corresponding outputs:

    INPUT         ->         OUTPUT
    -------------------------------
    April Tag [0] ->	 STAND
    April Tag [1] ->	 FORWARD
    April Tag [2] ->	 DANCE
    Tennis Ball   ->	 DANCE
    Too close     ->	 STAND
'''
# NOTE: You can easily/quickly change the messages you want to send from the camera to the brain for any number of april tags you want
# Simply go to line 79 below and add one-character strings as elements to the 'msgs' list to add what strings can be sent over serial to the RasPi
# Then, on line 80, add strings as elements to choose what led color you want to correspond to each action.
# The code is listed in the comment on that line, only 6 color combinations are possible with the on-board led and must be entered as lowercase strings in the order mentioned in the code.
# To turn all leds off, enter 'n'.
# The index # of the message and its corresponding color is then one more than the april tag id # that will trigger that message (i.e. 's' at index 1 in msgs = april tag id 0)
# since it was necessary to add a 'nothing' command to the list of messages to distinguish between when stop is called and when nothing is actually desired to happen with an april tag

# -------------------------------------------------------------------------------

import sensor
import image # machine vision algorithms
from time import sleep, ticks_add, ticks_diff, ticks_ms
import math
import detection # Custom library to receive boolean T/F or integers for certain objects (colors, April Tags, etc, etc.)
from thresholds import thresholdsOrange, thresholdsTennisBall8, STOP_MAX
from pyb import USB_VCP, LED # pyb is for board-related functions
from machine import I2C # for distance sensor
from vl53l1x import VL53L1X # for distance sensor
import network, omv, rtsp # for livestream

''' Setup '''
ledRed = LED(1)
ledGreen = LED(2)
ledBlue = LED(3)

usb = USB_VCP() # set-up usb for serial communication

testing = False # True for printing to terminal
                # False for serial communication w/ Raspberry Pi

using_april_tags = True
using_circles = True # Also need QQVGA (smaller frame size) for circle detection

e_stop = True # True for sending stop command if ANY object is too close
                # False otherwise

# --- set up detection stuff ---
tof = detection.set_sensors(sensor,using_april_tags,using_circles)

msgs = ['n','s','f','d','h'] # Messages to send to Raspberry Pi over UART
                                        # nothing, stand (stop), forward, dance, move head AND dance
leds = ['n','r','g','rb','rgb'] # Onboard LED colors to choose related to each message
                                            # g = green, r = red, b = blue, gb = green-blue, gr = green-red, rb = red-blue, rgb = red-green-blue, n = none (no leds on)

time_btwn_msgs = 2000 # [ms]

''' main '''
if (__name__ == "__main__"):
    while True:

        message = msgs[0] # Initialize to nothing

        # start timer so do 'while' with snapshots continuously but only break out once every 2 seconds to send message
        deadline = ticks_add(ticks_ms(), time_btwn_msgs)
        while ticks_diff(deadline, ticks_ms()) > 0:
            img = sensor.snapshot() # take image and save in memory

            color_copy = img # save as color for april tags later b/c modify img to be B&W based on tennis threshold (or could just id tennis ball last and chane image then...

            if using_circles:
                img = sensor.snapshot().lens_corr(1.8)

            # Make image b&w and eliminate noise
            img.binary([thresholdsTennisBall8])
            img.erode(3,3) # from testing realized want smaller threshold for erode and larger for dilate so lots of pixels are deleted, but only bigger clusters are expanded (not small noise left expanded)
            img.dilate(3,15)

            '''
            # get True/False if image snapshot has tennis ball color in it, return blobs to find characteristics of later
            # -- input params: image snapshot, color thresholds
            # -- outputs: T/F if blob is within color thresholds, blobs object
            is_tennis_color, blobs = detection.is_color(img,[thresholdsTennisBall8]) # add more thresholds imported inside [] if applicable

            # get T/F if any of the green blobs are circular & curved enough (params from testing)
            # -- input params: blobs object, max/min roundness/convexity
            # -- output: T/F if any blob in blobs is circular/convex enough (compared to tested input params below)
            is_blob_circle = detection.is_blob_round(blobs,0.80) # (blobs,max_roundness) -- docs say 1 is a perfect circle, but testing had a square at 1...after testing w diff thresholds actually this is true just w small L range threshold roundness goes down a lot
            is_blob_curved = detection.is_blob_convex(blobs,0.30) # (blobs,min_convex)

            # draw circle around first blob while testing
            if (len(blobs) > 0) and testing:
                img.draw_circle(blobs[0].enclosing_circle())

                for blob in blobs:
                    print(blob.roundness())
                #print(blobs[0].roundness())
            '''

            # get if circle is detected in image
            # -- input params: image snapshot
            # -- output: T/F if any circles are in image
            is_circle = detection.is_circle(img,5000,testing) # (img,threshold,testing) -- higher threshold = more circular, send testing b/c drawing inside detection library (NEED TO FIX SO CONSISTENT ACROSS METHODS IF DRAWING HERE OR IN LIBRARY)

            # check if anything is too close (if object closer than STOP_MAX distance away
            # -- input params: set-up distance sensor, furthest distance from cam to STOP
            # -- output: T/F if anything is too close to camera
            is_too_close = detection.is_too_close(tof,STOP_MAX)

            # get the id of any april tag detected in the 36H11 family & in range of needed #'s based on # of possible messages detected (assumes only one is in field of view, takes first index of list from one snapshot, could adapt later to react to two)
            # -- input params: image snapshot, list of messages to send to brain (needed to know # of april tags needed) -- LIST OF MSGS should exclude any commands not triggered by an april tag
            # ----------------------------------- >>> for now, first (index 0 = 'n' = nothing), and last (last index = 'h' = dance AND move head) are not triggered by april tags, so exclude from inputted list
            # -------------------------------------------- >>> 'n' is sent if nothing in camera is detected, 'h' is sent if tennis ball is detected
            # -- output (int): 0 to (+) #'s -- for any april tag in designated family and within range of # of messages
            #          -1 -- april tag detected but not in desired family
            #          -2 -- no april tags detected at all
            # NOTE: remember to turn the boolean above (using_april_tags) to True if running the line below so lens has small enough frame size to have enough memory
            april_id = detection.get_april_tag(color_copy,msgs[1:len(msgs)-1]) # !!! end of range is exclusive so want to exclude last (6 = 7th) index -- only send msgs in range that are triggered by april tags, not msgs triggered by other things detected



            # --- DECIDE MESSAGE BASED ON SENSOR INFO ---
            # -------------------------------------------
            # possible sensor info:
            # is_tennis_color = T / F
            # is_blob_circle = T / F
            # is_blob_curved = T / F
            # is_circle = T / F ------- commented out right now b/c doesn't match location of circle to location of blob (so will say T if ANY circle is in camera even if not the right color)
            # is_too_close = T / F
            # april_id = integer 0 to n-1 where n = number of messages to be triggered by april tags, OR -1 if april tag not in desired range/family, OR -2 if no april tags detected at all
            # -------------------------------------------

            # POSSIBLE MESSAGES (from msgs list above)
            # msgs = ['n','s','f','r','l','d','h']

            # --- message ----- robot movement ---- current trigger -------- (can change the trigger by setting message = msgs[index desired message] if desired trigger(s) are True/proper values
            # --------------------------------------------------------------
            # --- 'n' ---------- do nothing ------ nothing (default) ------------------------------------- indicator led --------
            # --- 's' ------------ stop ------------- april tag 0 --OR-- if anything is <150mm to camera ----
            # --- 'f' ----------- forward ----------- april tag 1 --------------------------------------
            # --- 'r' ------------ right ------------ april tag 2 --------------------------------------
            # --- 'l' ------------- left ------------ april tag 3 --------------------------------------
            # --- 'd' ------------ dance ------------ april tag 4 --------------------------------------
            # --- 'h' ------- dance & move head ----- tennis ball --------------------------------------
            # ------------------------------------------------------------------------------------------

            # the variable 'message' initialized right AFTER the while True holds the one-character string to be sent to the brain
            # the order of if statements below determine what is ultimately sent -- whatever the last message is detected is sent


            # ----- APRIL TAGS -----
            # if april tag within range/family detected, set message to send to message related to april tag
            # CURRENTLY (given msgs = ['n','s','f','r','l','d','h']) these are the april tags from the 36H11 family to show for related messages (for an april tag within range/family shown, the april_id returned should be the same):
            # NOTE: if you aren't getting the message you expect (probably 'n' instead of desired), try holding the april tag further from the camera -- it is likely not within frame
            # -- april_id ----- message ----- robot movement ----
            # ----- 0 ----------- 's' ---------- stop -----------
            # ----- 1 ----------- 'f' --------- forward ---------
            # ----- 2 ----------- 'r' ---------- right ----------
            # ----- 3 ----------- 'l' ----------- left ----------
            # ----- 4 ----------- 'd' ---------- dance ----------
            # NOTE: the last message in the list above ('h' = dance AND move head) is triggered by a tennis ball shown, NOT an april tag
            if april_id >= 0:
                message = msgs[april_id+1] # index shifted one right from actual april id b/c first index of msgs is default 'n', assume all non-april-tag-triggered messages (from other things detected) are written AFTER in list msgs above, could write some code to have order not matter so part of msg is to be detected by april tag
            # ------------------------------------------

            # ----- TENNIS BALL ------------------------
            # if tennis ball is detected, tell robot to dance & move head
            # need all these params to filter out colors/shapes that are similar but not a tennis ball
            '''
            print(is_tennis_color, is_blob_circle, is_blob_curved)
            if is_tennis_color and is_blob_circle and is_blob_curved:
            '''
            # with update filtering method, instead of detecting blob color & shape then combining booleans to determine if tennis ball is detected in one line,
            # now have already done color & noise filtering earlier (color w/ binary using color threshold, and noise with erode & dilate w certain size to 'erase')
            # and then got a black & white image only showing white pixels where color was within the desired threshold, and black everywhere else
            # therefore, with the noise filtering, shapes can more easily & accurately be detected
            # so now, given the B&W image filtered for desired color, we just have to find if there is a circle in the filtered image to say whether a tennis ball is present
            # therefore, a tennis ball is defined by being:
            # ---- greenish-yellow (color threshold changes based on lighting)
            # ---- a circle (must have STRONG 'circleness' with threshold of 5000 [can change as input to fxn in main code above], and filtered for min radius 30 and max 90 px [can't change in main fxn, built-in to library fxn])
            if is_circle:
                message = msgs[len(msgs)-1] # last index = 'h'
            # -------------------------------------------

            # ----- DISTANCE SENSOR --------------------- (ANYTHING TO CLOSE TRIGGERS STOP)
            # toggle emergency stop so that if ANYTHING is too close, stop the robot
            # leave off if only want to stop if certain objects are too close
            if e_stop:
                if is_too_close:
                    message = msgs[1] # 's' = stop
                    #print("too close")
            # ------------------------------------------------------------------




            # ----------- TURN ON INDICATOR on-board LED color BASED ON MESSAGE --------------
            # at the beginning of the code where the message list is, a list of related leds is created right below
            # FROM ABOVE
            # ----- msgs = ['n','s','f','r','l','d','h'] # nothing, stop, forward, right, left, dance, move head AND dance
            # ----- leds = ['n','r','g','gb','gr','b','rgb'] # list of led colors to choose related to each message -- g = green, r = red, b = blue, gb = green-blue, gr = green-red, rb = red-blue, rgb = red-green-blue, n = none (no leds on)

            # the led at each list index will turn on when the message at that index in the msgs list is the ultimate message
            # (led is only turned on when message is FINAL, not right after detected -- so led shows only the message that is ultimately sent to the brain)

            # --- message ----- robot movement ---- current trigger ------------------------------------- indicator led -------(can change the trigger by setting message = msgs[index desired message] if desired trigger(s) are True/proper values
            # -----------------------------------------------------------------------------------------------------------------
            # --- 'n' ---------- do nothing ------ nothing (default) ----------------------------------------------------------
            # --- 's' ------------ stop ------------- april tag 0 --OR-- if anything is <150mm to camera ----- RED ------------
            # --- 'f' ----------- forward ----------- april tag 1 ------------------------------------------- GREEN -----------
            # --- 'r' ------------ right ------------ april tag 2 ----------------------------------------- GREEN-BLUE --------
            # --- 'l' ------------- left ------------ april tag 3 ------------------------------------------ GREEN-RED --------
            # --- 'd' ------------ dance ------------ april tag 4 --------------------------------------------- BLUE ----------
            # --- 'h' ------- dance & move head ----- tennis ball ------------------------------------------ WHITE (RGB) ------
            # -----------------------------------------------------------------------------------------------------------------

            detection.led_from_message(ledRed,ledGreen,ledBlue,message,msgs,leds)
            sleep(.05)
            # ------------------------------------------


        # --- send message ---
        # for when connected to brain
        # NOTE: change boolean at start of code ('testing') to True when using Nicla wirelessly (not connected to PC/IDE)
        if not testing:
            # if usb is connected, send serial message
            if (usb.isconnected()):
                usb.write(message) # message is type str
                #sleep(time_btwn_msgs)
        # for testing just w Nicla (not connected to brain)
        else:
            # for testing just w nicla
            print(message)
            #sleep(time_btwn_msgs)
        # -------------------

