import pygame
import math
import random
from pygame import mixer


# Instance of pygame
pygame.init()


# Game Screen
screen = pygame.display.set_mode((800, 600))


# Image Loaders
background = pygame.image.load('img/background.png')
player_image = pygame.image.load('img/player_image.png')
enemy_image = pygame.image.load('img/invader.png')
icon = pygame.image.load('img/title_icon.png')
bullet_image = pygame.image.load('img/bullet.png')

# Background sound
mixer.music.load('sounds/Teminite_&_MDK_Space_Invaders.mp3')
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption('Doony Invaders')
pygame.display.set_icon(icon)

# Score
score = 0

# Player initial position and movement values
player_x = 368
player_y = 480
player_x_change = 0
player_y_change = 0
player_x_speed = 5
player_y_speed = 2

def player(x, y):
    screen.blit(player_image, (x, y))

# Buller initial position
bullet_x = player_x
bullet_y = player_y
bullet_x_change = player_x_change
bullet_y_change = 2
bullet_state = 'ready'

def fire_bullet(x, y):
    screen.blit(bullet_image, (x+16, y+10))

# Enemys initial position and movement values
num_enemy = 6
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_speed = []
for i in range(num_enemy):
    enemy_img.append(enemy_image)
    enemy_x.append(random.randint(50, 700))
    enemy_y.append(random.randint(50, 120))
    enemy_x_change.append(1)
    enemy_y_change.append(30)
    enemy_speed.append(1.09)

def enemy(enemyimg, x, y):
    screen.blit(enemyimg, (x, y))


# Collision
def collision(bullet_x, bullet_y, enemy_x, enemy_y):
    distance = math.sqrt(math.pow(bullet_x-enemy_x, 2)+math.pow(bullet_y-enemy_y, 2))
    if distance < 30:
        return True
    else:
        return False

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

def show_score(score, x, y):
    score = font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Over
over = pygame.font.Font('freesansbold.ttf', 64)
text_x = 10
text_y = 10

def game_over_text():
    game_over = over.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


# Game Loop
if __name__ == "__main__":
        
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
                # # if event.key == pygame.K_UP:
                # #     player_y_change = -player_y_speed
                # # elif event.key == pygame.K_DOWN:
                #     player_y_change =  player_y_speed
                if event.key == pygame.K_SPACE:
                    bullet_state = 'fire'

            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) and  keys[pygame.K_RIGHT]:
                    player_x_change =  player_x_speed
                elif (event.key == pygame.K_RIGHT) and  keys[pygame.K_LEFT]:
                    player_x_change = -player_x_speed
                elif (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                    player_x_change = 0
                # if (event.key == pygame.K_UP) and  keys[pygame.K_DOWN]:
                #     player_y_change =  player_y_speed
                # elif (event.key == pygame.K_DOWN) and  keys[pygame.K_UP]:
                #     player_y_change = -player_y_speed
                # elif (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                #     player_y_change = 0

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

        # Enemy movement and scaling difficulty
        for i in range(num_enemy):

            # Game Over
            if enemy_y[i] > 420: 
                for j in range(num_enemy):
                    enemy_y[j] = 2000
                game_over_text()
                break

            if enemy_x_change[i] >= 3:
                enemy_speed[i] = 1.06
            if enemy_x_change[i] >= 4.5:
                enemy_speed[i] = 1.03
            if enemy_x_change[i] >= 6:
                enemy_speed[i] = 1.01
            if enemy_x[i] <= 0:
                enemy_x_change[i] =  abs(enemy_x_change[i])*enemy_speed[i]
                enemy_y[i] += enemy_y_change[i]
            if enemy_x[i] >= 736:
                enemy_x_change[i] = -abs(enemy_x_change[i])*enemy_speed[i]
                enemy_y[i] += enemy_y_change[i]

            enemy_x[i] += enemy_x_change[i]
        
            # Collision
            if collision(bullet_x, bullet_y, enemy_x[i], enemy_y[i]):
                explosions = mixer.Sound('sounds/Explosion.wav')
                explosions.set_volume(0.5)
                explosions.play()
                bullet_state = 'ready'
                score += 1
                enemy_x[i] = random.randint(0, 736)
                enemy_y[i] = random.randint(50, 120)

            enemy(enemy_img[i] ,enemy_x[i], enemy_y[i])
            

            # Bullet
            if bullet_state == 'ready':
                bullet_x = player_x
                bullet_y = player_y
            if bullet_state == 'fire':
                fire_bullet(bullet_x, bullet_y)
                bullet_y -= bullet_y_change
            if bullet_y <= -32:
                bullet_state = 'ready'



    # Drawing the player and the enemy
        player(player_x, player_y)
        show_score(score, text_x, text_y)
        pygame.display.update()
