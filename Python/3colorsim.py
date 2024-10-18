from matplotlib.pylab import random_integers
import numpy as np
import pygame
import random
import matplotlib.pyplot as plt
from collections import deque
import time
from scipy.interpolate import interp1d

# Constants
# Colors
RED = (237, 28, 36)  # Alphabet Red
BLUE = (4, 155, 229)  # German Blue
GREEN = (38, 153, 38) # Dark Pastel Green
ORANGE = (241, 120, 41) # Pastel Orange
YELLOW = (255, 228, 23) # Yellow Flash
PURPLE = (158, 58, 195) # Candy Purple
BLACK = (31, 29, 27) # Black Bronze
WHITE = (248, 243, 239) # Flower White

FONT_WHITE = (255, 255, 255)
GREY = (100, 100, 100)


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
        self.initialize_colors()

    def initialize_colors(self):
        # Define the color palette
        color_palette = {
            1: RED,
            2: BLUE,
            3: GREEN,
            4: ORANGE,
            5: YELLOW,
            6: PURPLE,
            7: BLACK,
            8: WHITE
        }

        for j in range(self.rows):
            # Randomly color the first and last columns
            self.grid[0][j] = random.randint(1, len(color_palette))  # First column
            self.grid[self.columns - 1][j] = random.randint(1, len(color_palette))  # Last column

    def draw(self, window_screen):
        # Map integer values in the grid to their corresponding colors
        color_mapping = {
            0: GREY,
            1: RED,
            2: BLUE,
            3: GREEN,
            4: ORANGE,
            5: YELLOW,
            6: PURPLE,
            7: BLACK,
            8: WHITE
        }

        for i in range(self.columns):
            for j in range(self.rows):
                color = color_mapping.get(self.grid[i, j], GREY)
                rect = pygame.Rect(i * BOX_SIZE, j * BOX_SIZE, BOX_SIZE, BOX_SIZE)
                pygame.draw.rect(window_screen, color, rect)


    def count_entities(self, entity):
        square_count = np.sum(self.grid == entity)
        return square_count

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

            red_count = self.grid.count_entities(1)
            blue_count = self.grid.count_entities(2)
            green_count = self.grid.count_entities(3)
            orange_count = self.grid.count_entities(4)
            yellow_count = self.grid.count_entities(5)
            purple_count = self.grid.count_entities(6)
            black_count = self.grid.count_entities(7)
            white_count = self.grid.count_entities(8)
            
            color_counts = [red_count, blue_count, green_count, orange_count, yellow_count, purple_count, black_count, white_count]
            
            if self.seconds % GRAPH_UPDATE_INTERVAL == 0:
                self.update_graph_data(red_count, blue_count)

            if red_count == 0 or blue_count == 0:
                self.running = False

            self.perform_battles(red_count, blue_count)

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

    # Perform the actual battle
    def perform_battles(self, red_count, blue_count):
        for i in range(self.grid.columns):
            for j in range(self.grid.rows):
                entity = self.grid.grid[i, j]
                if entity in [1, 2]:
                    self.resolve_battles(i, j, entity)

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
    def resolve_battles(self, i, j, entity):
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
                    enemy_entity = self.grid.grid[nx, ny]
                    battle_result = self.resolve_combat(i, j, nx, ny, entity, enemy_entity)
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
    def resolve_combat(self, i, j, nx, ny, entity, enemy_entity):
        global TOTAL_BOXES
        red_conquer_chance, blue_conquer_chance = 0.005, 0.005
        
        if entity == 1:  # Red attacking
            conquer_chance = red_conquer_chance
        else:  # Blue attacking
            conquer_chance = blue_conquer_chance
            
        square_count = self.grid.count_entities(entity)
        enemy_count = self.grid.count_entities(enemy_entity)
        connected_squares = self.count_connected_sqaures(i, j, entity, set())
        
        if random.random() < conquer_chance * (square_count / TOTAL_BOXES) * (1 + (connected_squares / TOTAL_BOXES) * 0.01):  # Chance of conquering
            self.grid.grid[nx, ny] = entity
            return 'conquer'
        elif random.random() < 0.01:  # Chance of losing
            self.grid.grid[i, j] = 3 - entity
            return 'lost'
        elif TIMER > 5:
            if square_count < enemy_count and random.random() < 0.004 / square_count * (enemy_count / TOTAL_BOXES):
                self.bomb_area(i, j, 3 - enemy_entity)
                return 'bomb'
        elif TIMER > 10:            
            if random.random() < 0.002 / square_count:
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
    def draw_stats(self, color_counts):
        global TIMER, TOTAL_BOXES
        stats = [
            f"Time: {TIMER}s",
            f"Total Squares: {TOTAL_BOXES}",
            "",
            f"Red Owned: {color_counts[0]}",
            f"Blue Owned: {color_counts[1]}",
            f"Green Owned: {color_counts[2]}",
            f"Yellow Owned: {color_counts[3]}",
            f"Orange Owned: {color_counts[4]}",
            f"Purple Owned: {color_counts[5]}",
            f"Black Owned: {color_counts[6]}",
            f"White Owned: {color_counts[7]}"
        ]
        for i, stat in enumerate(stats):
            text = font.render(stat, True, FONT_WHITE)
            screen.blit(text, (GRID_WIDTH + 20, 20 + i * 30))

    # Draw the final graph, showing the evolution of the battle
    def plot_graph(self):
        colors = {
            'red': 'r',
            'blue': 'b',
            'green': 'g',
            'orange': 'orange',
            'yellow': 'y',
            'purple': 'purple',
            'black': 'k',
            'white': 'w'
        }
        
        colors_names = {
            'red': "Red",
            'blue': "Blue",
            'green': "Green",
            'orange': "Orange",
            'yellow': "Yellow",
            'purple': "Purple",
            'black': "Black",
            'white': "White"
        }

        for color in self.graph_data:
            if color != 'time':
                x = np.array(self.graph_data['time'])
                y = np.array(self.graph_data[color])

                # Remove duplicates from x
                x_unique, idx = np.unique(x, return_index=True)
                y_unique = y[np.argsort(idx)]  # Ensure y_unique is in the same order as x_unique

                f = interp1d(x_unique, y_unique, kind='cubic')  # cubic interpolation
                x_interp = np.linspace(x_unique.min(), x_unique.max(), 100)  # interpolate at 100 points
                y_interp = f(x_interp)

                plt.plot(x_interp, y_interp, label=f'{colors_names[color]}', color=colors.get(color, 'c'))  # default to cyan if color not found
        plt.xlabel('Time')
        plt.ylabel('Square Count')
        plt.title('Squares Owned Over Time')
        plt.legend()
        plt.savefig("3colorsim_graph.png", dpi=300)

# Run the Simulation
simulation = Simulation(GRID_WIDTH, HEIGHT, BOX_SIZE)
simulation.run()
pygame.quit()
