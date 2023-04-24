# thresholds

# Define the min/max LAB values we're looking for
    # threshold input to img.find_blobs later
    # for RGB565 need each tuple to have 6 inputs
    # (l_lo, l_hi, a_lo, a_hi, b_lo, b_hi)
    # ^^^ mins & maxes for LAB L, A, B channels
    # get MANUALLY (easiest) by taking snapshot of thing then Tools > Machine Vision > Threshold Editor

thresholdsOrange = (33, 55, 29, 58, 24, 70)
thresholdsTennisBall = (31, 92, -24, -3, 24, 41)
thresholdsTennisBall2 = (37, 91, -14, 3, 15, 44)
thresholdsTennisBall3 = (0, 100, -128, 5, 14, 41) # didn't change L as suggested by OpenMV forum (at AR)
thresholdsTennisBall4 = (0, 100, -24, -4, 29, 48) # didn't change L as suggested by OpenMV forum (in Blake)
thresholdsTennisBall5 = (0, 100, -18, 15, 21, 48) # L full range, in Blake, with SMALLER QQVGA frame that usually use in main.py
thresholdsTennisBall6 = (0, 100, -18, 5, 17, 44) # L full range, in Blake, smaller QQVGA frame, readjusted after running main.py...some other adjustment I can't remember?
thresholdsTennisBall7 = (0, 100, -22, -2, 17, 44) # narrowed A to exclude noise

STOP_MAX = 150 #[mm]
