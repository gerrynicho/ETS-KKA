#!/usr/bin/env python3
import pygame

running = bool(False)
screen = pygame.display.set_mode((2000, 1080))

def game_init():
    pygame.init()
    pygame.display.set_caption('Game')

def generate_maze():
    global screen
    for i in range(0, 2000, 20):
        pygame.draw.line(screen, "black", (i, 0), (i, 1080))
    for i in range(0, 1080, 20):
        pygame.draw.line(screen, "black", (0, i), (2000, i))

def run_game():
    global running, screen
    generate_maze()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
        screen.fill("white")

        pygame.display.flip()


if __name__ == '__main__':
    game_init()
    running = True
    run_game()
    pygame.quit()