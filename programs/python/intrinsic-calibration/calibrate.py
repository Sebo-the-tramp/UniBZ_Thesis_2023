## Note the folder with the images must be in the same folder as the script
## Now the folder is not provided because of the number of images
## If needed contact sebastian.cavada.dev@gmail.com

import numpy as np
import cv2 as cv
import glob

x = 12
y = 9

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((y*x,3), np.float32)
objp[:,:2] = np.mgrid[0:x,0:y].T.reshape(-1,2)

#folder = '../test_real_2/'
folder = '../test1/'

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob(folder + '*.png')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners

    #cv.imshow('img', gray)        
    #cv.waitKey() # wait for 1 ms

    ret, corners = cv.findChessboardCorners(gray, (y,x), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)        
        imgpoints.append(corners2)
        
        # Draw and display the corners
        """
        cv.drawChessboardCorners(img, (y,x), corners2, ret)
        cv.imshow('img', img)        
        cv.waitKey() # wait for 1 ms
        """
        

    else:
        print("Not found: ", fname)


cv.destroyAllWindows()

print("objpoints: ", len(objpoints))
print("imgpoints: ", len(imgpoints))

img = cv.imread('../10.png')
#img = cv.imread(folder + 'calibration6.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

h, w = img.shape[:2]
print("w: ", w)
print("h: ", h)
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort - cv2.undistort()
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
cv.imwrite('../calibresult0.png', dst)

print("mtx: ", mtx)
print("dist: ", dist)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(objpoints)) )
