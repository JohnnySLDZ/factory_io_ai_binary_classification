from opcua import Client, ua
import cv2
import sys
import numpy as np
import pyautogui
import os
import pandas as pd
import tensorflow as tf
from functions import write_value_int, write_value_bool, write_value_float, read_input_value, new_round
from settings import pc_coor, laptop_coor, brown_low, brown_high

model = tf.keras.models.load_model("boxes_model_75_1,00.keras")

# Class labels for information on model predictions
class_labels = {0: "code", 1: "no_code"}

def preprocess_image(image):
    """Prepare image for model prediction by:
    1. Converting to grayscale
    2. Resizing to 128x128
    3. Normalizing pixel values
    4. Adding batch dimension"""
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    resized_image = cv2.resize(gray_image, (128, 128))
    normalized_image = resized_image / 255.0

    input_image = np.expand_dims(normalized_image, axis=-1)
    input_image = np.expand_dims(input_image, axis=0)
    return input_image

def predict_image(image):
    """Run model prediction on preprocessed image Returns:
    -predicted_class (0 or 1)
    -confidence score (0-1)"""
    input_image = preprocess_image(image)
    prediction = model.predict(input_image)
    predicted_class = 1 if prediction > 0.5 else 0
    confidence = prediction[0][0] if predicted_class == 1 else 1 - prediction[0][0]
    return predicted_class, confidence

def predict_coor(client):
        # CAPTURE SCREEN REGION
        screenshot = pyautogui.screenshot(region=(pc_coor["region_x"], pc_coor["region_y"], pc_coor["width"], pc_coor["height"]))
        screenshot = np.array(screenshot) 

        # Convert to HSV and apply color mask to detect brown objects
        screenshot_hsv = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV) 
        mask = cv2.inRange(screenshot_hsv, brown_low, brown_high)

        # Apply erosion to remove small noise pixels
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        screenshot_copy = screenshot.copy()

        if len(contours) > 0:

            # Get dimensions from the most recent measurements file
            try:
                measures_folder = os.listdir("measures")
                df = pd.read_csv(f"measures/measures_{len(measures_folder)}.csv")
                w_principal = df['width'].iloc[0]
                h_principal = df['height'].iloc[0]
            except FileNotFoundError:
                print("File Not Found Define an Area First")
                write_value_bool(client, 'ns=3;s="SISTEM"', False)
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
                write_value_bool(client, 'ns=3;s="SISTEM"', False)
                sys.exit(1) 

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
                        
                        #boxes += num_rects_x * num_rects_y
                        for i in range(num_rects_x):
                            for j in range(num_rects_y):
                                # Calculate box coordinates
                                start_x = x + i * w_principal
                                start_y = y + j * h_principal
                                end_x = start_x + w_principal
                                end_y = start_y + h_principal
                                center_x = start_x + round((end_x - start_x)/2)
                                center_y = start_y + round((end_y - start_y)/2)

                                # Extract and classify each sub-box
                                contour_mask = np.zeros_like(screenshot)
                                contour_mask[start_y:end_y, start_x:end_x] = screenshot[start_y:end_y, start_x:end_x]
                                predicted_class, confidence = predict_image(contour_mask)
                                
                                # Red rectangle for "no_code", green for "code"
                                color = (0, 0, 255) if predicted_class == 1 else (0, 255, 0)
                                cv2.rectangle(screenshot_copy, (start_x, start_y), (end_x, end_y), color, 5)
                                
                                # Convert pixel coordinates to robot coordinates
                                x_claw = center_x * pc_coor["x_claw_m"] + pc_coor["x_claw_b"]
                                y_claw = center_y * pc_coor["y_claw_m"] + pc_coor["y_claw_b"]

                                # Send information to OPC UA server
                                write_value_bool(client, 'ns=3;s="CONFIG_VARS"."MOVE_2_BOX"', True)
                                write_value_float(client, 'ns=3;s="COORDS"."BOX_X"', x_claw)
                                write_value_float(client, 'ns=3;s="COORDS"."BOX_Y"', y_claw)
                                write_value_int(client, 'ns=3;s="COORDS"."CODE"', predicted_class)
                                
                                # Wait for robot to complete movement or user interrupt
                                while True:
                                    movement = read_input_value(client, 'ns=3;s="CONFIG_VARS"."MOVE_2_BOX"')
                                    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
                                    cv2.resizeWindow("image", 300, 300)
                                    cv2.imshow("image", screenshot_copy)
                                    cv2.namedWindow("image_raw", cv2.WINDOW_NORMAL)
                                    cv2.resizeWindow("image_raw", 300, 300)
                                    cv2.imshow("image_raw", mask)
                                    if not movement or cv2.waitKey(1) & 0xFF == ord('q'):
                                        break
                                    else:
                                        print(".") # Movement in progress indicator
                                    
                                cv2.destroyAllWindows
        # Final system response
        write_value_bool(client, 'ns=3;s="CONFIG_VARS"."PY_RESPONSE"', True)


client = Client("opc.tcp://192.168.0.1:4840", timeout=10)
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
            predict_coor(client)
            

finally:
    client.disconnect()