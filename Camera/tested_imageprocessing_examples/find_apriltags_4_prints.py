# Rose Kitz
# adapated from OpenMV IDE AprilTags Example (meant for OpenMV M7 cam, but works on Arduino Nicla Vision :) )
# last updated Mon 4/10/23

import sensor, image, time, math, pyb


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
# the two commands below came with the example, but aren't supported by the Nicla Vision board. Still trying to figure out how to do this with the Nicla Vision, but code works fine for now so maybe not necessary
#sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
#sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...

# initiate LEDs to indicate if april tag detected or not
ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led
ledBlue = pyb.LED(3)

# list of discrete commands to send to brain
# just use index (0, 1, 2, 3, etc.) as the april tag id
# (april tag ids go from 0 - whatever #, so say first command in list has id=0, second has id=1, etc., instead of making a list of ids...)
commands = ['f', 'b', 'l', 'r', 's'] # forward, backward, left, right, stop
# combos of leds to turn on for diff commands (extra indicator, and to test externally without wifi and without delay)
leds_for_commands = [[ledGreen],[ledBlue],[ledBlue,ledGreen],[ledBlue,ledRed],[ledRed]]
# initialize message to send if no tag detected (no command, so tell brain to do nothing)
msg = 'do nothing'


# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# The apriltag code supports up to 6 tag families which can be processed at the same time.
# Returned tag objects will have their tag family and id within the tag family.

tag_families = 0
#tag_families |= image.TAG16H5 # comment out to disable this family
#tag_families |= image.TAG25H7 # comment out to disable this family
#tag_families |= image.TAG25H9 # comment out to disable this family
#tag_families |= image.TAG36H10 # comment out to disable this family
tag_families |= image.TAG36H11 # comment out to disable this family (default family)
#tag_families |= image.ARTOOLKIT # comment out to disable this family

# What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
# a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
# is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positve
# rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
# reason to use the other tags families just use TAG36H11 which is the default family.

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

# function to get message for detected april tags (right now only return one message...so most last tag in tags, but for now we shouldn't ever have two tags detected at the same time
# could adapt to send other info like rotation if want to know direction of robot relative to tag
def get_msg_from_tags(snap):
    # reset msg for fresh 'buffer' in case nothing is detected in next 500ms so the old value isn't returned
    message = 'do nothing' # local var for message, say 'do nothing' if no tag detected or not one of desired tag fam/ids

    # loop through tags (detect in line below)
    for tag in img.find_apriltags(families=tag_families): # defaults to TAG36H11 without "families".
            img.draw_rectangle(tag.rect(), color = (255, 0, 0))
            img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))

            # get useful info about tag detected
            tag_fam = family_name(tag)
            tag_id = tag.id()
            rotation = (180 * tag.rotation()) / math.pi

            # if detected tag is within desired family and has an id within the range of the commands established above, assign a message
            if family_name(tag) == "TAG36H11" and tag_id >=0 and tag_id<=(len(commands)-1):
                ledRed.off()
                on_leds(leds_for_commands[tag_id]) # turn on leds to indicate this command
                message = commands[tag_id]
    return message


# function to turn on multiple leds from a list at the 'same' time
def on_leds(leds):
    for led in leds:
        led.on()
# function to turn off all leds
def off_all_leds():
    ledBlue.off()
    ledRed.off()
    ledGreen.off()

# initialize tracking var for time
old_tick = time.ticks_ms()

ledRed.on()
# loop to take snapshots w cam and interpret/send data as needed
while(True):

    # capture frames as fast as possible
    img = sensor.snapshot()

    # send (and calculate before) only every 500ms
    if time.ticks_diff(time.ticks_ms(),old_tick) > 500:
        # reset led to red once new 500ms block starts
        off_all_leds()
        ledRed.on()

        msg = get_msg_from_tags(img)
        # send direction to move based on most recent april tag seen in the last 500ms
        print(msg)

        # reset old tick to start new 500ms timer
        old_tick = time.ticks_ms()

    #print(clock.fps())
