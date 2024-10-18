import numpy as np
import pygame
import random
import time
import matplotlib.pyplot as plt
from collections import deque
from scipy.interpolate import interp1d

# Constants
BOX_SIZE = 5
GRID_WIDTH = 1000
STATS_WIDTH = 300
WIDTH = GRID_WIDTH + STATS_WIDTH
HEIGHT = 800
COLUMNS = GRID_WIDTH // BOX_SIZE
ROWS = HEIGHT // BOX_SIZE
TOTAL_BOXES = COLUMNS * ROWS

GRAPH_UPDATE_INTERVAL = 1
MAX_DATA_POINTS = 1000
SIMULATION_SPEED = 60
TIMER = 0

# Colors
RED = 1
BLUE = 2
GREEN = 3
ORANGE = 4
YELLOW = 5
PURPLE = 6
BLACK = 7
WHITE = 8
GREY = 0

# Color Mappings for Pygame
color_mapping = {
    GREY: (100, 100, 100),
    RED: (237, 28, 36),
    BLUE: (4, 155, 229),
    GREEN: (38, 153, 38),
    ORANGE: (241, 120, 41),
    YELLOW: (255, 228, 23),
    PURPLE: (158, 58, 195),
    BLACK: (31, 29, 27),
    WHITE: (248, 243, 239)
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI", 24)

class Grid:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.grid = np.zeros((columns, rows), dtype=np.uint8)
        self.initialize_colors()

    def initialize_colors(self):
        for j in range(self.rows):
            self.grid[0, j] = random.randint(1, 8)
            self.grid[self.columns - 1, j] = random.randint(1, 8)

    def draw(self, window_screen):
        unique_values = np.unique(self.grid)
        for i in range(self.columns):
            for j in range(self.rows):
                value = self.grid[i, j]
                if value not in color_mapping:
                    continue
                color = color_mapping[value]
                rect = pygame.Rect(i * BOX_SIZE, j * BOX_SIZE, BOX_SIZE, BOX_SIZE)
                pygame.draw.rect(window_screen, color, rect)
                pygame.draw.rect(window_screen, color, rect)

class Simulation:
    def __init__(self, grid_width, height, box_size):
        self.grid = Grid(grid_width // box_size, height // box_size)
        self.running = True
        self.color_palette = list(range(1, 9))
        self.graph_data = {color: deque(maxlen=MAX_DATA_POINTS) for color in self.color_palette}
        self.graph_data['time'] = deque(maxlen=MAX_DATA_POINTS)  # type: ignore
        self.time_elapsed = 0
        self.seconds = 0

    def run(self):
        global TIMER
        start_time = time.time()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill((0, 0, 0))
            self.grid.draw(screen)

            color_counts = np.bincount(self.grid.grid.flatten(), minlength=9)[1:]
            if self.seconds % GRAPH_UPDATE_INTERVAL == 0:
                self.update_graph_data(color_counts)

            if all(count == 0 for count in color_counts):
                self.running = False

            self.perform_battles()

            self.draw_stats(color_counts)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.running = False

            pygame.display.flip()
            clock.tick(SIMULATION_SPEED)
            self.time_elapsed += 1
            if self.time_elapsed >= SIMULATION_SPEED:
                self.time_elapsed = 0
                self.seconds += 1

            if time.time() - start_time >= 1:
                start_time = time.time()
                TIMER += 1

        self.plot_graph()

    def perform_battles(self):
        grid = self.grid.grid
        for i in range(self.grid.columns):
            for j in range(self.grid.rows):
                entity = grid[i, j]
                if entity != 0:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < self.grid.columns and 0 <= ny < self.grid.rows:
                            if grid[nx, ny] == 0:
                                conquer_chance = 0.01
                                if random.random() < conquer_chance:
                                    grid[nx, ny] = entity
                            else:
                                enemy_entity = grid[nx, ny]
                                if enemy_entity != entity:
                                    conquer_chance = 0.005
                                    if random.random() < conquer_chance * (np.sum(grid == entity) / TOTAL_BOXES) * (1 + (np.sum(grid == entity) / TOTAL_BOXES) * 0.01):
                                        grid[nx, ny] = entity
                                    elif random.random() < 0.01:
                                        grid[i, j] = enemy_entity
                                    elif TIMER > 5:
                                        if np.sum(grid == entity) < np.sum(grid == enemy_entity) and random.random() < 0.004 / np.sum(grid == entity) * (np.sum(grid == enemy_entity) / TOTAL_BOXES):
                                            self.bomb_area(i, j, enemy_entity)
                                    elif TIMER > 10:
                                        if random.random() < 0.002 / np.sum(grid == entity):
                                            self.cross_area(i, j)

    def cross_area(self, i, j):
        grid = self.grid.grid
        for x in range(self.grid.columns):
            grid[x, j] = grid[i, j]

    def bomb_area(self, i, j, target_entity):
        grid = self.grid.grid
        radius = 10
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if 0 <= i + dx < self.grid.columns and 0 <= j + dy < self.grid.rows:
                    if grid[i + dx, j + dy] == target_entity:
                        grid[i + dx, j + dy] = 3 - target_entity

    def update_graph_data(self, color_counts):
        for color in self.color_palette:
            self.graph_data[color].append(color_counts[color - 1])
        self.graph_data['time'].append(self.seconds)  # type: ignore

    def draw_stats(self, color_counts):
        stats = [
            f"Time: {TIMER}s",
            f"Total Squares: {TOTAL_BOXES}",
            ""
        ]

        colors = {
            1: "Red",
            2: "Blue",
            3: "Green",
            4: "Orange",
            5: "Yellow",
            6: "Purple",
            7: "Black",
            8: "White"
        }
        for color, count in enumerate(color_counts, start=1):
            stats.append(f"{colors[color]} Owned: {count}")

        for i, stat in enumerate(stats):
            text = font.render(stat, True, (255, 255, 255))
            screen.blit(text, (GRID_WIDTH + 20, 20 + i * 30))

    def plot_graph(self):
        colors = {
            1: 'r',    # Red
            2: 'b',    # Blue
            3: 'g',    # Green
            4: 'orange', # Orange
            5: 'y',    # Yellow
            6: 'purple', # Purple
            7: 'black', # Black
            8: 'grey', # White
        }
        
        for color in self.graph_data:
            if color != 'time':
                x = np.array(self.graph_data['time']) # type: ignore
                y = np.array(self.graph_data[color])

                # Remove duplicates from x
                x_unique, idx = np.unique(x, return_index=True)
                y_unique = y[idx]

                if len(x_unique) >= 4:  # Ensure there are enough points for cubic interpolation
                    f = interp1d(x_unique, y_unique, kind='cubic')  # cubic interpolation
                    x_interp = np.linspace(x_unique.min(), x_unique.max(), 100)  # interpolate at 100 points
                    y_interp = f(x_interp)
                else:
                    # Fallback to linear interpolation if not enough points for cubic
                    f = interp1d(x_unique, y_unique, kind='linear')
                    x_interp = np.linspace(x_unique.min(), x_unique.max(), 100)
                    y_interp = f(x_interp)

                plt.plot(x_interp, y_interp, label=f'{color}', color=colors.get(color, 'c'))  # default to cyan if color not found

        plt.xlabel('Time')
        plt.ylabel('Square Count')
        plt.title('Squares Owned Over Time')
        plt.legend()
        plt.savefig("6colorsim_graph.png", dpi = 300)


# Run the Simulation
simulation = Simulation(GRID_WIDTH, HEIGHT, BOX_SIZE)
simulation.run()
pygame.quit()
