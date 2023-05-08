# Untitled - By: rckch - Fri Mar 31 2023

import pyb # module for board-related functions (all sensors besides camera?)
import sensor # module for sensor-related functions (just camera)
import image # module w machine vision algorithms

redLED = pyb.LED(1)
blueLED = pyb.LED(3)

sensor.reset() # initialize camera sensor
sensor.set_pixformat(sensor.RGB565) # set sensor to RGB
sensor.set_framesize(sensor.QQVGA) # set resolution to 320x240 px // or QQVGA for smaller to rep when actual main.py is running
sensor.set_vflip(True) # flip image vertically
sensor.set_hmirror(True) # mirror image horizontally

#redLED.on()
sensor.skip_frames(time = 2000) # skip some frames to let image stabilize

redLED.off()
#blueLED.on()

print("You're on camera!")

img = sensor.snapshot()

stats = img.get_statistics()
print("l max:", stats.l_max())
print("l min:", stats.l_min())
print("l avg:", stats.l_mean())

# now go to threshold editor and find thresholds that encapsulate ball


blueLED.off()
print("Done! Reset the camera to see the saved image.")
