# Decided not to use pytesseract for now


import cv2
from pytesseract import pytesseract, Output
import numpy as np
from sklearn.cluster import KMeans
import os


# I moved the tesseract.exe file to this folder so that I wouldn't have to get the directory for each
# image that I wanted to read.
# changed all of the '\' to '/' in the names

myDirectory = os.getcwd()
myDirectory = myDirectory.replace('\\', '/')

tesseractDir = "C:/Users/nistp/Tesseract-OCR//tesseract.exe"
# run pytesseract
pytesseract.tesseract_cmd = tesseractDir

imgName = (f'{myDirectory}//test3.jpg')

img = cv2.imread(imgName)
# Resize Image for Reading the date
width = 1080
height = 1080
dim = (width, height)
img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
# store the info that pytesseract extracted
info = pytesseract.image_to_data(img, output_type=Output.DICT)
lowerInfo = []
# convert info to lowercase and store in a list
for element in info['text']:
    if element:
        lowerInfo.append(element.lower())

print(lowerInfo)
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
print(possibleMonth)

# make a copy of the original image to write our bounding boxes over it
img2 = img.copy()
# convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# perform gaussian thresholding
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 2)
# find the contours of the image
contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

cv2.imshow("thresh", thresh)
# perform clustering on the data-------------------------------------
# work on detecting the most frequent cluster only
areas = []
# fill in the array with the area of each contour greater than size
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 10000:
        areas.append(area)
# Used areas array to get an idea of the sizes of the contours
# print(areas)

# clustering information
clusterNum = 2
data = np.array(areas)
kmeans = KMeans(n_clusters=clusterNum).fit(data.reshape(-1, 1))
clusters = kmeans.predict(data.reshape(-1, 1))

# maxCluster is the cluster with the greatest number of data points in it
# which will be all of our actual calendar squares
maxCluster = max(kmeans.labels_)

# cluster_centers are the different clusters that were detected
# print(kmeans.cluster_centers_)
# keep track of the box
number = 0
# if monthName is not yet found, then declare it as follows:
if not monthName:
    monthName = "findMonth"

number = 0
for contour in contours:
    area = cv2.contourArea(contour)
    # for test 4, the areas are in the following range:
    if 16000 < area < 25000:
        # for test 5, the areas are in the following range:
        # if 100000 < area < 1000000:
        # for test2 the areas are in the following range:
        # if 24000 < area < 33000:
        # for test 4, the areas are in the following range:
        # if 14000 < area:

        # get the values for the bounding rect
        x, y, x2, y2 = cv2.boundingRect(contour)
        # save the image into a rectangle
        saveRect = img2[y:y+y2, x:x+x2]
        saveRect2 = img[y:y+y2, x:x+x2]
        width = 350
        height = 350
        dim = (width, height)
        saveRect2 = cv2.resize(saveRect2, dim, interpolation=cv2.INTER_AREA)
        saveRect2 = cv2.GaussianBlur(saveRect2, (5, 5), 0)
        # convert to grayscale
        saveRect2 = cv2.cvtColor(saveRect2, cv2.COLOR_BGR2GRAY)
        saveRect2 = cv2.threshold(
            saveRect2, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = np.ones((2, 2), np.uint8)
        saveRect2 = cv2.erode(saveRect2, kernel, iterations=1)
        saveRect2 = cv2.dilate(saveRect2, kernel, iterations=1)

        # draw the rectangle on img2, which is a copy of the original with no modifications
        cv2.rectangle(img2, (x, y), (x + x2, y + y2), (0, 0, 255), 3)
        day = pytesseract.image_to_data(
            saveRect2, output_type=Output.DICT, config='--psm 11')
        date = []
        for element in day['text']:
            if element.isdigit():
                date.append(element.lower())
                print(date)
        # for test purposes, will save the given image snip
        if 30 in date:
            filename = monthName + str(date[0]) + '.jpg'
            cv2.imwrite(filename, saveRect)
            #cv2.imshow("rect", saveRect)
        # if date is not recognized/if date is empty
        # if not date:
            #cv2.imshow(f"{number}", saveRect2)

        #number += 1
        # cv2.imshow(f"{number}", saveRect)
# print(f"The total number of boxes is: {number}")


# resizing image for viewing. ended up doing this above instead


width = 720
height = 720
dim = (width, height)

thresh = cv2.resize(thresh, dim, interpolation=cv2.INTER_AREA)
img2 = cv2.resize(img2, dim, interpolation=cv2.INTER_AREA)

cv2.imshow('result', img2)
cv2.waitKey(0)

cv2.destroyAllWindows()
