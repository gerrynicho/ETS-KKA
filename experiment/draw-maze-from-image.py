#!/usr/bin/env python3
import cv2
import numpy as np
from matplotlib import pyplot as plt

image_path = './sarinah.png'
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
equalized = cv2.equalizeHist(img)
_, binary = cv2.threshold(equalized, 200, 255, cv2.THRESH_BINARY)

# inverted = cv2.bitwise_not(binary)

plt.figure(figsize=(10, 7))
plt.subplot(1, 3, 1)
plt.title("Original Image")
plt.imshow(img, cmap='gray')
plt.subplot(1, 3, 2)
plt.title("Contrast Enhanced")
plt.imshow(equalized, cmap='gray')
plt.subplot(1, 3, 3)
plt.title("Binary Roads")
plt.imshow(binary, cmap='gray')
plt.show()
