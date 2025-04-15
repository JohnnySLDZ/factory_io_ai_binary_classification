import cv2
import numpy as np
import pyautogui
import pandas as pd
import os
from opcua import Client, ua
from functions import read_input_value, write_value_bool, new_round
from settings import pc_coor, laptop_coor, brown_low, brown_high

# Output folder for captured images
destiny_folder_location = "dataset/no_code"

def take_sample():
    for _ in range(5):
        # CAPTURE SCREEN REGION
        screenshot = pyautogui.screenshot(region=(pc_coor["region_x"], pc_coor["region_y"], pc_coor["width"], pc_coor["height"]))
        screenshot = np.array(screenshot) 

        # Convert to HSV and apply color mask to detect brown objects
        screenshot_hsv = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(screenshot_hsv, brown_low, brown_high)

        # Apply erosion to remove small noise pixels
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
       
        # Find external contours of detected objects
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

        if len(contours) > 0:
            # Get dimensions from the most recent measurements file
            try:
                measures_folder = os.listdir("measures")
                df = pd.read_csv(f"measures/measures_{len(measures_folder)}.csv")
                w_principal = df['width'].iloc[0]
                h_principal = df['height'].iloc[0]
            except FileNotFoundError:
                print("File Not Found Define an Area First")

                return 1
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
                return 1 

            # Process each detected contour
            for contour in contours:
                    # Divide detected object into sub-rectangles based on reference measurements
                    x, y, w, h = cv2.boundingRect(contour)
                    # Calculate how many sub-rectangles fit in detected object
                    num_rects_x = new_round(w / w_principal)
                    num_rects_y = new_round(h / h_principal)

                    if num_rects_x >= 1 and num_rects_y >= 1:
                        # Adjust reference dimensions based on actual detection
                        w_principal = int(w / num_rects_x)
                        h_principal = int(h / num_rects_y)
                        
                        for i in range(num_rects_x):
                            for j in range(num_rects_y):
                                start_x = x + i * w_principal
                                start_y = y + j * h_principal
                                end_x = start_x + w_principal
                                end_y = start_y + h_principal
                                
                                images_folder = os.listdir(destiny_folder_location)

                                contour_mask = np.zeros_like(screenshot)
                                
                                contour_mask[start_y:end_y, start_x:end_x] = screenshot[start_y:end_y, start_x:end_x]

                                # For each sub-rectangle:
                                # Save cropped and resized image (224x224 grayscale)
                                resized_image = cv2.resize(contour_mask, (224, 224))
                                resized_image_gray = cv2.cvtColor(resized_image, cv2.COLOR_RGB2GRAY)
                                n = len(images_folder)+1
                                cv2.imwrite(destiny_folder_location + "/cap_" + str(n) + ".jpg", resized_image_gray)
    return 0

client = Client("opc.tcp://192.168.0.1:4840")
try:
    client.connect()

    if not os.path.exists(destiny_folder_location):
        os.makedirs(destiny_folder_location)
    
    root = client.get_root_node()
    print("Objects root node is: ", root)
    value = False
    # Main control loop
    while True:
        images_folder = os.listdir(destiny_folder_location)
        if len(images_folder) >= 50:
                print("samples_taken")
                write_value_bool(client, 'ns=3;s="SISTEM"', False)
                break
        # Check OPC UA server for instruction
        value = read_input_value(client, 'ns=3;s="CONFIG_VARS"."INSTRUCTION_2_PY"')
        if value:
            if take_sample() == 0:
                # Send response back to server
                write_value_bool(client, 'ns=3;s="CONFIG_VARS"."PY_RESPONSE"', True)
            else:
                write_value_bool(client, 'ns=3;s="SISTEM"', False)
                break
            
finally:
    client.disconnect()