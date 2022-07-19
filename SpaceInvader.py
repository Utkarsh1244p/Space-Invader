import pygame
import math
import random

#Initialisation of Pygame 
pygame.init()

#Create The Screen
screen = pygame.display.set_mode((800,600))

#Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('img/ufo.png')
pygame.display.set_icon(icon)

#Player Initialisation
playerImg = pygame.image.load('img/player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#Eenmy initialisation
enemyImg = [pygame.image.load('img/enemy2.png'),pygame.image.load('img/enemy3.png'),pygame.image.load('img/enemy4.png')]
enemyX = []
enemyY = []
enemyX_change = [0.5,0.4,1]
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('img/enemy1.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


#Bullet initialisation
'''
Ready State: Bullet is ready to fight, you can't see it on the screen
Fire State: Bullet is in space, currently moving
'''
bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

#Function to check whether collision occure or not
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Score Initialisation
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#Game Over Tedt
over_font = pygame.font.Font('freesansbold.ttf',200)

def game_over_text():
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text ,(300, 250))

def show_score(x,y):
    score = font.render("Score : "+ str(score_value), True, (255,255,255))
    screen.blit(score ,(x, y))

def player(x,y):
    screen.blit(playerImg ,(x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg ,(x+16, y+10))

#Game Loop
running = True
while running:
    #To change Screen Color
    screen.fill((0,0,0))  #Values in (R,G,B)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed whether it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change -= 0.3
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change += 0.3
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                playerY_change -= 0.3
            if event.key == pygame.K_DOWN or event.key == pygame.K_x:
                playerY_change += 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    #Get Current X coordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)



        if event.type == pygame.KEYUP:
            # if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 0
            # if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_x:
                playerY_change = 0

    
    #To move player from Left-Right
    playerX += playerX_change
    #To move player from Up-Down
    playerY += playerY_change
     
    #To make Restrictions on Left-Right Movements for player
    if playerX <= 0:
        playerX = 0
    if playerX >=736:
        playerX = 736

    #To make Restrictions on Up-Down Movements for pkayer
    if playerY <= 0:
        playerY = 0
    if playerY >=536:
        playerY = 536

    for i in range(num_of_enemies):

        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            show_score(330,290)
            break 

        #To move enemy from Left-Right
        enemyX[i] += enemyX_change[i]

        #To make Restrictions on Left-Right Movements for enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        #For Checking Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bullet_state = "ready"
            bulletY = 480
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 200)
            score_value += 1

        enemy(enemyX[i], enemyY[i], i)

    #Bullet Movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    enemy(enemyX[i], enemyY[i], i)
    show_score(textX,textY)

    #To Update our screen
    pygame.display.update()

