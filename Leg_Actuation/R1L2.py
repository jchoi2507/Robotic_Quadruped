from time import sleep
from machine import Pin,PWM

# Setting up ports and pwm drive
R1_1 = PWM(Pin(26)) # "R1_1" means 1st right leg's 1st joint
R1_1.freq(50)
R1_2 = PWM(Pin(27))
R1_2.freq(50)
L2_1 = PWM(Pin(5)) # "L2_1" means 2nd left leg's 1st joint
L2_1.freq(50)
L2_2 = PWM(Pin(21))
L2_2.freq(50)

# Loading "angles" for leg's movement
angle1R = [7361,7378,7350,7293,7223,7161,7126,7123,7148,7195,7258,7328,7397,7464,7530,7597,7665,7732,7797,7862,7932,8011,8101,8205,8330,8473,8626,8776,8906,9000,9000,8930,8862,8795,8729,8665,8601,8538,8476,8415,8354,8295,8236,8178,8121,8065,8009,7954,7900,7847,7794,7743,7692,7642,7593,7545,7497,7451,7406,7361
]
angle2R = [7627,7682,7830,8046,8298,8545,8749,8888,8970,9000,8990,8958,8925,8900,8876,8847,8814,8782,8757,8731,8685,8599,8463,8269,8010,7701,7377,7079,6845,6711,6711,6779,6844,6905,6963,7019,7071,7120,7167,7211,7253,7292,7329,7364,7396,7426,7454,7480,7504,7525,7545,7562,7577,7590,7601,7611,7618,7623,7626,7627
]
angle1L = [2639,2622,2650,2707,2777,2839,2874,2877,2852,2805,2742,2672,2603,2536,2470,2403,2335,2268,2203,2138,2068,1989,1899,1795,1670,1527,1374,1224,1094,1000,1000,1070,1138,1205,1271,1335,1399,1462,1524,1585,1646,1705,1764,1822,1879,1935,1991,2046,2100,2153,2206,2257,2308,2358,2407,2455,2503,2549,2594,2639
]
angle2L = [2373,2318,2170,1954,1702,1455,1251,1112,1030,1000,1010,1042,1075,1100,1124,1153,1186,1218,1243,1269,1315,1401,1537,1731,1990,2299,2623,2921,3155,3289,3289,3221,3156,3095,3037,2981,2929,2880,2833,2789,2747,2708,2671,2636,2604,2574,2546,2520,2496,2475,2455,2438,2423,2410,2399,2389,2382,2377,2374,2373
]

# Drive the legs
while True:
    for i in range(len(angle1R)-1):
        R1_1.duty_u16(angle1R[i])
        R1_2.duty_u16(angle2R[i])
        L2_1.duty_u16(angle1L[i])
        L2_2.duty_u16(angle2L[i])
        sleep(0.01)