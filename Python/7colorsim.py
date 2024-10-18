#!/usr/bin/env python3

import numpy as np
import random
import pygame
import time
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Constants
GRID_WIDTH, GRID_HEIGHT = 200, 160  # 1000x800 px grid, 5x5 px squares
SQUARE_SIZE = 5
WIDTH, HEIGHT = GRID_WIDTH * SQUARE_SIZE, GRID_HEIGHT * SQUARE_SIZE
SIDE_PANEL_WIDTH = 300
SECONDS = 0
COLOR_THEMES = [
    "old disney", 
    "default", 
    "vintage sunset", 
    "tropical breeze", 
    "cyberpunk", 
    "pastel dreams",
    "forest glade",
    "sunrise glow",
    "cool blues",
    "desert dusk",
    "neon vibes",
    "earthy tones",
    "moody blues",
    "candy pop",
    "autumn leaves",
    "winter chill",
    "retro vibes",
    "lavender fields",
    "deep ocean",
    "spring bloom"
]

COLORS = {}
play_colors = []

# Game variables
while True:
    total_colors = int(input("Enter the number of colors playing in the Simulation (1-8): "))
    if 1 <= total_colors <= 8:
        break

def choose_color_theme():
    global color_theme, COLORS
    if color_theme == 0:
        COLORS = {
            'RED': (230, 57, 70),  # Sunset Red
            'BLUE': (69, 123, 157),  # Ocean Blue
            'GREEN': (42, 157, 143),  # Forest Green
            'ORANGE': (244, 162, 97),  # Sunset Orange
            'YELLOW': (233, 196, 106),  # Golden Yellow
            'PURPLE': (162, 155, 254),  # Lavender Purple
            'BLACK': (44, 44, 84),  # Midnight Black
            'WHITE': (250, 243, 221),  # Cream White
            'GREY': (211, 211, 211)  # Soft Grey
        }
    elif color_theme == 1:
        COLORS = {
            'RED': (237, 28, 36),  # Alphabet Red
            'BLUE': (4, 155, 229),  # German Blue
            'GREEN': (38, 153, 38),  # Dark Pastel Green
            'ORANGE': (241, 120, 41),  # Pastel Orange
            'YELLOW': (255, 228, 23),  # Yellow Flash
            'PURPLE': (88, 24, 118),  # Candy Purple
            'BLACK': (31, 29, 27),  # Black Bronze
            'WHITE': (248, 243, 239),  # Flower White
            'GREY': (100, 100, 100)  # Neutral Grey
        }
    elif color_theme == 2:
        COLORS = {
            'RED': (235, 94, 92),  # Coral Red
            'BLUE': (59, 130, 189),  # Sky Blue
            'GREEN': (120, 177, 89),  # Moss Green
            'ORANGE': (242, 157, 44),  # Golden Orange
            'YELLOW': (252, 211, 77),  # Sunflower Yellow
            'PURPLE': (170, 144, 200),  # Lilac Purple
            'BLACK': (64, 64, 64),  # Slate Black
            'WHITE': (240, 235, 216),  # Linen White
            'GREY': (200, 200, 200)  # Light Stone Grey
        }
    elif color_theme == 3:
        COLORS = {
            'RED': (255, 87, 94),  # Tropical Punch Red
            'BLUE': (89, 205, 244),  # Lagoon Blue
            'GREEN': (85, 191, 133),  # Palm Green
            'ORANGE': (255, 161, 101),  # Mango Orange
            'YELLOW': (255, 223, 103),  # Pineapple Yellow
            'PURPLE': (150, 111, 214),  # Orchid Purple
            'BLACK': (43, 45, 66),  # Deep Charcoal
            'WHITE': (255, 250, 240),  # Coconut White
            'GREY': (220, 220, 220)  # Beach Sand Grey
        }
    elif color_theme == 4:
        COLORS = {
            'RED': (255, 53, 139),  # Neon Pink
            'BLUE': (0, 229, 255),  # Electric Blue
            'GREEN': (0, 255, 135),  # Laser Green
            'ORANGE': (255, 140, 0),  # Neon Tangerine
            'YELLOW': (255, 233, 0),  # Cyber Yellow
            'PURPLE': (177, 0, 255),  # Ultraviolet
            'BLACK': (18, 18, 18),  # Pitch Black
            'WHITE': (255, 255, 255),  # Pure White
            'GREY': (128, 128, 128)  # Steel Grey
        }
    elif color_theme == 5:
        COLORS = {
            'RED': (255, 153, 153),  # Soft Rose
            'BLUE': (153, 204, 255),  # Baby Blue
            'GREEN': (153, 255, 204),  # Mint Green
            'ORANGE': (255, 204, 153),  # Peach
            'YELLOW': (255, 255, 153),  # Lemon Chiffon
            'PURPLE': (204, 153, 255),  # Lavender Blush
            'BLACK': (102, 102, 102),  # Cool Grey
            'WHITE': (255, 250, 240),  # Ivory White
            'GREY': (230, 230, 230)  # Misty Grey
        }
    elif color_theme == 6:
        COLORS = {
            'RED': (153, 63, 52),  # Redwood
            'BLUE': (76, 114, 176),  # Mountain Blue
            'GREEN': (34, 139, 34),  # Forest Green
            'ORANGE': (202, 113, 77),  # Bark Orange
            'YELLOW': (240, 230, 140),  # Pineapple Sage
            'PURPLE': (102, 51, 153),  # Plum Purple
            'BLACK': (54, 69, 79),  # Pine Charcoal
            'WHITE': (245, 245, 245),  # Birch White
            'GREY': (169, 169, 169)  # Granite Grey
        }
    elif color_theme == 7:
        COLORS = {
            'RED': (255, 99, 71),  # Tomato Red
            'BLUE': (135, 206, 235),  # Sky Blue
            'GREEN': (152, 251, 152),  # Pale Green
            'ORANGE': (255, 165, 79),  # Apricot Orange
            'YELLOW': (255, 239, 128),  # Buttercup Yellow
            'PURPLE': (218, 112, 214),  # Orchid Purple
            'BLACK': (75, 75, 75),  # Shadow Black
            'WHITE': (255, 245, 238),  # Seashell White
            'GREY': (211, 211, 211)  # Cloud Grey
        }
    elif color_theme == 8:
        COLORS = {
            'RED': (204, 102, 102),  # Muted Coral
            'BLUE': (70, 130, 180),  # Steel Blue
            'GREEN': (46, 139, 87),  # Sea Green
            'ORANGE': (210, 105, 30),  # Burnt Sienna
            'YELLOW': (240, 230, 140),  # Khaki Yellow
            'PURPLE': (106, 90, 205),  # Slate Blue
            'BLACK': (47, 79, 79),  # Dark Slate
            'WHITE': (245, 245, 245),  # White Smoke
            'GREY': (128, 128, 128)  # Slate Grey
        }
    elif color_theme == 9:
        COLORS = {
            'RED': (205, 92, 92),  # Indian Red
            'BLUE': (100, 149, 237),  # Cornflower Blue
            'GREEN': (143, 188, 143),  # Sage Green
            'ORANGE': (244, 164, 96),  # Sandy Brown
            'YELLOW': (238, 232, 170),  # Pale Goldenrod
            'PURPLE': (186, 85, 211),  # Medium Orchid
            'BLACK': (72, 61, 139),  # Dark Slate Blue
            'WHITE': (250, 235, 215),  # Antique White
            'GREY': (192, 192, 192)  # Desert Sand Grey
        }
    elif color_theme == 10:
        COLORS = {
            'RED': (255, 51, 51),  # Neon Red
            'BLUE': (51, 102, 255),  # Neon Blue
            'GREEN': (51, 255, 51),  # Neon Green
            'ORANGE': (255, 153, 51),  # Neon Orange
            'YELLOW': (255, 255, 51),  # Neon Yellow
            'PURPLE': (153, 51, 255),  # Neon Purple
            'BLACK': (25, 25, 25),  # Jet Black
            'WHITE': (255, 255, 255),  # Pure White
            'GREY': (169, 169, 169)  # Neutral Grey
        }
    elif color_theme == 11:
        COLORS = {
            'RED': (178, 34, 34),  # Firebrick Red
            'BLUE': (70, 130, 180),  # Sky Slate Blue
            'GREEN': (85, 107, 47),  # Olive Drab
            'ORANGE': (210, 105, 30),  # Chestnut Orange
            'YELLOW': (189, 183, 107),  # Pale Khaki
            'PURPLE': (147, 112, 219),  # Medium Purple
            'BLACK': (42, 42, 42),  # Earth Black
            'WHITE': (255, 250, 240),  # Floral White
            'GREY': (128, 128, 128)  # Warm Grey
        }
    elif color_theme == 12:  # "moody blues"
        COLORS = {
            'RED': (128, 0, 0),  # Maroon
            'BLUE': (25, 25, 112),  # Midnight Blue
            'GREEN': (47, 79, 79),  # Dark Sea Green
            'ORANGE': (139, 69, 19),  # Saddle Brown
            'YELLOW': (189, 183, 107),  # Dark Khaki
            'PURPLE': (72, 61, 139),  # Dark Slate Blue
            'BLACK': (0, 0, 0),  # Pure Black
            'WHITE': (245, 245, 245),  # White Smoke
            'GREY': (105, 105, 105)  # Dim Grey
        }
    elif color_theme == 13:  # "candy pop"
        COLORS = {
            'RED': (255, 105, 97),  # Candy Red
            'BLUE': (97, 168, 255),  # Bubblegum Blue
            'GREEN': (144, 238, 144),  # Light Green
            'ORANGE': (255, 182, 89),  # Peach
            'YELLOW': (255, 255, 128),  # Banana Yellow
            'PURPLE': (238, 130, 238),  # Violet
            'BLACK': (169, 126, 182) ,  # Blackberry Sorbet
            'WHITE': (255, 250, 250),  # Snow White
            'GREY': (169, 169, 169)  # Light Grey
        }
    elif color_theme == 14:  # "autumn leaves"
        COLORS = {
            'RED': (165, 42, 42),  # Brown Red
            'BLUE': (112, 128, 144),  # Slate Blue
            'GREEN': (107, 142, 35),  # Olive Green
            'ORANGE': (210, 105, 30),  # Chocolate
            'YELLOW': (218, 165, 32),  # Goldenrod
            'PURPLE': (128, 0, 128),  # Deep Purple
            'BLACK': (67, 67, 67),  # Charcoal Black
            'WHITE': (245, 245, 220),  # Beige
            'GREY': (169, 169, 169)  # Grey
        }
    elif color_theme == 15:  # "winter chill"
        COLORS = {
            'RED': (178, 34, 34),  # Firebrick
            'BLUE': (70, 130, 180),  # Light Steel Blue
            'GREEN': (85, 107, 47),  # Dark Olive Green
            'ORANGE': (210, 105, 30),  # Chocolate
            'YELLOW': (218, 165, 32),  # Goldenrod
            'PURPLE': (106, 90, 205),  # Slate Blue
            'BLACK': (25, 25, 25),  # Cold Black
            'WHITE': (255, 250, 250),  # Snow
            'GREY': (169, 169, 169)  # Winter Grey
        }
    elif color_theme == 16:  # "retro vibes"
        COLORS = {
            'RED': (255, 69, 0),  # Retro Red
            'BLUE': (100, 149, 237),  # Cornflower Blue
            'GREEN': (124, 252, 0),  # Lawn Green
            'ORANGE': (255, 165, 0),  # Orange Peel
            'YELLOW': (255, 215, 0),  # Gold
            'PURPLE': (186, 85, 211),  # Medium Orchid
            'BLACK': (25, 25, 25),  # Jet Black
            'WHITE': (255, 248, 220),  # Cornsilk
            'GREY': (169, 169, 169)  # Retro Grey
        }
    elif color_theme == 17:  # "lavender fields"
        COLORS = {
            'RED': (199, 21, 133),  # Medium Violet Red
            'BLUE': (123, 104, 238),  # Medium Slate Blue
            'GREEN': (152, 251, 152),  # Pale Green
            'ORANGE': (255, 160, 122),  # Light Salmon
            'YELLOW': (250, 250, 210),  # Light Goldenrod Yellow
            'PURPLE': (216, 191, 216),  # Thistle
            'BLACK': (47, 79, 79),  # Dark Slate Grey
            'WHITE': (255, 240, 245),  # Lavender Blush
            'GREY': (211, 211, 211)  # Light Slate Grey
        }
    elif color_theme == 18:  # "deep ocean"
        COLORS = {
            'RED': (220, 20, 60),  # Crimson Red
            'BLUE': (0, 0, 128),  # Navy Blue
            'GREEN': (46, 139, 87),  # Sea Green
            'ORANGE': (255, 127, 80),  # Coral
            'YELLOW': (249, 217, 78) ,  # Texas Yellow
            'PURPLE': (128, 0, 128),  # Purple
            'BLACK': (17, 12, 11),  # Coral Black
            'WHITE': (240, 255, 255),  # Azure
            'GREY': (112, 128, 144)  # Deep Slate Grey
        }
    elif color_theme == 19:  # "spring bloom"
        COLORS = {
            'RED': (255, 105, 180),  # Hot Pink
            'BLUE': (135, 206, 250),  # Light Sky Blue
            'GREEN': (144, 238, 144),  # Light Green
            'ORANGE': (255, 165, 0),  # Orange
            'YELLOW': (255, 255, 102),  # Light Yellow
            'PURPLE': (221, 160, 221),  # Plum
            'BLACK': (105, 105, 105),  # Dim Black
            'WHITE': (255, 245, 238),  # Seashell White
            'GREY': (192, 192, 192)  # Spring Grey
        }

    else:
        raise ValueError("Invalid color theme. Something went wrong.")


theme_counter = 0
print("\nAvailable color themes:")
for theme in COLOR_THEMES:
    theme_counter += 1
    print(f"{theme_counter}. {theme}")
while True:
    color_theme = int(input("Enter the color theme: ")) - 1
    if 0 <= color_theme <= len(COLOR_THEMES):
        break
choose_color_theme()

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH + SIDE_PANEL_WIDTH, HEIGHT))
pygame.display.set_caption("Color Conquest Simulation")

# Initialize the grid
grid = np.full((GRID_WIDTH, GRID_HEIGHT), 'GREY', dtype='<U10')

def initialize_grid():
    global play_colors, total_colors
    # play_colors = random.sample(list(COLORS.keys())[:-1], total_colors)
    for i in range(total_colors):
        play_colors.append(list(COLORS.keys())[i])
        
    # Set some initial values in the grid
    for x in range(1, GRID_WIDTH - 1):
        for y in range(1, GRID_HEIGHT - 1):
            if random.random() < 0.01:  # Chance of setting a cell to a color
                grid[x, y] = random.choice(play_colors)

def get_neighbors(x, y):
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < GRID_WIDTH - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < GRID_HEIGHT - 1:
        neighbors.append((x, y + 1))
    return neighbors

def update_grid(grids):
    global total_colors
    for x in range(1, GRID_WIDTH - 1):
        for y in range(1, GRID_HEIGHT - 1):
            if grids[x, y] == 'GREY':
                continue
            
            neighbors = get_neighbors(x, y)
            random.shuffle(neighbors)
            for nx, ny in neighbors:
                if grids[nx, ny] == 'GREY':
                    # Spreading mechanic
                    attacker_patch_size = len([n for n in neighbors if grids[n[0], n[1]] == grids[x, y]])
                    chance = 0.01 + 0.005 * len([n for n in get_neighbors(nx, ny) if grids[n[0], n[1]] == grids[x, y]]) + 0.01 * (attacker_patch_size / 100)
                    if random.random() < chance:
                        grids[nx, ny] = grids[x, y]
                elif total_colors > 1:
                    if grids[nx, ny] != grids[x, y]:
                        
                        # Attack mechanic
                        attacker_patch_size = len([n for n in neighbors if grids[n[0], n[1]] == grids[x, y]])
                        defender_patch_size = len([n for n in get_neighbors(nx, ny) if grids[n[0], n[1]] == grids[nx, ny]])
                        attack_chance = 2 * (0.005 + 0.001 * (SECONDS / 1000) + 0.005 * (attacker_patch_size / (defender_patch_size + 1)))
                        if random.random() < attack_chance:
                            grids[nx, ny] = grids[x, y]
                            
                        # Losing hard mechanic
                        lose_hard_chance = 0.01 * (defender_patch_size / (attacker_patch_size + 1))
                        if random.random() < lose_hard_chance:
                            grids[x, y] = grids[nx, ny]
                            
                        # Bomb mechanic
                        if SECONDS > 20:
                            if grids[x, y] != grids[nx, ny]:
                                bomb_chance = 2 * (0.000005 * (defender_patch_size / (attacker_patch_size + 1)))
                                if random.random() < bomb_chance:
                                    grids[x, y] = grids[nx, ny]
                                    for bx in range(max(0, nx - 5), min(GRID_WIDTH, nx + 6)):
                                        for by in range(max(0, ny - 5), min(GRID_HEIGHT, ny + 6)):
                                            grids[bx, by] = grids[x, y]
                                            
                        # Cross mechanic
                        if SECONDS > 30:
                            if play_colors.index(grids[x, y]) >= len(play_colors) - 3:
                                cross_chance = 2 * (0.000001 * (defender_patch_size / (play_colors.index(grids[x, y]) + 1)))
                                if random.random() < cross_chance:
                                    for i in range(max(0, x - 15), min(GRID_WIDTH, x + 16)):
                                        grids[i, y] = grids[x, y]
                                    for j in range(max(0, y - 15), min(GRID_HEIGHT, y + 16)):
                                        grids[x, j] = grids[x, y]

def draw_grid(screens, grids):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            color = COLORS[grids[x, y]]
            pygame.draw.rect(screens, color, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def leaderboard(grids):
    color_counts = {color: np.count_nonzero(grids == color) for color in play_colors}
    sorted_counts = sorted(color_counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts

def display_leaderboard(screens, leaderboards):
    global COLORS
    font = pygame.font.SysFont("Segoe UI", 24)
    y_offset = 20
    # Draw a black background
    pygame.draw.rect(screens, (0, 0, 0), (WIDTH, 0, 300, HEIGHT))
    for color, count in leaderboards:
        text = f"{color}: {count} squares"
        img = font.render(text, True, COLORS[color])
        screens.blit(img, (WIDTH + 10, y_offset))
        y_offset += 30

def plot_graph(time_series):
    plt.figure(figsize=(10, 6))
    COLORS['WHITE'] = (128, 128, 128)
    for color, series in time_series.items():
        x = np.array(range(len(series)))
        y = np.array(series)
        f = interp1d(x, y, kind='cubic')
        x_new = np.linspace(0, len(series) - 1, num=500, endpoint=True)
        y_new = f(x_new)
        color_value = np.array(COLORS[color]) / 255.0
        plt.plot(x_new, y_new, label=color, color=color_value)

    plt.xlabel('Time (seconds)')
    plt.ylabel('Owned Squares')
    plt.title('Evolution of Owned Squares Over Time')
    plt.legend()
    plt.savefig("7colorsim_graph.png", dpi=300) # type: ignore
    plt.show()
    
def main():
    global SECONDS
    initialize_grid()

    running = True
    clock = pygame.time.Clock()
    time_series = {color: [] for color in play_colors}
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Fill the screen with white color

        update_grid(grid)
        draw_grid(screen, grid)

        # Update and display leaderboard
        current_leaderboard = leaderboard(grid)
        if current_leaderboard[0][1] == 31996:
            running = False
            continue
        display_leaderboard(screen, current_leaderboard)
        # Update time series for graph
        for color, count in current_leaderboard:
            time_series[color].append(count)
        
        # Add a Second after every real time seconds
        if time.time() - start_time >= 1:
            start_time = time.time()
            SECONDS += 1
            
        pygame.display.flip()  # Update the display
        clock.tick(30)

    plot_graph(time_series)
    pygame.quit()

if __name__ == "__main__":
    main()
