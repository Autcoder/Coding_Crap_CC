import random
import pygame
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Constants for Colors
GREY = (100, 100, 100)
RED = (237, 28, 36) # Alphabet Red
BLUE = (4, 155, 229) # German Blue
WHITE = (255, 255, 255)

# Grid Configuration
BOX_SIZE = 5
GRID_WIDTH = 1000
STATS_WIDTH = 300  # Width of the stats panel
WIDTH = GRID_WIDTH + STATS_WIDTH  # Total width of the window
HEIGHT = 800
COLUMNS = GRID_WIDTH // BOX_SIZE
ROWS = HEIGHT // BOX_SIZE

SECONDS = 0
GRAPH_UPDATE_INTERVAL = 2

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Color Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segue UI", 24)  # Font for the stats display

# Grid Class
class Grid:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.grid = [[0 for _ in range(rows)] for _ in range(columns)]
        self.initialize_edges()

    def initialize_edges(self):
        for i in range(self.rows):
            if i % 2 == 0:
                self.grid[0][i] = 1  # Red
                self.grid[self.columns - 1][i] = 2  # Blue
            else:
                self.grid[0][i] = 2  # Blue
                self.grid[self.columns - 1][i] = 1  # Red

    def draw(self, window_screen):
        for i in range(self.columns):
            for j in range(self.rows):
                color = GREY if self.grid[i][j] == 0 else (RED if self.grid[i][j] == 1 else BLUE)
                rect = pygame.Rect(i * BOX_SIZE, j * BOX_SIZE, BOX_SIZE, BOX_SIZE)
                pygame.draw.rect(window_screen, color, rect)

    def count_entities(self):
        red_count, blue_count = 0, 0
        for i in range(self.columns):
            for j in range(self.rows):
                if self.grid[i][j] == 1:
                    red_count += 1
                elif self.grid[i][j] == 2:
                    blue_count += 1
        return red_count, blue_count

# Battle Class
class Battle:
    def __init__(self, grid, red_count, blue_count):
        self.grid = grid
        self.red_count = red_count
        self.blue_count = blue_count
        self.total_boxes = grid.columns * grid.rows

    def calc_chances(self):
        red_ratio = self.red_count / self.total_boxes
        blue_ratio = self.blue_count / self.total_boxes

        base_conquer_chance = 0.005
        base_lost_chance = 0.01
        base_bomb_chance = 0.005
        base_cross_chance = 0.005

        red_conquer_blue_chance = base_conquer_chance * red_ratio
        red_lost_chance = base_lost_chance / (self.red_count if self.red_count > 0 else 1)
        red_bomb_chance = base_bomb_chance * (1 / self.red_count if self.red_count > 0 else 1) * (self.blue_count / self.total_boxes)
        red_cross_chance = base_cross_chance * (red_ratio / (self.red_count + 1)) * (self.blue_count / self.total_boxes)

        blue_conquer_red_chance = base_conquer_chance * blue_ratio
        blue_lost_chance = base_lost_chance / (self.blue_count if self.blue_count > 0 else 1)
        blue_bomb_chance = base_bomb_chance * (1 / self.blue_count if self.blue_count > 0 else 1) * (self.red_count / self.total_boxes)
        blue_cross_chance = base_cross_chance * blue_ratio / (self.blue_count + 1) * (self.red_count / self.total_boxes)

        return red_conquer_blue_chance, red_lost_chance, red_bomb_chance, red_cross_chance, blue_conquer_red_chance, blue_lost_chance, blue_bomb_chance, blue_cross_chance

    def bomb_red(self, i, j):
        # Every square in a 10×10 radius becomes red
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                bomb_nx, bomb_nj = i + dx, j + dy
                if 0 <= bomb_nx < self.grid.columns and 0 <= bomb_nj < self.grid.rows and self.grid.grid[bomb_nx][bomb_nj] == 2:
                    self.grid.grid[bomb_nx][bomb_nj] = 1
        self.grid.grid[i][j] = 2
        
    def bomb_blue(self, i, j):
        # Every square in a 10×10 radius becomes blue
        for dx in range(-10, 11):
            for dy in range(-10, 11):
                bomb_nx, bomb_nj = i + dx, j + dy
                if 0 <= bomb_nx < self.grid.columns and 0 <= bomb_nj < self.grid.rows and self.grid.grid[bomb_nx][bomb_nj] == 1:
                    self.grid.grid[bomb_nx][bomb_nj] = 2
        self.grid.grid[i][j] = 1
        
    def red_cross(self, i ,j):
        # Sets all squares in the horizontal and vertical line to red.
        for dx in range(-self.grid.columns, self.grid.columns):
            if 0 <= i + dx < self.grid.columns:
                self.grid.grid[i + dx][j] = 1
        for dy in range(-self.grid.rows, self.grid.rows):
            if 0 <= j + dy < self.grid.rows:
                self.grid.grid[i][j + dy] = 1
        self.grid.grid[i][j] = 1
        
    def blue_cross(self, i ,j):
        # Sets all squares in the horizontal and vertical line to blue.
        for dx in range(-self.grid.columns, self.grid.columns):
            if 0 <= i + dx < self.grid.columns:
                self.grid.grid[i + dx][j] = 2
        for dy in range(-self.grid.rows, self.grid.rows):
            if 0 <= j + dy < self.grid.rows:
                self.grid.grid[i][j + dy] = 2
        self.grid.grid[i][j] = 2
        
    def resolve_battle(self, i, j, nx, nj, entity_type, conquer_chance, lost_chance, bomb_chance, cross_chance):
        global SECONDS

        if random.random() < conquer_chance:
            self.grid.grid[nx][nj] = entity_type
            return 'conquer'
        elif random.random() < lost_chance:
            self.grid.grid[i][j] = 3 - entity_type  # Switch to the opposite entity
            return 'lost'
        elif entity_type == 1 and self.red_count < self.blue_count and random.random() < bomb_chance:
            self.bomb_red(i, j)
            return 'bomb'
        elif entity_type == 2 and self.blue_count < self.red_count and random.random() < bomb_chance:
            self.bomb_blue(i, j)
            return 'bomb'
        elif entity_type == 1 and random.random() < cross_chance:
            self.red_cross(i, j)
            return 'cross'
        elif entity_type == 2 and random.random() < cross_chance:
            self.blue_cross(i, j)
            return 'cross'
        return 'none'

# Graph Class
class Graph:
    def __init__(self):
        self.points_red = []
        self.points_blue = []
        self.timestamps = []  # To keep track of time in seconds

    def update_graph(self, red_count, blue_count, time_elapsed):
        self.points_red.append(red_count)
        self.points_blue.append(blue_count)
        self.timestamps.append(time_elapsed)

    def draw_graph(self):
        global RED, BLUE
        x = self.timestamps
        y1 = np.array(self.points_red)
        y2 = np.array(self.points_blue)

        # Remove duplicates from x
        x_unique, idx = np.unique(x, return_index=True)
        y1_unique = y1[idx]
        y2_unique = y2[idx]

        x_smooth = np.linspace(x_unique[0], x_unique[-1], 500)
        f1 = interp1d(x_unique, y1_unique, kind='cubic')
        f2 = interp1d(x_unique, y2_unique, kind='cubic')
        y1_smooth = f1(x_smooth)
        y2_smooth = f2(x_smooth)

        plt.figure(figsize=(10, 5))
        plt.plot(x_smooth, y1_smooth, color='RED', label='Red Squares')
        plt.plot(x_smooth, y2_smooth, color='BLUE', label='Blue Squares')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Number of Squares')
        plt.title('Evolution of Owned Squares Over Time')
        plt.legend()
        plt.ylim(0, COLUMNS * ROWS)  # Y-axis range from 0 to 8000
        plt.grid(True)
        plt.savefig("2colorsim_graph.png", dpi=300)

# Simulation Class
class Simulation:
    def __init__(self, grid_width, height, box_size):
        self.grid = Grid(grid_width // box_size, height // box_size)
        self.running = True
        self.battles_won_red = 0
        self.battles_won_blue = 0
        self.terribly_lost_red = 0
        self.terribly_lost_blue = 0
        self.cross_red = 0
        self.cross_blue = 0
        self.bomb_red = 0
        self.bomb_blue = 0
        self.graph = Graph()
        self.time_elapsed = 0  # Time elapsed in seconds

    def run(self):
        global SECONDS
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill((0, 0, 0))
            self.grid.draw(screen)

            red_count, blue_count = self.grid.count_entities()
            if SECONDS % GRAPH_UPDATE_INTERVAL == 0:
                self.graph.update_graph(red_count, blue_count, SECONDS)

            if red_count == self.grid.columns * self.grid.rows or blue_count == self.grid.columns * self.grid.rows:
                self.running = False

            battle = Battle(self.grid, red_count, blue_count)
            red_conquer_blue_chance, red_lost_chance, red_bomb_chance, red_cross_chance, blue_conquer_red_chance, blue_lost_chance, blue_bomb_chance, blue_cross_chance = battle.calc_chances()

            for i in range(self.grid.columns):
                for j in range(self.grid.rows):
                    if self.grid.grid[i][j] != 0:  # If the box is not grey
                        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, nj = i + x, j + y
                            if 0 <= nx < self.grid.columns and 0 <= nj < self.grid.rows:
                                if self.grid.grid[nx][nj] == 0:
                                    if random.random() < 0.01:  # Chance of conquering grey
                                        self.grid.grid[nx][nj] = self.grid.grid[i][j]
                                elif self.grid.grid[i][j] == 1 and self.grid.grid[nx][nj] == 2:
                                    result = battle.resolve_battle(i, j, nx, nj, 1, red_conquer_blue_chance, red_lost_chance, red_bomb_chance, red_cross_chance)
                                    if result == 'conquer':
                                        self.battles_won_red += 1
                                    elif result == 'lost':
                                        self.terribly_lost_red += 1
                                    elif result == 'bomb':
                                        self.bomb_red += 1
                                    elif result == 'cross':
                                        self.cross_red += 1
                                elif self.grid.grid[i][j] == 2 and self.grid.grid[nx][nj] == 1:
                                    result = battle.resolve_battle(i, j, nx, nj, 2, blue_conquer_red_chance, blue_lost_chance, blue_bomb_chance, blue_cross_chance)
                                    if result == 'conquer':
                                        self.battles_won_blue += 1
                                    elif result == 'lost':
                                        self.terribly_lost_blue += 1
                                    elif result == 'bomb':
                                        self.bomb_blue += 1
                                    elif result == 'cross':
                                        self.cross_blue += 1

            self.draw_stats(red_count, blue_count)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.running = False

            pygame.display.flip()
            clock.tick(60)
            self.time_elapsed += 1 # Increment time every frame
            if self.time_elapsed >= 60:
                self.time_elapsed = 0
                SECONDS += 1

        self.print_results()
        self.graph.draw_graph()

    def draw_stats(self, red_count, blue_count):
        # Total boxes
        total_boxes = self.grid.columns * self.grid.rows

        # Stats to display
        stats = [
            f"Total Boxes: {total_boxes}",
            "",
            f"Red Owned: {red_count}",
            f"Red Battles Won: {self.battles_won_red}",
            f"Red Battles Lost: {self.terribly_lost_red}",
            f"Red Bombs: {self.bomb_red}",
            f"Red Crosses: {self.cross_red}",
            "",
            f"Blue Owned: {blue_count}",
            f"Blue Battles Won: {self.battles_won_blue}",
            f"Blue Battles Lost: {self.terribly_lost_blue}",
            f"Blue Bombs: {self.bomb_blue}",
            f"Blue Crosses: {self.cross_blue}"
        ]

        # Draw the stats
        for i, stat in enumerate(stats):
            text = font.render(stat, True, WHITE)
            screen.blit(text, (GRID_WIDTH + 20, 20 + i * 30))

    def print_results(self):
        print("\nRed battles won:", self.battles_won_red)
        print("Red battles lost:", self.terribly_lost_red)
        print("Red bombs:", self.bomb_red)
        print("Red crosses:", self.cross_red)
        print("Blue battles won:", self.battles_won_blue)
        print("Blue battles lost:", self.terribly_lost_blue)
        print("Blue bombs:", self.bomb_blue)
        print("Blue crosses:", self.cross_blue)

# Run the Simulation
simulation = Simulation(GRID_WIDTH, HEIGHT, BOX_SIZE)
simulation.run()

pygame.quit()
