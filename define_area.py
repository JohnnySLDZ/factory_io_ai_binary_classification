import cv2
import numpy as np
import pyautogui
import pandas as pd
import os
from opcua import Client, ua
from functions import read_input_value, write_value_bool
from settings import pc_coor, laptop_coor, brown_low, brown_high

# Minimum contour area to consider valid detection (noise reduction)
min_area = 500  

x, y, w_principal, h_principal = (0,0,0,0)

def define_area():
    # CAPTURE SCREEN REGION
    screenshot = pyautogui.screenshot(region=(pc_coor["region_x"], pc_coor["region_y"], pc_coor["width"], pc_coor["height"]))
    screenshot = np.array(screenshot) 

    # Convert to HSV and apply color mask to detect brown objects
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)  
    mask = cv2.inRange(screenshot, brown_low, brown_high)

    # Apply erosion to remove small noise pixels
    kernel = np.ones((5, 5), np.uint8) 
    mask = cv2.erode(mask, kernel, iterations=1) 
    
    # Find contours of detected objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate areas of all detected contours and filter by minimum size
    areas = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            areas.append(area)

    if len(areas) == 1: # Proceed only if exactly one valid object found
        area_principal = min(areas)
        index_area_principal = areas.index(area_principal)
        # Get bounding rectangle coordinates
        x, y, w_principal, h_principal = cv2.boundingRect(contours[index_area_principal])
        cv2.rectangle(screenshot, (x, y), (x + w_principal, y + h_principal), (0, 255, 0), 2)
        cv2.putText(screenshot, f"{x}, {y}, {w_principal}, {h_principal}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Create measures directory if it doesn't exist
        if not os.path.exists("measures"):
            os.makedirs("measures")
        folder = os.listdir("measures")

        # Create new CSV file with bounding box measurements
        df = pd.DataFrame(columns=['x', 'y', 'width', 'height'])
        df.loc[0] = [x, y, w_principal, h_principal]
        n = len(folder) + 1
        df.to_csv("measures/measures_" + str(n) + ".csv")
    else:
        print("error")
    
    # Send acknowledgment signal via OPC UA
    write_value_bool(client, 'ns=3;s="CONFIG_VARS"."PY_RESPONSE"', True)
    # RESULT DISPLAY
    cv2.imshow("Real Time Detection", screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

client = Client("opc.tcp://192.168.0.1:4840")
try:
    client.connect()

    root = client.get_root_node()
    print("Objects root node is: ", root)
    value = False
    # Main control loop
    while True:
        # Check OPC UA server for instruction
        value = read_input_value(client, 'ns=3;s="CONFIG_VARS"."INSTRUCTION_2_PY"')
        if value:
            define_area()
            break

finally:
    client.disconnect()