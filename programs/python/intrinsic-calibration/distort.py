import cv2
import numpy as np

# read image
img = cv2.imread('./2.png')

if(img is None):
    print('Image not found')
    exit()

# get image height, width
height, width = img.shape[:2]
print('height: ', height)
print('width: ', width)

# create parameters for distortion
# 1. center of distortion
# 2. angle
# 3. scale
center = (width/2, height/2)
angle = 0
scale = 1.0
494
# create parameters k1, k2, p1, p2, k3
k1 = 0.123
k2 = 0
p1 = 0
p2 = 0
k3 = 0.54

#-1.3992017198416036e+01 1.3551401805944428e+02 5.2987770184031825e-05 -3.5181799653829360e-05 -2.6094526306723793e+01 -1.4126573267547267e+01

# [k1, k2, p1, p2, [k3, [k4, k5, k6]]]

camera_matrix = np.array([[1885.5221317672456, 0, width/2], [0, 1885.5221317672456, height/2], [0, 0, 1]])

# create distortion matrix
distortion_matrix = np.array([1.93195040e-01, -8.01940859e-01, -1.53030929e-03,  1.52830751e-03, 7.25395235e+00])
#distortion_matrix = np.array([-13.82450916656845, 28.0639062179489, 0.01130842240628631, -0.001219832663596509, 145.9741335390135])
#distortion_matrix = np.array([k1, k2, p1, p2, k3])

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_matrix, (width,height), 1, (width,height))

# distort image
distorted_img = cv2.undistort(img, camera_matrix, distortion_matrix, None, newcameramtx)

# show image
cv2.imshow('undistorted image', distorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
