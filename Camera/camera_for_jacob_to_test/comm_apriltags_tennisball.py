# Rose Kitz
# Fri 4/21/23
# ME35
# Program to detect april tags, a tennis ball, and distance using the Arduino Nicla Vision cam to direct quadruped robot
# currently, april tag ids from the 36H11 family in the range from 0 to 2 can be detected, because only 3 messages are necessary to direct the robot
# when an april tag is detected, the related message for how the robot should move is sent over serial to the brain (Raspi). If nothing or a
# hold the phone with april tags about 1ft away from cam -- only tags 0 to 2 will show an led color, any others or nothing will cause nothing to happen ('n' is sent)

# I created my own library, 'detection,' to store the image processing code, to simply receive outputs of T/F for if certain colors/objects are detected, or #s for things like april tags

# NOTE: You can easily/quickly change the messages you want to send from the camera to the brain for any number of april tags you want
# Simply go to line 79 below and add one-character strings as elements to the 'msgs' list to add what strings can be sent over serial to the RasPi
# Then, on line 80, add strings as elements to choose what led color you want to correspond to each action.
# The code is listed in the comment on that line, only 6 color combinations are possible with the on-board led and must be entered as lowercase strings in the order mentioned in the code.
# To turn all leds off, enter 'n'.
# The index # of the message and its corresponding color is then one more than the april tag id # that will trigger that message (i.e. 's' at index 1 in msgs = april tag id 0)
# since it was necessary to add a 'nothing' command to the list of messages to distinguish between when stop is called and when nothing is actually desired to happen with an april tag


# TODO:
# clean up drawings so only if testing
# get a few more thresholds for tennis ball to use for diff lighting (eventually, make a calibration code based on lighting)
# -------------------------------------------------------------------------------

# import the fxns for diff methods of detection and keep this simple communication code?
# get the image here and use as param for function within detection file then get direction as result
# should I be doing classes???
# will having separate files on board take up more space than all code in one file?
# like would types of the class be orange, apple, april tag1, apriltag2, etc? but not sure if really need classes for that...
# is this even helpful if I'm not doing it the right/most efficient way??? maybe I should just ask jacob the cs major what he thinks how to organize it

#?? add stuff from this april tags version to thresholds


from pyb import USB_VCP, LED # pyb is for board-related functions

# for distance sensor
from machine import I2C
from vl53l1x import VL53L1X

# !!! change to from ___ import __
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
from time import sleep, clock # Import module for tracking elapsed time
import math

# import detection stuff
import detection # self-created library
from thresholds import thresholdsOrange, thresholdsTennisBall7, STOP_MAX

# --- set-up leds, clock ---
# ??? ctrl leds from here once get final message, or within library? I guess harder to change on the fly if in library but then simpler code here...
ledRed = LED(1) # Initiates the red led
ledGreen = LED(2) # Initiates the green led
ledBlue = LED(3) # Initiates the blue led

clock = clock() # Instantiates a clock object
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
# NOTE: toggle these depending on what detection methods using (need to do this so code changes frame size so enough memory on Nicla)
using_april_tags = True
using_circles = True # also need qqvga for circle detection

# toggle to change if want robot to stop if ANYTHING is too close, no matter what the close object is
e_stop = True

# --- set up detection stuff ---
# ??? could this be done inside detection library ???
tof = detection.set_sensors(sensor,using_april_tags,using_circles) # ??? should I always setup tof in case need? b/c seems more efficient than initialize every loop of while True when call command, but also seems inefficient to setup here then pass along later if needed...
# list of discrete commands to send to brain
# just use index (0, 1, 2, 3, etc.) as the april tag id
# (april tag ids go from 0 - whatever #, so say first command in list has id=0, second has id=1, etc., instead of making a list of ids...)

# -------------------- CHANGE DESIRED MESSAGES & RELATED LEDS HERE -----------------------------------
msgs = ['n','s','f','r','l','d','h'] # nothing, stop, forward, right, left, dance, move head AND dance
leds = ['n','r','g','gb','gr','b','rgb'] # list of led colors to choose related to each message -- g = green, r = red, b = blue, gb = green-blue, gr = green-red, rb = red-blue, rgb = red-green-blue, n = none (no leds on)

# ?? should do in 2d array? could be more edge-case friendly to check that these are same length...but I trust myself to write the code hopefully, and take care of incorrect characters but not possible b/c no user input only I hardcoding and I would find error
# ??? should names be diff btwn here and libraries???
# -----------------------

# loop forever
while True:

    # initialize message to edit based on info from sensors
    message = msgs[0] # default is nothing, led should be off

    clock.tick() # Advances the clock

    # take image and save in memory
    img = sensor.snapshot()

    if using_circles:
        img = sensor.snapshot().lens_corr(1.8)

     #make image b&w and eliminate noise
    img.binary([thresholdsTennisBall7])
    img.erode(3,3) # from testing realized want smaller threshold for erode and larger for dilate so lots of pixels are deleted, but only bigger clusters are expanded (not small noise left expanded)
    img.dilate(3,15)


    # --- DETECT STUFF FROM SENSORS ---
    # !!! if using april tags remember to change boolean above so cam resolution is set small enough to have enough memory
    '''
    # get True/False if image snapshot has tennis ball color in it, return blobs to find characteristics of later
    # -- input params: image snapshot, color thresholds
    # -- outputs: T/F if blob is within color thresholds, blobs object
    is_tennis_color, blobs = detection.is_color(img,[thresholdsTennisBall7]) # add more thresholds imported inside [] if applicable

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
    april_id = detection.get_april_tag(img,msgs[1:len(msgs)-1]) # !!! end of range is exclusive so want to exclude last (6 = 7th) index -- only send msgs in range that are triggered by april tags, not msgs triggered by other things detected



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
    # ------------------------------------------


    # --- send message ---
    time_btwn_msgs = .1 # [s]
    # for when connected to brain
    # NOTE: change boolean at start of code ('testing') to True when using Nicla wirelessly (not connected to PC/IDE)
    if not testing:
        # if usb is connected, send serial message
        if (usb.isconnected()):
            usb.write(message) # message is type str
            sleep(time_btwn_msgs)
    # for testing just w Nicla (not connected to brain)
    else:
        # for testing just w nicla
        print(message)
        sleep(time_btwn_msgs)
    # -------------------

