import matplotlib.pyplot as plt
import numpy as np

# Defining the original triangle points (homogeneous coordinates with 1 for translation purposes)
original_triangle = np.array([[4, 2, 1],  # Point A
                              [4, 4, 1],  # Point B
                              [6, 4, 1]])  # Point C

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

# Defining transformation matrices

# 3. Scaling Matrix (scaling by a factor of 0.5 on x and y axes)
scaling_matrix = np.array([[0.5, 0, 0],
                           [0, 0.5, 0],
                           [0, 0, 0.5]])

# Apply transformations using matrix_multiplication
scaled_triangle = matrix_multiply(scaling_matrix, original_triangle.T).T

# Plotting
plt.figure()

# Plot original triangle (blue)
plot_triangle(original_triangle, 'blue', 'Original')
# Plot scaled triangle (red)
plot_triangle(scaled_triangle, 'red', 'Scaled')

# Label the plot
plt.title('Scaling of a Triangle')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)
plt.legend()
plt.axis('equal')  # Keep the aspect ratio equal
plt.show()
