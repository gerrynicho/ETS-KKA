#!/usr/bin/env python3
import pygame
import random

# Screen settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Directions for maze generation (Up, Right, Down, Left)
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game with Player Movement")
clock = pygame.time.Clock()

# Maze grid initialization
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]

# Player's starting position
player_x, player_y = 0, 0

def generate_maze():
    global maze, player_x, player_y
    stack = [(random.randint(0, ROWS - 1), random.randint(0, COLS - 1))]
    while stack:
        x, y = stack[-1]
        maze[y][x] = 0
        neighbors = []
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
                neighbors.append((nx, ny, dx, dy))
        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze[y + dy][x + dx] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    while maze[player_y][player_x] != 0:
        player_x, player_y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player():
    global player_x, player_y

    pygame.draw.rect(screen, BLUE, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def handle_player_movement(keys):
    global player_x, player_y
    new_x, new_y = player_x, player_y
    if keys[pygame.K_UP]:      # Move up
        new_y -= 1
    if keys[pygame.K_DOWN]:    # Move down
        new_y += 1
    if keys[pygame.K_LEFT]:    # Move left
        new_x -= 1
    if keys[pygame.K_RIGHT]:   # Move right
        new_x += 1

    # Check if new position is within bounds and is a path
    if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
        player_x, player_y = new_x, new_y

def main():
    generate_maze()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        handle_player_movement(keys)

        screen.fill(BLACK)
        draw_maze()
        draw_player()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
