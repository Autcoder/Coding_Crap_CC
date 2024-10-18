import numpy as np
import pygame
import random
import matplotlib.pyplot as plt
from collections import deque
import time
from scipy.interpolate import interp1d

# Constants
GREY = (100, 100, 100)
RED = (237, 28, 36)
BLUE = (4, 155, 229)
WHITE = (255, 255, 255)

# Grid Configurations
# BOX_SIZE = int(input("Enter the box size(2, 4, 5, 10, 20, 40, 80, 100): "))
BOX_SIZE = 5
GRID_WIDTH = 1000
STATS_WIDTH = 300
WIDTH = GRID_WIDTH + STATS_WIDTH
HEIGHT = 800
COLUMNS = GRID_WIDTH // BOX_SIZE
ROWS = HEIGHT // BOX_SIZE
TOTAL_BOXES = COLUMNS * ROWS

# Performance Configurations
GRAPH_UPDATE_INTERVAL = 1
MAX_DATA_POINTS = 1000  # Max points to keep for graphing
SIMULATION_SPEED = 60  # FPS
TIMER = 0

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Color Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI", 24)

# Class Definitions

class Grid:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.grid = np.zeros((columns, rows), dtype=int)
        self.initialize_edges()

    def initialize_edges(self):
        # Alternate starting edges between red and blue
        for i in range(self.rows):
            self.grid[0, i] = 1 if i % 2 == 0 else 2
            self.grid[self.columns - 1, i] = 2 if i % 2 == 0 else 1

    def draw(self, window_screen):
        colors = np.array([GREY, RED, BLUE])
        for i in range(self.columns):
            for j in range(self.rows):
                color = tuple(colors[self.grid[i, j]])
                rect = pygame.Rect(i * BOX_SIZE, j * BOX_SIZE, BOX_SIZE, BOX_SIZE)
                pygame.draw.rect(window_screen, color, rect)

    def count_entities(self):
        red_count = np.sum(self.grid == 1)
        blue_count = np.sum(self.grid == 2)
        return red_count, blue_count

class Simulation:
    def __init__(self, grid_width, height, box_size):
        self.grid = Grid(grid_width // box_size, height // box_size)
        self.running = True
        self.stats = {
            'red_wins': 0,
            'blue_wins': 0,
            'red_lost': 0,
            'blue_lost': 0,
            'red_bombs': 0,
            'blue_bombs': 0,
            'red_crosses': 0,
            'blue_crosses': 0
        }
        self.graph_data = {
            'red': deque(maxlen=MAX_DATA_POINTS),
            'blue': deque(maxlen=MAX_DATA_POINTS),
            'time': deque(maxlen=MAX_DATA_POINTS)
        }
        self.time_elapsed = 0
        self.seconds = 0

    def run(self):
        global SECONDS, TIMER
        start_time = time.time()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill((0, 0, 0))
            self.grid.draw(screen)

            red_count, blue_count = self.grid.count_entities()
            if self.seconds % GRAPH_UPDATE_INTERVAL == 0:
                self.update_graph_data(red_count, blue_count)

            if red_count == 0 or blue_count == 0:
                self.running = False

            self.perform_battles(red_count, blue_count)

            self.draw_stats(red_count, blue_count)
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

        self.display_results()
        self.plot_graph()

    # Perform the actual battle
    def perform_battles(self, red_count, blue_count):
        for i in range(self.grid.columns):
            for j in range(self.grid.rows):
                entity = self.grid.grid[i, j]
                if entity in [1, 2]:
                    self.resolve_battles(i, j, entity, red_count, blue_count)

    # Count how many squares are connected
    def count_connected_sqaures(self, i, j, entity, visited):
        if (i, j) in visited:
            return 0
        visited.add((i, j))
        count = 1
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = i + x, j + y
            if 0 <= nx < self.grid.columns and 0 <= ny < self.grid.rows and self.grid.grid[nx, ny] == entity:
                count += self.count_connected_sqaures(nx, ny, entity, visited)
        return count
    
    # Count how many Neighbors are the same color
    def check_neighbors(self, i, j, entity):
        count = 0
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = i + x, j + y
            if 0 <= nx < self.grid.columns and 0 <= ny < self.grid.rows and self.grid.grid[nx, ny] == entity:
                count += 1
        return count

    # Resolve the combat between two entities
    def resolve_battles(self, i, j, entity, red_count, blue_count):
        # Cross pattern attack (up, down, left, right)
        cross_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x, y in cross_directions:
            nx, ny = i + x, j + y
            if 0 <= nx < self.grid.columns and 0 <= ny < self.grid.rows:
                if self.grid.grid[nx, ny] == 0:
                    conquer_chance = 0.01  # Chance to conquer grey squares
                    if random.random() < conquer_chance:
                        self.grid.grid[nx, ny] = entity
                elif self.grid.grid[nx, ny] != entity:
                    battle_result = self.resolve_combat(i, j, nx, ny, entity, red_count, blue_count)
                    if battle_result == 'conquer':
                        if entity == 1:
                            self.stats['red_wins'] += 1
                        else:
                            self.stats['blue_wins'] += 1
                    elif battle_result == 'lost':
                        self.stats['red_lost' if entity == 2 else 'blue_lost'] += 1
                    elif battle_result == 'bomb':
                        if entity == 1:
                            self.stats['red_bombs'] += 1
                        else:
                            self.stats['blue_bombs'] += 1
                    elif battle_result == 'cross':
                        if entity == 1:
                            self.stats['red_crosses'] += 1
                        else:
                            self.stats['blue_crosses'] += 1

    # Resolve what is going to happen between two squares
    def resolve_combat(self, i, j, nx, ny, entity, red_count, blue_count):
        global TOTAL_BOXES
        red_conquer_chance, blue_conquer_chance = 0.005, 0.005
        if entity == 1:  # Red attacking
            conquer_chance = red_conquer_chance
            square_count = red_count
        else:  # Blue attacking
            conquer_chance = blue_conquer_chance
            square_count = blue_count
        connected_squares = self.count_connected_sqaures(i, j, entity, set())
        
        if random.random() < conquer_chance * (square_count / TOTAL_BOXES) * (1 + (connected_squares / TOTAL_BOXES) * 0.01):  # Chance of conquering
            self.grid.grid[nx, ny] = entity
            return 'conquer'
        elif random.random() < 0.01:  # Chance of losing
            self.grid.grid[i, j] = 3 - entity
            return 'lost'
        elif entity == 1 and red_count < blue_count and random.random() < 0.004 / red_count * (blue_count / TOTAL_BOXES):  # Red bomb
            self.bomb_area(i, j, 2)
            return 'bomb'
        elif entity == 2 and blue_count < red_count and random.random() < 0.004 / blue_count * (red_count / TOTAL_BOXES):  # Blue bomb
            self.bomb_area(i, j, 1)
            return 'bomb'
        elif entity == 1 and random.random() < 0.002 / red_count:  # Red cross
            self.cross_area(i, j)
            return 'cross'
        elif entity == 2 and random.random() < 0.002 / blue_count:  # Blue cross
            self.cross_area(i, j)
            return 'cross'
        return 'none'

    # Carry out the Cross Attack, coloring sqaures in the horizontal and vertical direction
    def cross_area(self, i, j):
        # Color the entire row
        for x in range(self.grid.columns):
            self.grid.grid[x][j] = self.grid.grid[i][j]
        
        # Color the entire column
        for y in range(self.grid.rows):
            self.grid.grid[i][y] = self.grid.grid[i][j]

    # Carry out the Bomb Attack, coloring sqaures in a 10x10 area
    def bomb_area(self, i, j, target_entity):
        radius = 10  # 10x10 area bomb
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if 0 <= i + dx < self.grid.columns and 0 <= j + dy < self.grid.rows:
                    if self.grid.grid[i + dx, j + dy] == target_entity:
                        self.grid.grid[i + dx, j + dy] = 3 - target_entity

    # Update the graph data with the current square counts
    def update_graph_data(self, red_count, blue_count):
        self.graph_data['red'].append(red_count)
        self.graph_data['blue'].append(blue_count)
        self.graph_data['time'].append(self.seconds)

    # Draw and Update the stats Panel
    def draw_stats(self, red_count, blue_count):
        global TIMER, TOTAL_BOXES
        stats = [
            f"Time: {TIMER}s",
            f"Total Squares: {TOTAL_BOXES}",
            "",
            f"Red Owned: {red_count}",
            f"Red Wins: {self.stats['red_wins']}",
            f"Red Lost: {self.stats['red_lost']}",
            f"Red Bombs: {self.stats['red_bombs']}",
            f"Red Crosses: {self.stats['red_crosses']}",
            "",
            f"Blue Owned: {blue_count}",
            f"Blue Wins: {self.stats['blue_wins']}",
            f"Blue Lost: {self.stats['blue_lost']}",
            f"Blue Bombs: {self.stats['blue_bombs']}",
            f"Blue Crosses: {self.stats['blue_crosses']}"
        ]
        for i, stat in enumerate(stats):
            text = font.render(stat, True, WHITE)
            screen.blit(text, (GRID_WIDTH + 20, 20 + i * 30))

    # Print the final results in the Terminal
    def display_results(self):
        print("Simulation ended. Final Results:")
        print(f"Red Wins: {self.stats['red_wins']}")
        print(f"Red Lost: {self.stats['red_lost']}")
        print(f"Red Bombs: {self.stats['red_bombs']}")
        print(f"Red Crosses: {self.stats['red_crosses']}")
        print("")
        print(f"Blue Wins: {self.stats['blue_wins']}")
        print(f"Blue Lost: {self.stats['blue_lost']}")
        print(f"Blue Bombs: {self.stats['blue_bombs']}")
        print(f"Blue Crosses: {self.stats['blue_crosses']}")

    # Draw the final graph, showing the evolution of the battle
    def plot_graph(self):
        # Interpolate and smooth the lines
        x = np.array(self.graph_data['time'])
        y_red = np.array(self.graph_data['red'])
        y_blue = np.array(self.graph_data['blue'])

        # Remove duplicates from x
        x_unique, idx = np.unique(x, return_index=True)
        y_red_unique = y_red[idx]
        y_blue_unique = y_blue[idx]

        f_red = interp1d(x_unique, y_red_unique, kind='cubic')
        f_blue = interp1d(x_unique, y_blue_unique, kind='cubic')

        x_new = np.linspace(x_unique.min(), x_unique.max(), num=2000, endpoint=True)
        y_red_new = f_red(x_new)
        y_blue_new = f_blue(x_new)

        plt.figure(figsize=(10, 5))
        plt.plot(x_new, y_red_new, color='red', label='Red Squares')
        plt.plot(x_new, y_blue_new, color='blue', label='Blue Squares')
        plt.xlabel('Time (s)')
        plt.ylabel('Square Count')
        plt.title('Red vs Blue Simulation')
        plt.legend()
        plt.savefig("1colorsim_graph.png", dpi=300)

# Run the Simulation
simulation = Simulation(GRID_WIDTH, HEIGHT, BOX_SIZE)
simulation.run()
pygame.quit()
