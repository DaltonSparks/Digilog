#

import cv2
from pytesseract import pytesseract, Output
from sklearn.cluster import KMeans
import numpy as np
import os
from imutils import contours


# changed all of the '\' to '/' in the names
# make this wherever you have tessreact stored
tesseractDir = "C:/Users/nistp/Tesseract-OCR//tesseract.exe"
# pytesseract
pytesseract.tesseract_cmd = tesseractDir


def getRandomColor():
    return (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))


# Read image and resize it
image = cv2.imread('test3.jpg')
width = 1000
height = 700
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

tess = image.copy()
tess = cv2.resize(tess, (1080, 1080), interpolation=cv2.INTER_AREA)

# GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--
# GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--
# extract text from image with pytesseract
info = pytesseract.image_to_data(tess, output_type=Output.DICT)
lowerInfo = []
# convert info to lowercase and store in a list
for element in info['text']:
    if element:
        lowerInfo.append(element.lower())

# we will check to see if the month name is detected
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']
possibleMonth = []
for name in months:
    if name in lowerInfo:
        possibleMonth.append(name)
# if there is a detected month, then set the monthName as that month
if len(possibleMonth) == 1:
    monthName = possibleMonth[0]
else:
    # otherwise, the monthName will be named as follows:
    monthName = "findMonth"
# GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--
# GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--GETMONTHNAME--


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 1)
thresh = cv2.Canny(blur, 200, 50)
#cv2.imshow("T", thresh)
kernel = np.ones((5, 5))
dilation = cv2.dilate(thresh, kernel, iterations=2)
erosion = cv2.erode(dilation, kernel, iterations=1)
#cv2.imshow("erosion", erosion)
# Find the biggest contours--the calendar box-----------------------
allContours, hierarchy = cv2.findContours(
    erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# drawContours on copy image (not necessary)
# cv2.drawContours(image, allContours, -1, (np.random.randint(0, 255),
#                                          np.random.randint(0, 255), np.random.randint(0, 255)), 10)
#cv2.imshow("ab", image)

# choose the biggest contours for cropping
areas = []
for contour in allContours:
    area = cv2.contourArea(contour)
    areas.append(area)
bigC = max(areas)

for contour in allContours:
    area = cv2.contourArea(contour)
    if area == bigC:
        x, y, w, h = cv2.boundingRect(contour)
        imageCropped = image[y:y+h, x:x+w]
#cv2.imshow("image", image)
#cv2.imshow("CROP", imageCropped)
output = imageCropped.copy()
#output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)

grayC = cv2.cvtColor(imageCropped, cv2.COLOR_BGR2GRAY)
threshC = cv2.adaptiveThreshold(
    grayC, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 2)
contoursC = cv2.findContours(threshC, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contoursC = contoursC[0] if len(contoursC) == 2 else contoursC[1]
#cv2.imshow("a", threshC)
for c in contoursC:
    area = cv2.contourArea(c)
    if 1000 < area < 20000:
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(contour, True), True)
        if len(approx) < 7:
            x, y, w, h = cv2.boundingRect(c)
            #save = output[y:y+h, x:x+w]
            #cv2.rectangle(output, (x, y), (x+w, y+h), getRandomColor(), 2)
            cv2.drawContours(threshC, [c], -1, (255, 255, 255), 3)
threshC = cv2.bitwise_not(threshC)
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
threshC = cv2.morphologyEx(threshC, cv2.MORPH_CLOSE,
                           vertical_kernel, iterations=1)
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
threshC = cv2.morphologyEx(threshC, cv2.MORPH_CLOSE,
                           horizontal_kernel, iterations=1)
threshC = cv2.bitwise_not(threshC)
cv2.imshow("Thresh", threshC)

# so far, the square for the 28th does not get detected. change iterations or modify kernels
contoursC = cv2.findContours(threshC, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contoursC = contoursC[0] if len(contoursC) == 2 else contoursC[1]
#(contoursC, _) = contours.sort_contours(contoursC, method="top-to-bottom")

allRows = []
row = []

'''for (i, c) in enumerate(contoursC, 1):
    area = cv2.contourArea(c)
    if 1000 < area < 25000:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(output, (x, y), (x+w, y+h), (np.random.randint(0, 255),
                      np.random.randint(0, 255), np.random.randint(0, 255)), 2)
        row.append(c)
        if i % 7 == 0:
            (contoursC, _) = contours.sort_contours(row, method="left-to-right")
            allRows.append(contoursC)
            row = []
temp = 0
for item in allRows:
    for element in item:
        x, y, w, h = cv2.boundingRect(c)
        save = output[y:y+h, x:x+w]
        cv2.imshow(f"{temp}", save)
        temp += 1'''
for contour in contoursC:
    area = cv2.contourArea(contour)
    if 1000 < area < 25000:
        # if the contour has 4 points, then print it/save it
        #approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(contour, True), True)
        # print(len(approx))
        cv2.drawContours(output, [contour], -1, getRandomColor(), 3)


cv2.imshow("output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
