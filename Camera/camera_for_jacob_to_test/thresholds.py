# thresholds

# Define the min/max LAB values we're looking for
    # threshold input to img.find_blobs later
    # for RGB565 need each tuple to have 6 inputs
    # (l_lo, l_hi, a_lo, a_hi, b_lo, b_hi)
    # ^^^ mins & maxes for LAB L, A, B channels
    # get MANUALLY (easiest) by taking snapshot of thing then Tools > Machine Vision > Threshold Editor

thresholdsOrange = (33, 55, 29, 58, 24, 70)
