import numpy 
import cv2
import imutils
import sys
import pytesseract
import pandas as pd
import time

#Use openCV to read and annotate image
# cv2 to read the image

img = cv2.imread('./dataset/plate-1.jpg')
# Resize the image with specified height and width
img = imutils.resize(img, width = 500)
cv2.imshow("Original Image", img)

gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

'''
cv2.bilateralFilter() is an effective noise removal tool which keeps the
edges sharp. Bilateral filter preserves edges since the piles at the edges
will have large intensity variation

source - docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html
'''

gray_scale = cv2.bilateralFilter(gray_scale,11,17,17) 
'''
Concept of Canny edge detection
Multi-stage algorithm used for Noise reduction
Smoothened image is filtered in both horizontal and vertical direction.

docs.opencv.org/3.1.0/d4/d13/tutorial_py_canny.html
'''
edges = cv2.Canny(gray_scale,170,200 )
'''
Contours can be explained simply as a curve joining all the continuous points having the same color or intensity.
Contours are a useful tool for shape analysis and object detection

Using Numpy to find countours
im = cv2.imread('test.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
im2, contours,hierarchy = cv2.findContours(thresh,cv2.RETR.tree,cv2.CHAIN_APPROX_SIMPLE)

Three arguments in findCountours : First is source image, second is contour retrieval mode and third
is contour approximation method. Each individual contour is a numpy array of (x,y)
'''
(new,contour, _) = cv2.findContours(edges.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contour = sorted(contour, key = cv2.contourArea, reverse = True)[:30]

NumberPlate = None

count = 0

for i in contour:
    perimeter = cv2.arcLength(i , True)
    approxPoly = cv2.approxPolyDP( i, 0.02* perimeter, True)
    if len(approxPoly) == 4:
        NumberPlate = approxPoly
        break

# Masking the other parts of the number plate apart from the numbers assuming
# a specefic and generic size of the number plate

mask = numpy.zeros(gray_scale.shape,numpy.uint8)
output_image = cv2.drawContours(mask,[NumberPlate],0,255,-1)

output_image = cv2.bitwise_and(img,img,mask = mask)


cv2.imshow("Ouput Image", output_image)

#Configure the tesseract model for Optical character recognition on the new model

config = ('--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

#Running pyTesseract
# pyTesseract is a wrapper for Google's tesseract-OCR-engine.
#This uses requests to make an API Call

text = pytesseract.image_to_string(output_image, config=config, lang = 'eng')

#Use pandas to store data in a JSON file
# pandas .to_json() 

csv_data = raw_data = {'date': [time.asctime( time.localtime(time.time()) )], 
        'plate_number': [text]}

x = pd.DataFrame(csv_data, columns = ['date','plate_number'])
x.to_json('detected.json')

print(text)
cv2.waitKey(0)
