import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import matplotlib.animation as animation
import random

# Linear transformation for rotation
def rotation_matrix(angle_deg):
    angle_rad = np.radians(angle_deg)
    return np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])

# Linear transformation for translation
def translate(position, translation):
    return position + translation

# Function to handle screen boundaries (no wrapping, stays at the edge)
def constrain_position(position, velocity, xlim, ylim):
    if position[0] < xlim[0]:
        position[0] = xlim[0]
        velocity[0] = 0
    elif position[0] > xlim[1]:
        position[0] = xlim[1]
        velocity[0] = 0
    
    if position[1] < ylim[0]:
        position[1] = ylim[0]
        velocity[1] = 0
    elif position[1] > ylim[1]:
        position[1] = ylim[1]
        velocity[1] = 0

    return position, velocity

# Function to handle screen wrapping (for asteroids only)
def wrap_position(position, xlim, ylim):
    if position[0] < xlim[0]:
        position[0] = xlim[1]
    elif position[0] > xlim[1]:
        position[0] = xlim[0]
    
    if position[1] < ylim[0]:
        position[1] = ylim[1]
    elif position[1] > ylim[1]:
        position[1] = ylim[0]
    
    return position

# Class to represent the spaceship
class Spaceship:
    def __init__(self, xlim, ylim):
        self.position = np.array([0.0, 0.0])
        self.direction = np.array([0.0, 1.0])
        self.angle = 0  # Angle in degrees
        self.velocity = np.array([0.0, 0.0])
        self.shape = np.array([[0, 1], [-0.5, -1], [0.5, -1]])  # Triangle shape
        self.xlim = xlim
        self.ylim = ylim
    
    def rotate(self, angle_delta):
        self.angle += angle_delta
        rotation = rotation_matrix(self.angle)
        self.direction = np.dot(rotation, np.array([0, 1]))
    
    def thrust(self, acceleration):
        self.velocity += self.direction * acceleration

    def update(self):
        self.position, self.velocity = constrain_position(self.position, self.velocity, self.xlim, self.ylim)
        self.position = translate(self.position, self.velocity)
    
    def get_transformed_shape(self):
        rotation = rotation_matrix(self.angle)
        rotated_shape = np.dot(self.shape, rotation.T)
        return rotated_shape + self.position

    def respawn(self, asteroids, power_ups):
        # Randomly place spaceship in a position that doesn't overlap with asteroids or power-ups
        while True:
            new_position = np.array([random.uniform(self.xlim[0], self.xlim[1]), random.uniform(self.ylim[0], self.ylim[1])])
            # Check for collisions with asteroids and power-ups
            no_collision = all(np.linalg.norm(asteroid.position - new_position) > asteroid.size for asteroid in asteroids) and \
                           all(np.linalg.norm(power_up.position - new_position) > 0.5 for power_up in power_ups if not power_up.collected)
            if no_collision:
                self.position = new_position
                self.velocity = np.array([0.0, 0.0])
                break

# Class to represent an asteroid
class Asteroid:
    def __init__(self, position, velocity, size, xlim, ylim):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.size = size
        self.initial_size = size  # Initial size to prevent overgrowth
        self.xlim = xlim
        self.ylim = ylim
        self.shape = np.array([[0, 1], [-1, -1], [1, -1], [1.5, 0]])

    def update(self):
        self.position = translate(self.position, self.velocity)
        self.position = wrap_position(self.position, self.xlim, self.ylim)  # Ensure asteroids wrap

    def get_transformed_shape(self):
        return self.shape * self.size + self.position

    def grow(self):
        if self.size < self.initial_size:  # Asteroids can't grow beyond their initial size
            self.size *= 1.1  # Grow by 10%
    
    def shrink(self):
        self.size *= 0.9  # Shrink by 10%
    
    def is_too_small(self):
        return self.size < 0.3  # Threshold for asteroid size

# Class to represent power-ups
class PowerUp:
    def __init__(self, xlim, ylim):
        self.position = np.array([random.uniform(xlim[0], xlim[1]), random.uniform(ylim[0], ylim[1])])
        self.collected = False

    def get_shape(self):
        return self.position

    def check_collision(self, spaceship_pos):
        dist = np.linalg.norm(self.position - spaceship_pos)
        return dist < 0.5  # Check collision with spaceship (radius of 0.5 units)

# Game setup
class AsteroidsGame:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.xlim = (-10, 10)
        self.ylim = (-10, 10)
        self.spaceship = Spaceship(self.xlim, self.ylim)
        self.asteroids = [
            Asteroid([5, 5], [-0.01, -0.02], 2, self.xlim, self.ylim),
            Asteroid([-5, -5], [0.02, 0.01], 1.5, self.xlim, self.ylim)
        ]
        self.power_ups = [PowerUp(self.xlim, self.ylim) for _ in range(2)]  # Start with two power-ups
        self.score = 0
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=50)
        self.key_state = {'left': False, 'right': False, 'up': False}
        
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)
    
    def on_key_press(self, event):
        if event.key == 'left':
            self.key_state['left'] = True
        elif event.key == 'right':
            self.key_state['right'] = True
        elif event.key == 'up':
            self.key_state['up'] = True

    def on_key_release(self, event):
        if event.key == 'left':
            self.key_state['left'] = False
        elif event.key == 'right':
            self.key_state['right'] = False
        elif event.key == 'up':
            self.key_state['up'] = False
    
    def check_power_up_collision(self):
        collected_power_ups = 0
        for power_up in self.power_ups:
            if not power_up.collected and power_up.check_collision(self.spaceship.position):
                power_up.collected = True
                self.score += 1
                collected_power_ups += 1
                for asteroid in self.asteroids:
                    asteroid.shrink()  # Shrink asteroids
                print(f"Power-up collected! Score: {self.score}")

        # Check if all power-ups have been collected
        if all(power_up.collected for power_up in self.power_ups):
            self.power_ups = [PowerUp(self.xlim, self.ylim) for _ in range(2)]  # Spawn two new power-ups
            print("New power-ups spawned!")

    def check_asteroid_collision(self):
        for asteroid in self.asteroids:
            dist = np.linalg.norm(asteroid.position - self.spaceship.position)
            if dist < asteroid.size:
                self.score = max(0, self.score - 1)  # Lose 1 point
                self.spaceship.respawn(self.asteroids, self.power_ups)  # Respawn the spaceship
                asteroid.grow()  # Increase asteroid size
                print(f"Hit an asteroid! Score: {self.score}")
    
    def check_game_over(self):
        if all([asteroid.is_too_small() for asteroid in self.asteroids]):
            print("You win! All asteroids reduced to a small size.")
            plt.close(self.fig)

        if self.score >= 10:  # Win condition: score reaches 10
            print("You win! Score reached 10.")
            plt.close(self.fig)
    
    def update(self, frame):
        self.ax.clear()
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        self.ax.set_aspect('equal')

        # Control spaceship movement
        if self.key_state['left']:
            self.spaceship.rotate(5)  # Rotate counterclockwise
        if self.key_state['right']:
            self.spaceship.rotate(-5)  # Rotate clockwise
        if self.key_state['up']:
            self.spaceship.thrust(0.02)  # Thrust forward with lower speed
        
        self.spaceship.update()

        # Draw spaceship
        spaceship_shape = self.spaceship.get_transformed_shape()
        spaceship_polygon = Polygon(spaceship_shape, closed=True, color='blue')
        self.ax.add_patch(spaceship_polygon)

        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.update()
            asteroid_shape = asteroid.get_transformed_shape()
            asteroid_polygon = Polygon(asteroid_shape, closed=True, color='red')
            self.ax.add_patch(asteroid_polygon)
        
        # Draw power-ups
        for power_up in self.power_ups:
            if not power_up.collected:
                power_up_circle = Circle(power_up.get_shape(), radius=0.3, color='green')
                self.ax.add_patch(power_up_circle)
        
        # Check for collisions
        self.check_power_up_collision()
        self.check_asteroid_collision()
        
        # Check game over
        self.check_game_over()

game = AsteroidsGame()
plt.show()
