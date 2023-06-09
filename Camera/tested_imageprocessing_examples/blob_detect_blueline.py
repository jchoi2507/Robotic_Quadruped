# program to detect a blue line
# and send message which way to turn and by how many degrees in order to follow the line forward


import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time

sensor.reset() # Resets the sensor
sensor.set_pixformat(sensor.RGB565) # Sets the sensor to RGB
sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
sensor.set_vflip(True) # Flips the image vertically
sensor.set_hmirror(True) # Mirrors the image horizontally
sensor.skip_frames(time = 2000) # Skip some frames to let the image stabilize

# set pixel positions for image to compare what robot sees vs. its position
# resolution of image is 320x240 px, so with origin at top left, (320,0) is top right, (320,240) is bottom right, (0,240) is bottom left
width = 320
height = 240
center_x = width/2
center_y = height/2


# Define the min/max LAB values we're looking for
# threshold input to img.find_blobs later
# for RGB565 need each tuple to have 6 inputs
# (l_lo, l_hi, a_lo, a_hi, b_lo, b_hi)
# ^^^ mins & maxes for LAB L, A, B channels
# get MANUALLY (easiest) by taking snapshot of thing then Tools > Machine Vision > Threshold Editor
thresholdsClementine = (11, 63, 16, 54, 12, 68)
thresholdsBlueLine = (9, 31, 8, 40, -49, -25)

ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led

clock = time.clock() # Instantiates a clock object

while(True):
    clock.tick() # Advances the clock
    img = sensor.snapshot() # Takes a snapshot and saves it in memory

    # Find blobs with a minimal area of 50x50 = 2500 px
    # Overlapping blobs will be merged
    # ?? not sure if need to edit areaThreshold
    blobs = img.find_blobs([thresholdsBlueLine], area_threshold=2500, merge=True)

    # if a blob is found, find the biggest blob and decide what to do based on its properties
    if len(blobs) > 0:
        # find the 'biggest' blob of all currently found (to filter out smaller objects, not sure if this will work)
        biggest_blob = blobs[0]
        for blob in blobs:
            if blob.pixels() > biggest_blob.pixels():
                biggest_blob = blob

        # Draw biggest blob
        # (x,y) coords of centroid of blob
        x = biggest_blob.cx()
        y = biggest_blob.cy()
        rot = biggest_blob.rotation_deg()

        # from testing, rot=0 is horiz pointing left, rot=90 is pointing up, rot=180 is horiz pointing right
        # dog's frame of reference is pointing forward is 0 deg
        deg_from_line = 90 - rot # degrees of dog (facing forward frame of reference) from line it needs to follow // (+) is line to left, (-) is line to right
        deg_error = 3 # let robot move forward if within 3 deg rot from either side of line so not always turning
        if rot < 90 - deg_error:
            print("turn left",deg_from_line,"degrees")
        elif rot > 90 + deg_error:
            print("turn right",abs(deg_from_line),"degrees")
        else:
            print("on track! keep going forward!")

        # Draw a rectangle where the blob was found
        img.draw_rectangle(biggest_blob.rect(), color=(0,255,0))
        # Draw a cross in the middle of the blob
        img.draw_cross(x, y, color=(0,255,0))

        # how to deal w corners??? could draw line with points of diff color at corners would make much easier but then robot isn't doing as much work...
        # draw curved line (Lol)
        # question of how much work can we do on our side to control the environment to ease the programming of the robot...but Spot is very automated

        # for now assume turning will be inaccurate
        # make a lane path to follow rather than a signular line
        # can demo can move with april tags
        # move automatically with boundaries
        # -- can delete testing serial file


    ''' change this stuff to external leds far from cam so don't affect the colors that it sees
    # Turn on green LED if a blob was found
    if len(blobs) > 0:
        ledGreen.on()
        ledRed.off()
    else:
    # Turn the red LED on if no blob was found
        ledGreen.off()
        ledRed.on()
    '''

    pyb.delay(50) # Pauses the execution for 50ms
    #print(clock.fps()) # Prints the framerate to the serial console
