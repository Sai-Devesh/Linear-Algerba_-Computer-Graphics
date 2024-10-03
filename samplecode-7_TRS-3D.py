import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Define the original cube vertices (homogeneous coordinates with 1 for translation)
original_cube = np.array([[0, 0, 0, 1],  # Point A
                          [1, 0, 0, 1],  # Point B
                          [1, 1, 0, 1],  # Point C
                          [0, 1, 0, 1],  # Point D
                          [0, 0, 1, 1],  # Point E
                          [1, 0, 1, 1],  # Point F
                          [1, 1, 1, 1],  # Point G
                          [0, 1, 1, 1]]) # Point H

# Function to perform matrix multiplication
def matrix_multiply(matrix1, matrix2):
    return np.dot(matrix1, matrix2.T).T

# Function to plot the cube using ax for 3D plotting
def plot_cube(cube, color, label=None):
    # Define edges connecting cube vertices
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),  # Bottom square edges
             (4, 5), (5, 6), (6, 7), (7, 4),  # Top square edges
             (0, 4), (1, 5), (2, 6), (3, 7)]  # Vertical edges
    
    for edge in edges:
        # Plot lines using ax.plot for 3D cube representation
        ax.plot([cube[edge[0], 0], cube[edge[1], 0]],
                [cube[edge[0], 1], cube[edge[1], 1]],
                [cube[edge[0], 2], cube[edge[1], 2]], color=color)
    
    # Plot points using ax.plot3D to maintain consistency with the 3D space
    ax.plot(cube[:, 0], cube[:, 1], cube[:, 2], 'o', color=color, label=label)

# Taking user inputs for translation, rotation, and scaling
tx = float(input("Enter translation along x-axis (tx): "))
ty = float(input("Enter translation along y-axis (ty): "))
tz = float(input("Enter translation along z-axis (tz): "))
theta_x = float(input("Enter rotation angle around x-axis in degrees: "))
theta_y = float(input("Enter rotation angle around y-axis in degrees: "))
theta_z = float(input("Enter rotation angle around z-axis in degrees: "))
scaling_factor = float(input("Enter scaling factor (s): "))

# 1. Translation Matrix (4x4)
translation_matrix = np.array([[1, 0, 0, tx],
                               [0, 1, 0, ty],
                               [0, 0, 1, tz],
                               [0, 0, 0, 1]])

# 2. Rotation Matrices around each axis (converted to radians)
theta_x = np.radians(theta_x)
theta_y = np.radians(theta_y)
theta_z = np.radians(theta_z)

rotation_matrix_x = np.array([[1, 0, 0, 0],
                              [0, np.cos(theta_x), -np.sin(theta_x), 0],
                              [0, np.sin(theta_x), np.cos(theta_x), 0],
                              [0, 0, 0, 1]])

rotation_matrix_y = np.array([[np.cos(theta_y), 0, np.sin(theta_y), 0],
                              [0, 1, 0, 0],
                              [-np.sin(theta_y), 0, np.cos(theta_y), 0],
                              [0, 0, 0, 1]])

rotation_matrix_z = np.array([[np.cos(theta_z), -np.sin(theta_z), 0, 0],
                              [np.sin(theta_z), np.cos(theta_z), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

# 3. Scaling Matrix (uniform scaling in all axes)
scaling_matrix = np.array([[scaling_factor, 0, 0, 0],
                           [0, scaling_factor, 0, 0],
                           [0, 0, scaling_factor, 0],
                           [0, 0, 0, 1]])

# Apply transformations independently to the original cube
# Step 1: Apply scaling
scaled_cube = matrix_multiply(scaling_matrix, original_cube)

# Step 2: Apply rotation (rotate around x, y, and z axes)
rotated_cube = matrix_multiply(rotation_matrix_x, original_cube)
rotated_cube = matrix_multiply(rotation_matrix_y, rotated_cube)
rotated_cube = matrix_multiply(rotation_matrix_z, rotated_cube)

# Step 3: Apply translation
translated_cube = matrix_multiply(translation_matrix, original_cube)

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the original cube (blue)
plot_cube(original_cube, 'blue', 'Original')

# Plot the scaled cube (red)
plot_cube(scaled_cube, 'red', 'Scaled')

# Plot the rotated cube (green)
plot_cube(rotated_cube, 'green', 'Rotated')

# Plot the translated cube (black)
plot_cube(translated_cube, 'black', 'Translated')

# Set axis labels and plot details
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Cube with Independent Transformations')
ax.view_init(elev=20., azim=30)

# Add a legend for cube transformations
ax.legend()

plt.show()
