import numpy as np
import matplotlib.pyplot as plt

# Define the perspective projection matrix
def perspective_matrix(d):
    """ Return the 4x4 perspective projection matrix. """
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, -1/d, 1]
    ])

# Apply perspective projection using matrix multiplication
def apply_perspective(points, d):
    """ Apply perspective projection to 3D points using a 4x4 matrix. """
    # Convert points to homogeneous coordinates by adding a fourth coordinate (w=1)
    points_h = np.hstack([points, np.ones((points.shape[0], 1))])
    
    # Apply the perspective transformation matrix
    matrix = perspective_matrix(d)
    transformed_points = np.dot(matrix, points_h.T).T
    
    # Divide by the h coordinate (homogeneous coordinate) to project back to 3D
    projected_points = transformed_points[:, :2] / (1 - points[:, 2] / d)[:, np.newaxis]
    
    return projected_points

# Define rotation matrix around the Y-axis
def rotate_y(points, theta):
    rotation_matrix = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])
    return np.dot(rotation_matrix,points.T).T

# Create a cube with 8 vertices
def create_cube():
    return np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Back face
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]        # Front face
    ])

# Define edges of the cube (pairs of vertices that form edges)
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
    (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
    (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
]

# Create cube points
cube = create_cube()

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')

# Function to plot the cube with perspective projection
def plot_cube(cube_2d, edges):
    ax.clear()
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')

    for edge in edges:
        point1 = cube_2d[edge[0]]
        point2 = cube_2d[edge[1]]
        ax.plot([point1[0], point2[0]], [point1[1], point2[1]], 'b')


theta = 0     # Initial rotation angle
d = 5         # Distance from camera to projection plane

plt.show(block=False)  # Non-blocking plot

while True:
    # Rotate the cube around the Y-axis
    rotated_cube = rotate_y(cube, np.radians(theta))
    
    # Apply perspective projection using matrix multiplication
    projected_cube = apply_perspective(rotated_cube, d)
    
    # Plot the projected cube
    plot_cube(projected_cube, edges)
    
    # Pause to allow plot refresh
    plt.pause(0.05)
    
    # Increment the rotation angle
    theta += 2

plt.show()
