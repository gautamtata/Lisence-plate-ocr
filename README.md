# Lisence-plate-ocr
A simple object detection model that detects lisence plate objects crops them and does OCR

# Object-Detection
Object detection is done using *tensorflow*. Tensorflow is an open source machine learning by framework that simplfies machine learning. I used tf to build a simple object detection model that works like a moving frame. The frame when detects an object that looks like a lisence plate stops.

# Image-stablization grayscale crop and sharpen 

All the above features are done using *openCV*. Once the object is detected, the lisence plate is cropped up into a another image which is then sharpened and a grayscale filter is added upon it. Some more features for image optimaztion have been added from the openCV docs.

# Optical character recognition

Now that all the filters have been added to it for optimal character recognition I used *tesseract* for optical character recognition. Tesseract is an Open source OCR engine which basically upon pinging the tesseract API renders and reads the characters on the image server side and spits out the output to the terminal.

# Pandas-JSON

Use the Pandas Library to take the output and print it in a JSON file.

# *problems with the project*

1. One problem seems to be that it is a single point of failure. By that I mean in this case, there are too many things that can and will go wrong. The object detection model is quite simple and therefore not robust. Any image with multiple car images or images with text already rendered on it will bound to create problems.

2. Another problem, which I faced (which I'm assuming is a problem with Tesseract) is that If I try to OCR California lisence plates the program detects the plates fine but since there is a registeration tag with Characters on it, the OCR fails and sometimes breaks.


