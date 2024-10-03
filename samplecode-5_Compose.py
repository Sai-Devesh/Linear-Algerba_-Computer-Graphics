import matplotlib.pyplot as plt
import numpy as np

# Defining the original triangle points (homogeneous coordinates with 1 for translation purposes)
original_triangle = np.array([[1, 1, 1],  # Point A
                              [4, 2, 1],  # Point B
                              [1, 4, 1]])  # Point C

# Function to perform matrix multiplication
def matrix_multiply(matrix1, matrix2):
    return np.dot(matrix1, matrix2)

# Function to plot triangles
def plot_triangle(ax, triangle, color, label):
    triangle = np.vstack([triangle, triangle[0]])  # Closing the triangle
    ax.plot(triangle[:, 0], triangle[:, 1], 'o-', color=color, label=label)
    ax.set_aspect('equal')  # Keep the aspect ratio equal
    ax.grid(True)

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

# Step 1: Apply scaling first
scaled_triangle = matrix_multiply(scaling_matrix, original_triangle.T).T

# Step 2: Apply rotation to the scaled triangle
scaled_rotated_triangle = matrix_multiply(rotation_matrix, scaled_triangle.T).T

# Step 3: Apply translation to the rotated and scaled triangle
scaled_rotated_translated_triangle = matrix_multiply(translation_matrix, scaled_rotated_triangle.T).T

# Now calculate the combined TRS matrix (Translation * Rotation * Scaling)
trs_matrix = matrix_multiply(translation_matrix, matrix_multiply(rotation_matrix, scaling_matrix))

# Apply the combined TRS matrix to the original triangle
final_triangle = matrix_multiply(trs_matrix, original_triangle.T).T

# Creating subplots for side-by-side comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  # Two plots side by side

# Plotting in the first subplot (ax1) - Stepwise transformations
ax1.set_title('Stepwise Transformation (S -> R -> T)')
plot_triangle(ax1, original_triangle, 'blue', 'Original')
plot_triangle(ax1, scaled_triangle, 'red', 'Scaled')
plot_triangle(ax1, scaled_rotated_triangle, 'green', 'Scaled + Rotated')
plot_triangle(ax1, scaled_rotated_translated_triangle, 'black', 'Scaled + Rotated + Translated')
ax1.legend()

# Plotting in the second subplot (ax2) - Final triangle from TRS
ax2.set_title('Final Transformation (TRS Applied)')
plot_triangle(ax2, original_triangle, 'blue', 'Original')
plot_triangle(ax2, final_triangle, 'orange', 'Final (TRS)')
ax2.legend()

# Display the plots side by side
plt.tight_layout()
plt.show()

# Check if final transformation matches the one before TRS
are_same = np.allclose(scaled_rotated_translated_triangle, final_triangle)
print(f"Are the triangles before and after TRS the same? {'Yes' if are_same else 'No'}")
