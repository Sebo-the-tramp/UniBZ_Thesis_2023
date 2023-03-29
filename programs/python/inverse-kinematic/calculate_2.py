from math import sqrt, atan2, pi
import numpy as np

##p5 = np.array([0.0318884, -0.303479, 7.10128]) * 100
##p6 = np.array([0.158565, -0.130994, 7.34722]) * 100 


# Input points
##x1, y1, z1 = p5[0], p5[1], p5[2]
#x2, y2, z2 = p6[0], p6[1], p6[2]

x1, y1, z1 = 44.14, 3.5, 143.38
x2, y2, z2 = 71.19, 17.44, 124.40

# Calculate vector
vector_x = x2 - x1
vector_y = y2 - y1
vector_z = z2 - z1

# calculate midpoint
midpoint_x = (x1 + x2) / 2
midpoint_y = (y1 + y2) / 2
midpoint_z = (z1 + z2) / 2

print("Midpoint: ({}, {}, {})".format(midpoint_x, midpoint_y, midpoint_z))

# Calculate magnitude of vector
magnitude = sqrt(vector_x**2 + vector_y**2 + vector_z**2)

# Calculate rotation angle on x-axis
rotation_x = atan2(vector_z, vector_x) * 180 / pi

# Calculate rotation angle on y-axis
rotation_y = atan2(vector_z, vector_y) * 180 / pi

print("Vector: ({}, {}, {})".format(vector_x, vector_y, vector_z))
print("Magnitude: {}".format(magnitude))
print("Rotation angle on x-axis: {:.2f} degrees".format(rotation_x))
print("Rotation angle on y-axis: {:.2f} degrees".format(rotation_y))