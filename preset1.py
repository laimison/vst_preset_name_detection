#!/usr/local/bin/python3

# it should extract "Analog Grit"

import numpy as np
import cv2
from PIL import Image
import pytesseract

img = cv2.imread('img/preset1.png', cv2.IMREAD_COLOR)
# img = cv2.blur(img, (5, 5))
# img = cv2.blur(img, (1, 1))
# img = cv2.GaussianBlur(img, (5, 5), 0)
# img = cv2.GaussianBlur(img, (0,0), 3)

# sharpen
# img = cv2.addWeighted(img, 1.5, blur, -0.5, 0)

# unsharpen
# unsharp_image = cv2.addWeighted(img, 2, blur, -0.8, 0)

#HSV (hue, saturation, value)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)

#Applying threshold on pixels' Value (or Brightness)
thresh = cv2.adaptiveThreshold(v, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
# thresh = cv2.adaptiveThreshold(v, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

#Finding contours
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Fixing
# print(contours)
# arr = (np.array([[[ 52, 200]], [[ 57, 201]], [[ 56, 200]]], dtype=np.int32), np.array([[[ 30, 200]], [[ 33, 201]], [[ 31, 201]]], dtype=np.int32), np.array([[[ 27, 205]], [[ 25, 206]], [[ 26, 205]]], dtype=np.int32), np.array([[[ 29, 105]], [[ 35, 106]], [[ 34, 105]]], dtype=np.int32), np.array([[[ 60, 104]], [[ 64, 107]], [[ 61, 104]]], dtype=np.int32), np.array([[[53, 23]], [[63, 27]], [[59, 23]]], dtype=np.int32), np.array([[[26, 23]], [[35, 25]], [[33, 23]]], dtype=np.int32), np.array([[[29, 27]], [[26, 29]], [[27, 29]]], dtype=np.int32), np.array([[[ 1, 22]], [[ 4, 23]], [[ 2, 23]]], dtype=np.int32), np.array([[[10, 11]], [[25, 12]], [[24, 11]]], dtype=np.int32), np.array([[[58,  6]]], dtype=np.int32), np.array([[[0, 6]], [[6, 7]], [[5, 6]]], dtype=np.int32), np.array([[[89,  0]], [[91,  2]], [[91,  0]]], dtype=np.int32), np.array([[[ 0,  0]], [[37,  1]], [[36,  0]]], dtype=np.int32))
# okey = np.concatenate(arr)
contours_okey = np.concatenate(contours)
# exit(0)

#Filling contours
# contours = cv2.drawContours(img, np.array(contours_okey), -1, (255,255,255), -1)
contours = cv2.drawContours(img, np.array(contours_okey), -1, (0, 255, 0), thickness=0)

#To black and white
grayImage = cv2.cvtColor(contours, cv2.COLOR_BGR2GRAY)
# grayImage = cv2.cvtColor(contours, cv2.COLOR_BGR2RGB)

#And inverting it
#Setting all `dark` pixels to white
grayImage[grayImage > 200] = 0 # default
# grayImage[grayImage > 197] = 0
# grayImage[grayImage > 203] = 0
#Setting relatively clearer pixels to black
# grayImage[grayImage < 35] = 255 # preset1 works
# grayImage[grayImage < 40] = 255 # preset2 works
grayImage[grayImage < 38] = 255 # preset1 and preset2 works
# grayImage[grayImage < 43] = 255 # preset1 works

#Write the temp file
cv2.imwrite('tmp/temp.png', grayImage)

# resize image to two times bigger
image = cv2.imread('tmp/temp.png', cv2.IMREAD_UNCHANGED)
new_size = (image.shape[1]*2, image.shape[0]*2)
resized_image = cv2.resize(image, new_size)
cv2.imwrite('tmp/temp_bigger.png', resized_image)

#Read it with tesseract
text = pytesseract.image_to_string(Image.open('tmp/temp_bigger.png'),config='tessedit_char_whitelist=0123456789_-qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM -psm 6 ')
# text = pytesseract.image_to_string(Image.open('temp_bigger.png'),config='tessedit_char_whitelist=0123456789_-qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
# text = pytesseract.image_to_string(Image.open('preset4.png'),config='tessedit_char_whitelist=0123456789_-qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM -psm 6 ')
# text = pytesseract.image_to_string(Image.open('preset3.png')) # preset3 works!

#Output
# print("####  Raw text ####")
# print(text)
# print()
# print("#### Extracted chracters ####")
# print([''.join([y for y in x if y.isdigit()]) for x in text.split('\n')])
print(text.split('\n'))
