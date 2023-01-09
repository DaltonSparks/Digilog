# copy of the detect.py file

import cv2
import numpy as np
from imutils import contours as ctrs
# do not modify!


def getRandomColor():
    return (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))


image = cv2.imread('test6.jpg')
width = 1000
height = 700
image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

# GET LARGEST CONTOUR AND CROP      #GET LARGEST CONTOUR AND CROP
# GET LARGEST CONTOUR AND CROP      #GET LARGEST CONTOUR AND CROP
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 1)
thresh = cv2.Canny(blur, 200, 50)
kernel = np.ones((5, 5))
dilation = cv2.dilate(thresh, kernel, iterations=3)
erosion = cv2.erode(dilation, kernel, iterations=1)


allContours, hierarchy = cv2.findContours(
    dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

maxArea = 0
maxContour = allContours[0]

for contour in allContours:
    area = cv2.contourArea(contour)
    if area > maxArea:
        maxArea = area
        maxContour = contour
x, y, w, h = cv2.boundingRect(maxContour)
imageCropped = image[y:y+h, x:x+w]
# GET LARGEST CONTOUR AND CROP      #GET LARGEST CONTOUR AND CROP
# GET LARGEST CONTOUR AND CROP      #GET LARGEST CONTOUR AND CROP

gray = cv2.cvtColor(imageCropped, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 2)
contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
# expand the contours for the calendar lines by drawing over the contours in the thresh image
for c in contours:
    area = cv2.contourArea(c)
    if 1000 < area < 50000:
        # thicken the contours that are detected
        cv2.drawContours(thresh, [c], -1, (255, 255, 255), 4)

# vertical and horizontal thresholds using morphological transformations
thresh = cv2.bitwise_not(thresh)
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 4))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                          vertical_kernel, iterations=1)
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 1))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                          horizontal_kernel, iterations=1)
thresh = cv2.bitwise_not(thresh)
# get rid of background noise in image
thresh = cv2.erode(thresh, (1, 1), iterations=3)
# END - vertical and horizontal thresholds using morphological transformations
# obtain contours once more on the cleaner thresh image
contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
#(contoursC, _) = contours.sort_contours(contoursC, method="top-to-bottom")
avgW = 0
avgH = 0
avgArea = 0
counter = 0
for contour in contours:
    area = cv2.contourArea(contour)
    if 1000 < area < 25000:
        x, y, w, h = cv2.boundingRect(contour)
        avgArea += area
        avgW += w
        avgH += h
        counter += 1

avgW = (avgW / counter)
avgArea = (avgArea / counter)
avgH = (avgH / counter)
deleteMe = 0
for contour in contours:
    area = cv2.contourArea(contour)
    if (avgArea - (avgArea * .4)) < area < (avgArea + (avgArea * .4)):
        x, y, w, h = cv2.boundingRect(contour)
        if (avgW - (avgW * .4)) < w < (avgW + (avgW * .4)) and (avgH - (avgH * .4)) < h < (avgH + (avgH * .4)):
            save = imageCropped[y:y+h, x:x+w]
            cv2.drawContours(imageCropped, [contour], -1, getRandomColor(), 2)

            if deleteMe == 6:
                cv2.imshow(f"{deleteMe}", save)
            deleteMe += 1
cv2.imshow("output", imageCropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
