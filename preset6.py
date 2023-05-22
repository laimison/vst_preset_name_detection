#!/usr/local/bin/python3

# it should extract "PR Kicking [CFA]"

import pytesseract
import cv2
from PIL import Image

# Open image file
img = Image.open('img/preset6.png')

# Preprocess the image
img = img.convert('L')      # Convert the image to grayscale
img = img.point(lambda x: 0 if x < 128 else 255, '1') # Binarization

# Whitelist characters
whitelist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_ '
# whitelist = 'k'

# Specify the language and character set
lang = 'eng'
# config = f'-c tessedit_char_whitelist={whitelist} --psm 6 -l {lang}'
config = f'tessedit_char_whitelist= --psm 6 -l {lang}' # preset 6 worked!
# config = f'--psm 6 -l {lang}'

# resize image to two times bigger
# image = cv2.imread('preset6.png', cv2.IMREAD_UNCHANGED)
# new_size = (image.shape[1]*2, image.shape[0]*2)
# resized_image = cv2.resize(image, new_size)
# cv2.imwrite('temp_bigger.png', resized_image)
# img = Image.open('temp_bigger.png')

# Convert image to string using pytesseract
# text = pytesseract.image_to_string(img)
text = pytesseract.image_to_string(img, config=config)

# Print the string
print(text.split('\n'))
