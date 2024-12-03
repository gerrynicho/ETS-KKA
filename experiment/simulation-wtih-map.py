#!/usr/bin/env python3
import pygame
import heapq
import cv2
import numpy as np

image_path = './sarinah.png'
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
equalized = cv2.equalizeHist(img)
_, binary = cv2.threshold(equalized, 200, 255, cv2.THRESH_BINARY)

new_img = cv2.bitwise_not(binary) / 255.0

WIDTH, HEIGHT = 1200, 800
ROWS, COLS = new_img.shape[0], new_img.shape[1]
CELL_SIZE = (WIDTH // COLS)

WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
BLUE    = (0, 0, 255)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
PURPLE  = (128, 0, 128)

PLAYING = "playing"
FINISHED = "finished"

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game with Player Movement")
clock = pygame.time.Clock()

maze = new_img.astype(int)
player_x, player_y = 210, 250
player_path = []
shortest_path = []

MOVEMENT_COOLDOWN = 150
last_move_time = 0
game_state = PLAYING

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE + 10, CELL_SIZE + 10))
    for pos in player_path:
        pygame.draw.rect(screen, RED, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE + 5, CELL_SIZE + 5))

def draw_player():
    pygame.draw.rect(screen, GREEN, pygame.Rect(player_x * (CELL_SIZE), player_y * (CELL_SIZE), CELL_SIZE + 5, CELL_SIZE + 5))

def handle_player_movement(keys):
    global player_x, player_y, last_move_time
    
    if game_state == FINISHED:
        return

    current_time = pygame.time.get_ticks()
    
    if current_time - last_move_time < MOVEMENT_COOLDOWN:
        return

    new_x, new_y = player_x, player_y
    moved = False

    if keys[pygame.K_UP]:
        new_y -= 1
        moved = True
    elif keys[pygame.K_DOWN]:
        new_y += 1
        moved = True
    elif keys[pygame.K_LEFT]:
        new_x -= 1
        moved = True
    elif keys[pygame.K_RIGHT]:
        new_x += 1
        moved = True

    if moved and 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
        player_x, player_y = new_x, new_y
        last_move_time = current_time
        if (player_x, player_y) not in player_path:
            player_path.append((player_x, player_y))

def draw_game_over_message():
    font = pygame.font.Font(None, 74)
    text = font.render('Finish, You Can Close the App', True, GREEN)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)

def find_shortest_path():
    global shortest_path
    if len(player_path) < 2:
        return

    start, end = player_path[0], player_path[-1]
    queue = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while queue:
        _, current = heapq.heappop(queue)

        if current == end:
            break

        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if neighbor in player_path and (neighbor not in cost_so_far or cost_so_far[current] + 1 < cost_so_far[neighbor]):
                cost_so_far[neighbor] = cost_so_far[current] + 1
                priority = cost_so_far[neighbor]
                heapq.heappush(queue, (priority, neighbor))
                came_from[neighbor] = current

    shortest_path = []
    current = end
    while current != start:
        shortest_path.append(current)
        current = came_from.get(current)
        if current is None:
            return
    shortest_path.append(start)
    shortest_path.reverse()

def draw_shortest_path():
    for pos in shortest_path:
        pygame.draw.rect(screen, PURPLE, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE + 5, CELL_SIZE + 5))

def main():
    global game_state
    running = True
    show_shortest_path = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game_state == PLAYING:
                    find_shortest_path()
                    show_shortest_path = True
                    game_state = FINISHED

        keys = pygame.key.get_pressed()
        handle_player_movement(keys)

        screen.fill(BLACK)
        draw_maze()
        if show_shortest_path:
            draw_shortest_path()
        draw_player()
        
        print(f"player: ({player_x}, {player_y})")

        if game_state == FINISHED:
            draw_game_over_message()
            
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()