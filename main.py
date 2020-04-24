import pygame
import random


# Instance of pygame
pygame.init()


# Game Screen
screen = pygame.display.set_mode((800, 600))


# Image Loaders
background = pygame.image.load('img/background.png')
player_image = pygame.image.load('img/player_image.png')
enemy1_image = pygame.image.load('img/invader.png')
icon = pygame.image.load('img/title_icon.png')
bullet_image = pygame.image.load('img/bullet.png')


# Title and Icon
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(icon)


# Player initial position and movement values
player_x = 368
player_y = 480
player_x_change = 0
player_y_change = 0
player_x_speed = 2
player_y_speed = 2

def player(x, y):
    screen.blit(player_image, (x, y))

# Buller initial position
bullet_y = player_y
bullet_x_change = player_x_change
bullet_y_change = 6
bullet_state = 'ready'

def fire_bullet(x, y):
    screen.blit(bullet_image, (x+16, y+10))

# Enemy initial position and movement values
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 120)
enemy_x_change = 1
enemy_y_change = 30

def enemy1(x, y):
    screen.blit(enemy1_image, (x, y))


# Game Loop
running = True
while running:

# Background image
    screen.blit(background, (0, 0))

# Events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():

        # Closing the Game
        if event.type == pygame.QUIT:
            running = False

        # Player controls and movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_x_speed
            elif event.key == pygame.K_RIGHT:
                player_x_change =  player_x_speed
            if event.key == pygame.K_UP:
                player_y_change = -player_y_speed
            elif event.key == pygame.K_DOWN:
                player_y_change =  player_y_speed
            if event.key == pygame.K_SPACE:
                bullet_state = 'fire'

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT) and  keys[pygame.K_RIGHT]:
                player_x_change =  player_x_speed
            elif (event.key == pygame.K_RIGHT) and  keys[pygame.K_LEFT]:
                player_x_change = -player_x_speed
            elif (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                player_x_change = 0
            if (event.key == pygame.K_UP) and  keys[pygame.K_DOWN]:
                player_y_change =  player_y_speed
            elif (event.key == pygame.K_DOWN) and  keys[pygame.K_UP]:
                player_y_change = -player_y_speed
            elif (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                player_y_change = 0

# Movement and boundaries

    # Player
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    player_y += player_y_change
    if player_y <= 0:
        player_y = 0
    elif player_y >= 536:
        player_y = 536

    # Bullet
    if bullet_state == 'ready':
        bullet_x = player_x
        bullet_y = player_y
    if bullet_state == 'fire':
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    if bullet_y <= -32:
        bullet_state = 'ready'

    # Enemy
    if enemy_x <= 0:
        enemy_x_change =  abs(enemy_x_change)*1.1
        enemy_y += enemy_y_change
    if enemy_x >= 736:
        enemy_x_change = -abs(enemy_x_change)*1.1
        enemy_y += enemy_y_change
    enemy_x += enemy_x_change

# Drawing the player and the enemy
    player(player_x, player_y)
    enemy1(enemy_x, enemy_y)
    pygame.display.update()