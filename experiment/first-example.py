#!/usr/bin/env python3
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if (player_pos.y - 40) > 0:
            player_pos.y -= 700 * dt
    if keys[pygame.K_s]:
        if (player_pos.y + 40) < screen.get_height():
            player_pos.y += 700 * dt
    if keys[pygame.K_a]:
        if (player_pos.x - 40) > 0:
            player_pos.x -= 700 * dt
    if keys[pygame.K_d]:
        if (player_pos.x + 40) < screen.get_width():
            player_pos.x += 700 * dt

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()