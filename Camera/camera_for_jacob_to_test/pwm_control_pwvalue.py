# PWM Control Example

# program makes two micro servos spin 0-180 deg back and forth while connected to Nicla vision

import time
from pyb import Pin, Timer

class PWM():
    def __init__(self, pin, tim, ch):
        self.pin = pin
        self.tim = tim
        self.ch = ch;

pwms = {
    'PWM1' : PWM('PE12', 1, 1),
    'PWM2' : PWM('PE11', 1, 2),
#   'PWM3' : PWM('PA9',  1, 2),
    'PWM3' : PWM('PA10', 1, 3),
    'PWM4' : PWM('PE14', 1, 4),
    'PWM5' : PWM('PB8',  4, 3),
    'PWM6' : PWM('PB9',  4, 4),
}
'''
# Generate a 1KHz square wave with 50% cycle on the following PWM.
for k, pwm in pwms.items():
    tim = Timer(pwm.tim, freq=1000) # Frequency in Hz
    ch  = tim.channel(pwm.ch, Timer.PWM, pin=Pin(pwm.pin), pulse_width_percent=50)

while (True):
    time.sleep_ms(1000)

   '''
# tested on scope, all pins above work
# 1.5ms pulse every 6 ms 90deg
# 1.0-2.0ms

# pick freq want
# Chris said freq 25-50hz doens't really matter as long as pulse width is correct
# change freq to change how often change position
#change pulse width to change position
# will need to calibrate
# run at 1.0ms pulse width, run at 2.0, do linear in between

# pulse widths for 0 and 180 deg on servo
start_pw = 325 # can go before 0deg, to 250 pw
end_pw = 2000
range_pw = end_pw - start_pw

port_1 = PWM('PB8', 4, 3)
tim_1 = Timer(port_1.tim, freq=15)
ch_1  = tim_1.channel(port_1.ch, Timer.PWM, pin=Pin(port_1.pin), pulse_width=start_pw)

port_2 = PWM('PE11', 1, 2)
tim_2 = Timer(port_2.tim, freq=15)
ch_2  = tim_2.channel(port_2.ch, Timer.PWM, pin=Pin(port_2.pin), pulse_width=start_pw)


# for freq=15
# pw = 2000 for 180
# pw = 250 for end
# pw = 1250 160deg
#print("servo 1:", ch_1.pulse_width())
print("servo 2:", ch_2.pulse_width())

while True:
    for i in range(range_pw):
        ch_1.pulse_width(start_pw+i)
        ch_2.pulse_width(start_pw+i)
    time.sleep(1)
    for j in range(range_pw):
        ch_1.pulse_width(end_pw-i)
        ch_2.pulse_width(end_pw-i)
    time.sleep(1)
