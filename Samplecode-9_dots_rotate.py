import numpy as np
import matplotlib.pyplot as plt
import time

# Define rotation matrix for rotating around the y-axis by angle theta
def rotate_y(points, theta):
    rotation_matrix_y = np.array([[np.cos(theta), 0, -np.sin(theta)],
                                   [0, 1, 0],
                                   [np.sin(theta), 0, np.cos(theta)]])
    return np.dot(points, rotation_matrix_y.T)

# Create a set of 3D points (or use any 3D model of a ball-like object)
def create_3d_sphere(n_points=100):
    phi = np.random.uniform(0, np.pi, n_points)
    theta = np.random.uniform(0, 2 * np.pi, n_points)
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    return np.stack([x, y, z], axis=-1)

# Project the 3D points to 2D by ignoring the z-coordinate
def project_to_2d(points_3d):
    return points_3d[:, :2]

# Create ball-like object
points_3d = create_3d_sphere()

# Setup the plot
fig, ax = plt.subplots()
scat = ax.scatter(points_3d[:, 0], points_3d[:, 1], c='b')

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')

# Infinite loop for continuous rotation

while True:
    theta = np.radians(2)  # Rotate by 2 degrees
    points_3d = rotate_y(points_3d, theta)
    points_2d = project_to_2d(points_3d)  # Project rotated points to 2D
    scat.set_offsets(points_2d)  # Update scatter plot
    plt.pause(0.05)  # Pause to update the plot

