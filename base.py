# Import libraries
import pygame
import random
import time
import sys
pygame.init()

# Default values
m = 20  # unit pixel
speed = 100

red = pygame.Color(255,  0,  0)
orange = pygame.Color(255, 165, 0)
blue = pygame.Color(65,  105,  255)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

# Main window
mapsize = 500
gameSurface = pygame.display.set_mode((mapsize+20, mapsize+60))
pygame.display.set_caption('Snake Game')

# Varibles
# about snake
snakepos = [100, 60]
snakebody = [[100, 60], [80, 60], [60, 60]]

# about food
Xfood = random.randrange(2, mapsize/10 - 2)
Yfood = random.randrange(6, mapsize/10 - 2)
if (Xfood % 2 != 0):
    Xfood += 1
if (Yfood % 2 != 0):
    Yfood += 1
foodpos = [Xfood * 10,  Yfood * 10]
foodexist = True

# about gameplay
direction = 'RIGHT'
changeto = direction
score = 0

# Imgbody = pygame.transform.scale(pygame.image.load('1.png'), (m, m))
# Imghead = pygame.transform.scale(pygame.image.load('Head.png'), (m, m))

# Function when game is over


def GameOver():
    gfont = pygame.font.SysFont('bahnshcriff',  80, False, True)
    gsurf = gfont.render('Game Over!',  True, orange)
    grect = gsurf.get_rect()
    grect.midtop = (mapsize/2, mapsize/2-20)
    gameSurface.blit(gsurf, grect)
    showScore(0)
    pygame.display.flip()
    time.sleep(3)  # time wait to exit
    pygame.quit()
    sys.exit()

# Function to show score


def showScore(choice=1):
    sfont = pygame.font.SysFont('bahnschriff', 30)
    ssurf = sfont.render('Score: {0}'.format(score),  True,  white)
    srect = ssurf.get_rect()
    if (choice == 1):
        srect.midtop = (70, 15)     # normal
    else:
        srect.midtop = (mapsize/2, mapsize/2 + 50)   # game over
    gameSurface.blit(ssurf, srect)

# Show on screen


def showScreen():
    gameSurface.fill(black)
    for pos in snakebody:
        pygame.draw.rect(gameSurface, red, pygame.Rect(
            pos[0], pos[1], m-1, m-1))
    pygame.draw.rect(gameSurface, orange, pygame.Rect(
        snakebody[0][0], snakebody[0][1], m-1, m-1))  # snake's head
    pygame.draw.rect(gameSurface, blue, pygame.Rect(
        foodpos[0], foodpos[1], m, m))

# Random food position


def randomFood():
    while True:
        check = True
        Xfood = random.randrange(2, mapsize/10 - 2)
        Yfood = random.randrange(6, mapsize/10 - 2)
        if (Xfood % 2 != 0):
            Xfood += 1
        if (Yfood % 2 != 0):
            Yfood += 1

        for cursnake in snakebody:
            if (Xfood == cursnake[0] and Yfood == cursnake[1]):
                GameOver()

        if (check == True):
            return Xfood, Yfood

    # Main program


# Main Game
while True:
    pygame.time.delay(speed)  # speed
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()

        # key input
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_RIGHT):
                changeto = 'RIGHT'
            if (event.key == pygame.K_LEFT):
                changeto = 'LEFT'
            if (event.key == pygame.K_UP):
                changeto = 'UP'
            if (event.key == pygame.K_DOWN):
                changeto = 'DOWN'
            if (event.key == pygame.K_ESCAPE):
                pygame.event.post(pygame.evet.Event(pygame.QUIT))

    # directions
    if (changeto == 'RIGHT' and not direction == 'LEFT'):
        direction = 'RIGHT'
    if (changeto == 'LEFT' and not direction == 'RIGHT'):
        direction = 'LEFT'
    if (changeto == 'UP' and not direction == 'DOWN'):
        direction = 'UP'
    if (changeto == 'DOWN' and not direction == 'UP'):
        direction = 'DOWN'

    # update directions
    if (direction == 'RIGHT'):
        snakepos[0] += m
    if (direction == 'LEFT'):
        snakepos[0] -= m
    if (direction == 'UP'):
        snakepos[1] -= m
    if (direction == 'DOWN'):
        snakepos[1] += m

    # snake grows up
    snakebody.insert(0, list(snakepos))
    if (snakepos[0] == foodpos[0] and snakepos[1] == foodpos[1]):
        score += 1
        foodexist = False
        if ((score % 2 == 0 and score > 0 and speed > 50)):
            speed -= 5
    else:
        snakebody.pop()

    showScreen()

    # food shows up
    if (foodexist == False):
        Xfood, Yfood = randomFood()
        foodpos = [Xfood * 10,  Yfood * 10]
    foodexist = True

    # if snake get into border
    if (snakepos[0] > mapsize - 20 or snakepos[0] < 20):
        GameOver()
    if (snakepos[1] > mapsize + 20 or snakepos[1] < 60):
        GameOver()

    # if snake kills himself
    for b in snakebody[1:]:
        if (snakepos[0] == b[0] and snakepos[1] == b[1]):
            GameOver()

    # border
    pygame.draw.rect(gameSurface, white, (10, 50, mapsize, mapsize), 1)
    showScore()
    pygame.display.flip()
