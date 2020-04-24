import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("space_background.png")

# background sound
mixer.music.load("background_music_cropped.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("universe.png")
pygame.display.set_icon(icon)

# Player image and axis placement
playerimg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerimg, (x, y))

# multiple enemy # Enemy image and axis placement
Enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemy = 6

for i in range(num_enemy):
    Enemyimg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# bullet image and axis placement
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
# ready state :  cant see the bullet
# fire state :  the bullet is moving
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
game_over = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score :  " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def enemy(x, y, i):
    screen.blit(Enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))  
    if distance < 27:
        return True
    else:
        return False

# game screenloop 
running = True
while running:
    # RGB values for screen     
    screen.fill((0, 0, 0))
    # screen background upload
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        # if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            print("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                # print("Left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                # print("Right arrow is pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('shot.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                # print("Right arrow is pressed")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking screen boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    # enemy movement
    for i in range(num_enemy):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_enemy):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i] 
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i] 
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)
          
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY) 
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
