import matplotlib.pyplot as plt
import numpy as np

# Defining the original triangle points (homogeneous coordinates with 1 for translation purposes)
original_triangle = np.array([[1, 1, 1],  # Point A
                              [4, 2, 1],  # Point B
                              [1, 4, 1]])  # Point C

# Function to perform matrix multiplication
def matrix_multiply(matrix1, matrix2):
    result = np.zeros((matrix1.shape[0], matrix2.shape[1]))
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    
    return result

# Function to plot triangles
def plot_triangle(triangle, color, label):
    triangle = np.vstack([triangle, triangle[0]])  # Closing the triangle
    plt.plot(triangle[:, 0], triangle[:, 1], 'o-', color=color, label=label)

# Taking user inputs
tx = float(input("Enter translation along x-axis (tx): "))
ty = float(input("Enter translation along y-axis (ty): "))
theta = float(input("Enter rotation angle in degrees (θ): "))
scaling_factor = float(input("Enter scaling factor (s): "))

# Defining transformation matrices

# 1. Translation Matrix
translation_matrix = np.array([[1, 0, tx],
                               [0, 1, ty],
                               [0, 0, 1]])

# 2. Rotation Matrix (rotate by theta degrees counterclockwise)
theta = np.radians(theta)  # Convert to radians
rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                            [np.sin(theta),  np.cos(theta), 0],
                            [0, 0, 1]])

# 3. Scaling Matrix (scaling by the given factor on x and y axes)
scaling_matrix = np.array([[scaling_factor, 0, 0],
                           [0, scaling_factor, 0],
                           [0, 0, 1]])  # Corrected to keep homogeneous coordinate as 1

# Apply transformations using matrix_multiplication
translated_triangle = matrix_multiply(translation_matrix, original_triangle.T).T
rotated_triangle = matrix_multiply(rotation_matrix, original_triangle.T).T
scaled_triangle = matrix_multiply(scaling_matrix, original_triangle.T).T

# Plotting
plt.figure()

# Plot original triangle (blue)
plot_triangle(original_triangle, 'blue', 'Original')

# Plot translated triangle (black)
plot_triangle(translated_triangle, 'black', 'Translated')

# Plot rotated triangle (green)
plot_triangle(rotated_triangle, 'green', 'Rotated')

# Plot scaled triangle (red)
plot_triangle(scaled_triangle, 'red', 'Scaled')

# Label the plot
plt.title('Transformation of a Triangle')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)
plt.legend()
plt.axis('equal')  # Keep the aspect ratio equal
plt.show()
