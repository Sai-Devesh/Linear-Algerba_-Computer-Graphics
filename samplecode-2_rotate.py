import matplotlib.pyplot as plt
import numpy as np

# Defining the original triangle points (homogeneous coordinates with 1 for translation purposes)
original_triangle = np.array([[1, 1, 1],  # Point A
                              [6, 2, 1],  # Point B
                              [5, 4, 1]])  # Point C

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

theta = np.radians(45)  # 45 degrees in radians
rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                            [np.sin(theta),  np.cos(theta), 0],
                            [0, 0, 1]])

rotated_triangle = matrix_multiply(rotation_matrix, original_triangle.T).T

# Plotting
plt.figure()

# Plot original triangle (blue)
plot_triangle(original_triangle, 'blue', 'Original')

# Plot rotated triangle (green)
plot_triangle(rotated_triangle, 'green', 'Rotated')

# Label the plot
plt.title('Rotation of a Triangle')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)
plt.legend()
plt.axis('equal')  # Keep the aspect ratio equal
plt.show()