# modified a canny viewer with sliders to show us adaptative threshold results with sliders

import cv2
import numpy as np
import matplotlib.pyplot as plt


def callback(x):
    print(x)


img = cv2.imread('test2.jpg', 0)  # read image as grayscale
width = 500
height = 300
dim = (width, height)
img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


canny = cv2.adaptiveThreshold(
    img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 5)

cv2.namedWindow('image')  # make a window with name 'image'
# lower threshold trackbar for window 'image
cv2.createTrackbar('L', 'image', 3, 255, callback)
# upper threshold trackbar for window 'image
cv2.createTrackbar('U', 'image', 3, 255, callback)

while(1):
    numpy_horizontal_concat = np.concatenate(
        (img, canny), axis=1)  # to display image side by side
    cv2.imshow('image', numpy_horizontal_concat)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # escape key
        break
    l = cv2.getTrackbarPos('L', 'image')
    u = cv2.getTrackbarPos('U', 'image')

    if l % 2 == 0:
        l += 1

    if u % 2 == 0:
        u += 1

    canny = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, l, u)

cv2.destroyAllWindows()
