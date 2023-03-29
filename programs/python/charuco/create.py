# https://pyimagesearch.com/2020/12/14/generating-aruco-markers-with-opencv-and-python/

import cv2
import cv2.aruco as aruco
import numpy as np

# Set the size of the charuco board and the size of the markers
square_length = 0.04   # Length of one square in meters
marker_length = 0.02   # Length of the marker in meters
dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)   # Set the aruco dictionary
charuco_board = aruco.CharucoBoard((9, 6), square_length, marker_length, dictionary)

# create matrix to store the image
boardImage = np.zeros((2000, 2000, 3), dtype=np.uint8)

img = charuco_board.generateImage((2000, 2000), boardImage, 10, 1)

cv2.imwrite('charuco_pattern.png', img)