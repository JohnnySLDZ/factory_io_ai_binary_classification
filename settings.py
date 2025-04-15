import numpy as np

# Device-specific calibration parameters:
# - Screen capture region coordinates
# - Linear regression coefficients (m,b) for claw position conversion
# (Different sets based on my PC and laptop screen size)
pc_coor = {
    "region_x": 650,
    "region_y": 270,
    "width": 550,
    "height": 550,
    "x_claw_m": 0.01102,
    "x_claw_b": 1.8525,
    "y_claw_m": 0.006617,
    "y_claw_b": 7.01875
}

laptop_coor = {
    "region_x": 768,
    "region_y": 240,
    "width": 650,
    "height": 650,
    "x_claw_m": 0.01075,
    "x_claw_b": 1.9077,
    "y_claw_m": 0.006394,
    "y_claw_b": 6.8195
}

# Color range for brown detection in HSV format
brown_low = np.array([15, 20, 20], np.uint8)
brown_high = np.array([60, 100, 100], np.uint8)

# Convert color ranges from 0-360/0-100 to OpenCV's HSV ranges (0-179/0-255)
brown_low[0] = np.interp(brown_low[0], [0, 360], [0, 179])
brown_low[1:] = np.interp(brown_low[1:], [0, 100], [0, 255])

brown_high[0] = np.interp(brown_high[0], [0, 360], [0, 179])
brown_high[1:] = np.interp(brown_high[1:], [0, 100], [0, 255])