import pygame
import random, math
from pygame import mixer

pygame.init()


screen = pygame.display.set_mode((800, 600))
running = True

pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load('pictures/ufo.png'))

bgImg = pygame.image.load('pictures/bg.png')
# bgImg = pygame.transform.scale(bgImg, (600,800))
# bgImg = pygame.transform.rotate(bgImg, (270))

mixer.music.load('background.wav')
mixer.music.play(-1)

bulletImg = pygame.image.load('pictures/bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (32,32))
bulletImg = pygame.transform.rotate(bulletImg, (45))
bulletX = 0
bulletY = 480
bulletY_change = 15
bullet_state = 'ready'

playerImg = pygame.image.load('pictures/space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_speed = 1.1
num_of_enemies = 3



score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score ,(x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player():
    screen.blit(playerImg,(playerX, playerY))

def enemy(enemyX, enemyY, i):
    screen.blit(enemyImg[i],(enemyX, enemyY))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 9, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY, distance_between):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < distance_between:
        return True
    else: 
        return False

while running:

    screen.fill((0, 0, 0))
    screen.blit(bgImg, (0, 0))

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('pictures/skull.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(-enemy_speed)
        enemyY_change.append(70)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # X Move - Left Right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:     
                playerX_change = 5
            if event.key == pygame.K_SPACE:   
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        collision = isCollision(enemyX[i], enemyY[i], playerX, playerY, 30)
        if collision:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY, 27)
        if collision:
            hit_sound = mixer.Sound('explosion.wav')
            hit_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 100
            enemy_speed += 0.1
            num_of_enemies += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i],enemyY[i], i)
        
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change        


    player()
    show_score(textX, textY)
    pygame.display.update()