from scipy.spatial.transform import Rotation
import numpy as np
import cv2

p5 = np.array([0.0318884, -0.303479, 7.10128])
p6 = np.array([0.158565, -0.130994, 7.34722])

# Define the keypoints of the body in the keypoints_pose_25 format
keypoints = np.array([p5, p6])

# Define the indices of the joints that we want to compute the rotation for
joint_indices = [(0,1)]

# Define the Y-axis of the 3D space
y_axis = np.array([0,1,0])

# Define the Z-axis of the 3D space
z_axis = np.array([0,0,1])


# calculate
vec = p6 - p5

# Compute the rotation around the Y-axis
angle_y = np.arccos(np.dot(vec, y_axis) / np.linalg.norm(vec))
axis_y = np.cross(vec, y_axis)
rot_y = cv2.Rodrigues(axis_y * angle_y)[0]

# Compute the rotation around the Z-axis
angle_z = np.arccos(np.dot(rot_y.dot(vec), z_axis) / np.linalg.norm(rot_y.dot(vec)))
axis_z = np.cross(rot_y.dot(vec), z_axis)
rot_z = cv2.Rodrigues(axis_z * angle_z)[0]

# Compute the final rotation matrix for the joint
joint_rot = rot_z.dot(rot_y)

# Create rotation object
r = Rotation.from_matrix(joint_rot)

# Convert to Euler angles (in radians)
euler = r.as_euler('xyz', degrees=True)

# Print Euler angles
print("Euler angles (in degrees): ", euler)