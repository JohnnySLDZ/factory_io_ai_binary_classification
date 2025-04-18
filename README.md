# Industrial AI with Python: CNN in FactoryIO + TIA Portal | OPC-UA Communication

## Implementation of a binary classification model for a production line using FactoryIO, Tia Portal and Python

## Description
This project is the implementation of a Convolutional Neural Network (CNN) to automatically identify and sort marked vs. unmarked boxes using a Pick & Place XYZ system in FactoryIO. The system communicates Siemens TIA Portal with FactoryIO and Python via an OPC UA server, bridging AI and industrial PLC control.

## Explanation Video⬇️⬇️⬇️:  
[![Alt text](https://img.youtube.com/vi/VSK87Z9wKWo/0.jpg)](https://youtube.com/shorts/VSK87Z9wKWo)

<[Video](https://youtube.com/shorts/VSK87Z9wKWo)>

## Video Demo⬇️⬇️⬇️:  
[![Alt text](https://img.youtube.com/vi/g0u7S8w8YA4/0.jpg)](https://www.youtube.com/watch?v=g0u7S8w8YA4)

<[Video](https://www.youtube.com/watch?v=g0u7S8w8YA4)>

## This project consists of three parts, each with its own Python and FactoryIO files, along with a folder containing the TIA Portal project:

### Project
This is central part of project, is organized into three core components:
- `project.py`: This Python script waits for a signal from TIA Portal, captures an image of boxes on the conveyor, processes the image to extract individual boxes with their coordinates, uses a pre-trained CNN model to classify each box, and finally sends the prediction results and coordinates back to TIA Portal.
- `project.factoryio`: FactoryIO Scene with the Complete Production Line with XYZ Pick & Place System.
- `project_tia_portal` : Ladder logic for the plc s7-1500 that controls the entire system.

### Define Area
This section defines the width and height of a single box in pixels to facilitate box detection. It consists of:
- `define_area.py`: This Python script waits for a signal from TIA Portal, captures an image of a single box, extracts its width and height in pixels, and stores these measurements in a CSV file for use in other parts of the project.
- `define_area.factoryio`: Factory Io scene made to allow a single box along the productio line.
- `define_area_tia_portal`: Ladder logic for the plc s7-1500 that controls the entire system for a single box.

### Create Dataset
This section creates a balanced dataset of marked and unmarked boxes in equal quantities to ensure proper training of the CNN. It consists of:
- `create_dataset.py`: This Python script waits for a trigger signal from TIA Portal, captures an image of the boxes on the conveyor, processes the image to isolate each individual box, saves cropped images of every box in a designated folder.
- `creat_dataset.factoryio`: The FactoryIO scene is specifically designed to position six boxes simultaneously within the camera's capture area.
- `create_dataset_tia_portal`: Ladder logic for the plc s7-1500 that controls the entire system.

To create the dataset of marked and unmarked boxes, this process must be executed twice: first in the default configuration, then again turning the box emitter upside down in the FactoryIO scene and changing the name of the outfolder in the python file to distinguish between the two sets of captured box images. 

## Other Files
### functions.py
This Python file contains the essential OPC UA client operations, including functions for writing and reading values from the server. It also implements a personalized round function.

### settings.py
This project highly depends on the screen size of the device, to set the regions of the screen capture and to transform the coordinates of each box in pixels to the real coordinates of the Pick & Place XYZ component in FactoryIO. Therefore, this file contains these settings for a 1680×1050 screen and a 1920×1080 one. For the Pick & Place, the settings are the a and b coefficients of a linear regression made using a group of dots in the captured image as X and the coordinates of the Pick & Place for those dots as y.

### Libraries

| Library               | Primary Use                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `opcua` (`Client`, `ua`) | OPC UA communication for industrial automation (client-server interactions) |
| `cv2` (`OpenCV`)        | Computer vision tasks (image processing, object detection)                 |
| `sys`                 | System-specific parameters and functions                                   |
| `numpy` (`np`)        | Numerical operations and array manipulation                                |
| `pyautogui`           | Programmatic mouse/keyboard control                                        |
| `os`                  | Operating system interactions                                              |
| `pandas` (`pd`)       | Data manipulation and analysis                                             |
| `tensorflow` (`tf`)   | Machine learning model development (CNN training/inference)                |

### Reference videos
- [Tia Portal and Python Comunication](https://youtu.be/BqaXtVe9z3s?si=EPxnBUihLmdpv2xy)
- [Tia Portal and FactoryIO Comunication](https://youtu.be/o4VLUmY8a9E?si=NMv2TfIltdsByXfI)
