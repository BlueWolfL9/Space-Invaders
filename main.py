import math
import random

import pygame
from pygame import mixer
pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')
background_2 = pygame.image.load('space-galaxy-background.jpg')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

bulletImg = pygame.image.load('bullet.png')
bulletX_1 = 0
bulletY_1 = 480
bulletX_2 = 0
bulletY_2 = 480
bulletX_change = 0
bulletY_change = 5
bullet_state_1 = "ready"
bullet_state_2 = "ready"
bulletX = 0
bulletY = 480
bullet_state = "ready"

# Score

score_value = 0
level_value = 1
font = pygame.font.Font('freesansbold.ttf', 32)
levelX = 650
levelY = 10
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
win_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_level(x, y):
    level = font.render("Level : " + str(level_value), True, (255, 255, 255))
    screen.blit(level, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def win_text():
    over_text = over_font.render("You Win", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y + 10))


def fire_bullet_1(x, y):
    global bullet_state_1
    bullet_state_1 = "fire"
    screen.blit(bulletImg, (x - 20, y + 10))


def fire_bullet_2(x, y):
    global bullet_state_2
    bullet_state_2 = "fire"
    screen.blit(bulletImg, (x + 25, y + 10))


def isCollision_1(enemyX, enemyY, bulletX_1, bulletY_1):
    distance_1 = math.sqrt(math.pow(enemyX - bulletX_1, 2) + (math.pow(enemyY - bulletY_1, 2)))
    if distance_1 < 27:
        return True
    else:
        return False


def isCollision_2(enemyX, enemyY, bulletX_2, bulletY_2):
    distance_2 = math.sqrt(math.pow(enemyX - bulletX_2, 2) + (math.pow(enemyY - bulletY_2, 2)))
    if distance_2 < 27:
        return True
    else:
        return False


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    #Level 2 background
    if score_value > 2:
        screen.blit(background_2, (0, 0))
    if score_value == 2:
        level_value = 2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                    #check if the level is 1 or 2
                    if score_value > 2:
                        playerImg = pygame.image.load('spaceship.png')
                        if bullet_state_1 is "ready" and bullet_state_2 is "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            # Get the current x cordinate of the spaceship
                            bulletX_1 = playerX - 10
                            fire_bullet_1(bulletX_1, bulletY_1)
                            bulletX_2 = playerX + 10
                            fire_bullet_2(bulletX_2, bulletY_2)

                    else:
                            # if key is pressed check if its right or left
                            if bullet_state is "ready":
                                bulletSound = mixer.Sound("laser.wav")
                                bulletSound.play()
                                # Get the current x cordinate of the spaceship
                                bulletX = playerX
                                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

        # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        #Win
        if score_value >= 10:
            win_text()
            break
        #Lose
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        #the enemy hits the edge of the screen
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collisions
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        collision_1 = isCollision_1(enemyX[i], enemyY[i], bulletX_1, bulletY_1)
        collision_2 = isCollision_2(enemyX[i], enemyY[i], bulletX_2, bulletY_2)
        if collision_1:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY_1 = 480
            bullet_state_1 = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        if collision_2:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY_2 = 480
            bullet_state_2 = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bulletY_1 <= 0:
        bulletY_1 = 480
        bullet_state_1 = "ready"
    if bulletY_2 <= 0:
        bulletY_2 = 480
        bullet_state_2 = "ready"

    if bullet_state_1 is "fire":
        fire_bullet_1(bulletX_1, bulletY_2)
        bulletY_1 -= bulletY_change

    if bullet_state_2 is "fire":
        fire_bullet_2(bulletX_2, bulletY_2)
        bulletY_2 -= bulletY_change

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    show_level(levelX, levelY)
    pygame.display.update()
