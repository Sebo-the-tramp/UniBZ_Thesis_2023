import numpy as np
import cv2 as cv
import glob

img = cv.imread('../2.jpg')
#img = cv.imread(folder + 'calibration6.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

mtx = np.array([[706.76644819,   0,        960],
                [0,         708.74725602,  540],
                [0,          0,          1, ]])


#dist = np.array([[0, 0, 0,  0, 0]])
dist = np.array([[-1.99794990e-02,  -2.14154680e-06, -6.97411544e-06,  0, 0]])
#dist = np.array([[-0.03018198, -0.005255 ,  -0.02849359,  0.04396421,  0.00361847]])

h, w = img.shape[:2]
print("w: ", w)
print("h: ", h)
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# undistort - cv2.undistort()
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
cv.imwrite('../calibresult0.png', dst)