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

ORIGINAL_WIDTH, ORIGINAL_HEIGHT = 1200, 800
ROWS, COLS = new_img.shape[0], new_img.shape[1]
CELL_SIZE = (ORIGINAL_WIDTH // COLS)
PLAYER_SIZE = 5

WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
DARK_GRAY    = (50, 50, 50)
BLUE    = (0, 0, 255)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
PURPLE  = (128, 0, 128)

PRESTART = "waiting"
PLAYING = "playing"
FINISHED = "finished"

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

pygame.init()
screen = pygame.display.set_mode((ORIGINAL_WIDTH, ORIGINAL_HEIGHT))
pygame.display.set_caption("Final Proyek KKA 2024")
clock = pygame.time.Clock()

map = new_img.astype(int)
player_path = []
shortest_path = []

MOVEMENT_COOLDOWN = 50
last_move_time = 0
game_state = PRESTART

ZOOM_FACTOR = 2
zoom_width = ORIGINAL_WIDTH // ZOOM_FACTOR
zoom_height = ORIGINAL_HEIGHT // ZOOM_FACTOR

player_x, player_y = None, None

def draw_map(surface, offset_x, offset_y, zoom=False):
    zoom_cell_size = CELL_SIZE * ZOOM_FACTOR if zoom else CELL_SIZE
    if zoom:
        zoom_rows = ROWS // ZOOM_FACTOR
        zoom_cols = COLS // ZOOM_FACTOR
        
        for y in range(zoom_rows):
            for x in range(zoom_cols):
                color = WHITE if map[y + offset_y][x + offset_x] == 0 else BLACK
                pygame.draw.rect(surface, color, 
                    ((x * zoom_cell_size), (y * zoom_cell_size), 
                     zoom_cell_size + 10, zoom_cell_size + 10))
    else:
        for y in range(ROWS):
            for x in range(COLS):
                color = WHITE if map[y][x] == 0 else BLACK
                pygame.draw.rect(surface, color, 
                    (x * zoom_cell_size, y * zoom_cell_size, 
                     zoom_cell_size + 10, zoom_cell_size + 10))
    
    for pos in player_path:
        if zoom:
            if (offset_x <= pos[0] < offset_x + (COLS // ZOOM_FACTOR) and 
                offset_y <= pos[1] < offset_y + (ROWS // ZOOM_FACTOR)):
                pygame.draw.rect(surface, RED, 
                    ((pos[0] - offset_x) * zoom_cell_size, 
                     (pos[1] - offset_y) * zoom_cell_size, 
                     zoom_cell_size + 2, zoom_cell_size + 2))
        else:
            pygame.draw.rect(surface, RED, 
                (pos[0] * zoom_cell_size, pos[1] * zoom_cell_size, 
                 zoom_cell_size + 2, zoom_cell_size + 2))

def draw_player(surface, offset_x, offset_y, zoom=False):
    global player_x, player_y
    if player_x is None or player_y is None:
        return

    zoom_cell_size = CELL_SIZE * ZOOM_FACTOR if zoom else CELL_SIZE

    if zoom:
        pygame.draw.rect(surface, GREEN, pygame.Rect(
            (player_x - offset_x) * zoom_cell_size, 
            (player_y - offset_y) * zoom_cell_size, 
            zoom_cell_size + PLAYER_SIZE, zoom_cell_size + PLAYER_SIZE))
    else:
        pygame.draw.rect(surface, GREEN, pygame.Rect(
            player_x * zoom_cell_size, 
            player_y * zoom_cell_size, 
            zoom_cell_size + PLAYER_SIZE, zoom_cell_size + PLAYER_SIZE))

def draw_game_over_message():
    font = pygame.font.Font(None, 60)
    text = font.render('Jarak Optimal menggunakan A*', True, GREEN, DARK_GRAY)
    text_rect = text.get_rect(center=(ORIGINAL_WIDTH/2, ORIGINAL_HEIGHT/2))
    screen.blit(text, text_rect)

def draw_shortest_path(surface, zoom=False):
    zoom_cell_size = CELL_SIZE * ZOOM_FACTOR if zoom else CELL_SIZE

    for i in range(len(shortest_path)) :
        if i == 0 or i == len(shortest_path) - 1 : 
            pygame.draw.rect(surface, BLUE, 
                (shortest_path[i][0] * zoom_cell_size, shortest_path[i][1] * zoom_cell_size, 
                 zoom_cell_size + 5, zoom_cell_size + 5))
        else : 
            pygame.draw.rect(surface, PURPLE, 
                (shortest_path[i][0] * zoom_cell_size, shortest_path[i][1] * zoom_cell_size, 
                 zoom_cell_size + 5, zoom_cell_size + 5))

def calculate_zoom_offset():
    zoom_x = max(0, min(player_x - (COLS // (ZOOM_FACTOR * 2)), 
                        COLS - (COLS // ZOOM_FACTOR)))
    zoom_y = max(0, min(player_y - (ROWS // (ZOOM_FACTOR * 2)), 
                        ROWS - (ROWS // ZOOM_FACTOR)))
    return int(zoom_x), int(zoom_y)

def handle_player_movement(keys):
    global player_x, player_y, last_move_time, game_state
    
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

    if moved and 0 <= new_x < COLS and 0 <= new_y < ROWS and map[new_y][new_x] == 0:
        player_x, player_y = new_x, new_y
        last_move_time = current_time
        if (player_x, player_y) not in player_path:
            player_path.append((player_x, player_y))

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

def main():
    global game_state, screen, ZOOM_FACTOR, player_x, player_y
    running = True
    show_shortest_path = False
    zoomed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == PRESTART and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                map_x = mouse_x // CELL_SIZE
                map_y = mouse_y // CELL_SIZE
                
                if 0 <= map_x < COLS and 0 <= map_y < ROWS and map[map_y][map_x] == 0:
                    player_x, player_y = map_x, map_y
                    player_path.append((player_x, player_y))
                    game_state = PLAYING

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game_state == PLAYING:
                    find_shortest_path()
                    show_shortest_path = True
                    game_state = FINISHED
                elif event.key == pygame.K_z:
                    zoomed = not zoomed

        keys = pygame.key.get_pressed()
        
        if game_state == PLAYING:
            handle_player_movement(keys)

        screen.fill(BLACK)

        if game_state == PRESTART:
            draw_map(screen, 0, 0)
        elif game_state == PLAYING:
            zoom_x, zoom_y = calculate_zoom_offset() if zoomed else (0, 0)
            draw_map(screen, zoom_x, zoom_y, zoom=zoomed)
            draw_player(screen, zoom_x, zoom_y, zoom=zoomed)
            
            if show_shortest_path:
                draw_shortest_path(screen, zoom=zoomed)
        else:
            draw_map(screen, 0, 0, zoom=False)
            draw_player(screen, 0, 0, zoom=False)
            
            if show_shortest_path:
                draw_shortest_path(screen, zoom=False)
            
            draw_game_over_message()
            
        pygame.display.flip()
        clock.tick(165)

    pygame.quit()


if __name__ == "__main__":
    main()