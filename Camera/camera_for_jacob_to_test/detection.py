import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time

# ??? do I need the imports in here? or ok if just in the main file?

def set_sensors(sensor):
    sensor.reset() # Resets the sensor
    sensor.set_pixformat(sensor.RGB565) # Sets the sensor to RGB
    sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
    sensor.set_vflip(True) # Flips the image vertically
    sensor.set_hmirror(True) # Mirrors the image horizontally
    sensor.skip_frames(time = 2000) # Skip some frames to let the image stabilize

def command_from_blobs(clock,img,thresholds,ledR,ledG):
    # message is default 'forward' -- only stop (send 's') if see orange
    msg = 'f'

    # Find blobs with a minimal area of 50x50 = 2500 px
    # Overlapping blobs will be merged
    # ?? not sure if need to edit areaThreshold
    blobs = img.find_blobs(thresholds, area_threshold=2500, merge=True)

    # if blob found, change message to 'stop', draw blob on screen (get rid of for real dog, only for testing w IDE), turn on green led
    if len(blobs) > 0:
        msg = 's'

        # Turn on green LED if a blob was found
        ledG.on()
        ledR.off()

        # Draw blobs (ONLY FOR TESTING)
        for blob in blobs:
            # Draw a rectangle where the blob was found
            img.draw_rectangle(blob.rect(), color=(0,255,0))
            # Draw a cross in the middle of the blob
            img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))

    # turn on red led if blob not found
    else:
        # Turn the red LED on if no blob was found
        ledG.off()
        ledR.on()

        pyb.delay(50) # Pauses the execution for 50ms
        #print(clock.fps()) # Prints the framerate to the serial console
        #print("x", blob.cx(), "y", blob.cy())

    return msg
