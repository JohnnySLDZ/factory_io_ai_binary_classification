# factory_io_ai_binary_classification

## Implementation of a binary classification model for a production line using FactoryIO, Tia Portal and Python

## Description
This project is the implementation of a Convolutional Neural Network (CNN) to automatically identify and sort marked vs. unmarked boxes using a Pick & Place XYZ system in FactoryIO. The system communicates Siemens TIA Portal with FactoryIO and Python via an OPC UA server, bridging AI and industrial PLC control.

## Explanation Video⬇️⬇️⬇️:  
[![Alt text](https://img.youtube.com/vi/VSK87Z9wKWo/0.jpg)](https://youtube.com/shorts/VSK87Z9wKWo)

<[Video](https://youtube.com/shorts/VSK87Z9wKWo)>

## Video Demo⬇️⬇️⬇️:  
[![Alt text](https://img.youtube.com/vi/g0u7S8w8YA4/0.jpg)](https://www.youtube.com/watch?v=g0u7S8w8YA4)

<[Video](https://www.youtube.com/watch?v=g0u7S8w8YA4)>

## This project consist of three parts each one have their python and FactoryIO files and a folder with the Tia Portal project:

### Project
This is the main part of the project consist of:
- `project.py`: Python file that waits for tia portal signal, captures an image of the boxes on screen, procceses the image, extract each box along with their coordinates, loads the pretrained model to make predictions for each fox and then send the information back to tia portal.
- `project.factoryio`: Factory Io scene of the entire production line with the Pick & Place xyz system
- `project_tia_portal` : Ladder logic for the plc s7-1500 that controls the entire system

### Define Area
This part stablishes the width and hight of a single box in pixels to facilitate box detection, consist of:
- `define_area.py`: Python file that waits for tia portal signal, captures an image of a single box, extract its width and height and store them in a csv file to use in the others part of the project
- `define_area.factoryio`: Factory Io scene made to allow a single box into the capture area
- `define_area_tia_portal`: Ladder logic for the plc s7-1500 that controls the entire system

### Create Dataset
This part creates a dataset of marked and unmarked boxes in equal quantity to ensure the proper train of the CNN, consist of:
- `create_dataset.py`: Python file that waits for tia portal signal, captures an image of the boxes on screen, procceses the image, creates an image of each one of the box and store them in a specific folder
- `creat_dataset.factoryio`: Factory Io scene made to allow the python file to capture an image of 6 boxes at a time
- `create_dataset_tia_portal`: Ladder logic for the plc s7-1500 that controls the entire system
it is necesary to run this process two times turning upside down the box emitter in the factory io scene and changing the name of the outfolder in the python file to have a complete dataset of marked and unmarked boxes

## Other Files
### functions.py
This python file contains the definitions of the used to write and read values from the opcua server along with the implementation of a personalised round function

### settings.py
this project depends very highly on the screen size of the device to set the regions of the screen capture and to transform the coordinates of each box in pixel to the real coordinates of the Pick & Place XYZ Component in FactoryIO, therefore, this file contains these settings for a 1680x1050 screen and a 1920x1080 one, for Pick & Place the setting are the a and b coficient of a linear regretion made using a gruoup of dots in the captured image as X and the coordigates of the Pick & Place for those dots as y.

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
