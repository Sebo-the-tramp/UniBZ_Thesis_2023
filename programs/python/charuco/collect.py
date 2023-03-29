# write a program that every 5 seconds takes a picture and saves it to a folder

import cv2
import time
import winsound

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second

# Set up camera
camera = cv2.VideoCapture(5)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
print("Camera opened: {}".format(camera.isOpened()))

# Define file name and directory
directory = "images/"
file_name = "image_{}.jpg"

# Initialize counter for file name
i = 0

# Run loop to capture images every 5 seconds
while True:

    winsound.Beep(frequency+500, duration *2)
    print("Capturing image")
    # Capture image
    ret, frame = camera.read()
    
    # Save image
    file_path = directory + file_name.format(i)
    cv2.imwrite(file_path, frame)

    print("saved image {}".format(file_path))
    
    # Increment file name counter
    i += 1

    # Wait for 2 seconds
    winsound.Beep(frequency, duration)
    print("2")
    time.sleep(1)
    winsound.Beep(frequency, duration)
    print("1")
    time.sleep(1)    

# Release camera
camera.release()