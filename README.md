# QR Code Reader
A Python Program that uses OpenCV to detect and extract data from QR Codes in Images or in Live Video.

## Requirements
Language Used = Python3<br />
Modules/Packages used:
* cv2
* datetime
* optparse
* time
* colorama
<!-- -->
Install the dependencies:
```bash
pip install -r requirements.txt
```

## Inputs
It takes the following arguments from the command that is used to run the Python Program:
* '-s', "--save" : Name of the file to save Data extracted from the QR Code
* '-i', "--image" : Load Image from the given file

## Output
If no image path is provided, then the Program will start the Default Camera of the Device and start detection of QR Codes and will display the extracted data.<br />
It no output file name is provided, then the data is saved in a file with name as the current date and time.