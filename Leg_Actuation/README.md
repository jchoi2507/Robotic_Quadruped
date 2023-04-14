## Explanation:  

All txt files are angles. "MP" means angles for micropython.   
"R/L" means right/left, "1/2" means 1st/2nd joint of each leg.   
"Dog Leg Control" is an Arudino file.   
"RP2040_ServoTest" is Nano RP2040 micropython file. This code controls all the legs at once.   
**R1L2** is the code drives 1st right and 2nd left legs   
**R2L1** is the code drives 2nd right and 1st left legs

PWM Library Documentation: https://docs.micropython.org/en/latest/library/machine.PWM.html
Servo PWM Conversions:

500000 ns — 0 degrees
1000000 ns — 45 degrees
1500000 ns — 90 degrees
2000000 ns — 135 degrees
2500000 ns — 180 degrees
