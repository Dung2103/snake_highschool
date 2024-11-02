# Import libraries
import pygame
import random
import time
import sys
import os
from text import text

pygame.init()


# Default values

m = 20  # unit pixel

red = pygame.Color(255,  0,  0)
orange = pygame.Color(255, 165, 0)
blue = pygame.Color(65,  105,  255)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
yellow = pygame.Color(255, 255, 0)

# Main window
windowWidth = 540
windowHeight = 580
mapsize = 500
gameSurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Snake Game')

# Varibles
# about snake
snakepos = [100, 60]
snakebody = [[100, 60], [80, 60], [60, 60]]

# about food
Xfood = random.randrange(2, 48)
Yfood = random.randrange(6, 52)
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

obstacles = 10
obslist = []

# ? Game Settings
mainSettings = {
    "lang": 0,  # ? Language
    "gvol":  5,  # ? Sound effect volume
    "mvol":  3,  # ? Music volume
    "currentOption": 0  # ! Current option / Don't touch this shit
}

gameAEffect = {
    "boop1": pygame.mixer.Sound("./audio/boop1.wav"),
    "select": pygame.mixer.Sound("./audio/select.wav"),
}

gameValue = {
    "tick": 0,
    "maxtick": 30,
}


def reset():
    snakepos=[100,60]
    snakebody = [[100, 60], [80, 60], [60, 60]]

    Xfood = random.randrange(2, 48)
    Yfood = random.randrange(6, 52)
    if (Xfood % 2 != 0):
        Xfood += 1
    if (Yfood % 2 != 0):
        Yfood += 1
    foodpos = [Xfood * 10,  Yfood * 10]
    foodexist = True

    direction = 'RIGHT'
    changeto = direction
    score = 0
    
    gameValue["maxtick"] = 30
    gameValue["tick"] = 0


def playEffect(id, time=1):
    if (gameAEffect.get(id)):
        gameAEffect[id].set_volume(mainSettings["gvol"]/10)
        gameAEffect[id].play()


def changeMusicVolume():
    pygame.mixer.music.set_volume(mainSettings["mvol"]/10)


def playMusic(id, fade_ms=0, time=-1):
    pygame.mixer.music.load("./audio/{0}.mp3".format(id))
    changeMusicVolume()
    pygame.mixer.music.play(fade_ms=fade_ms, loops=time)


def getText(id):
    langList = ["en", "vi"]

    if (text[id].get("gb")):
        return text[id]["gb"]

    lang = langList[mainSettings["lang"]]

    return text[id][lang]


def drawText(text="", x=0, y=0, size=30, color=white, align="topleft", bold=False):
    # ? define text
    # sfont = pygame.font.SysFont(mainFont, size, bold=bold)
    mainFont = pygame.font.Font("./fonts/Determination.ttf", size + 5)
    ssurf = mainFont.render(text, True, color)
    # ? define space
    srect = ssurf.get_rect()

    match align:
        case "topleft":
            srect.topleft = (x, y)

        case "topright":
            srect.topright = (x, y)

        case "center":
            srect.center = (x, y)

    # ? draw
    gameSurface.blit(ssurf, srect)


# Function when game is over
def GameOver():
    drawText("Game Over", 260, 210, 50, orange, "center")
    showScore(score, True)
    pygame.display.flip()

    time.sleep(5)  # time wait to exit
    pygame.quit()
    sys.exit()


# Function to show score
def showScore(score, failed):
    if (failed == False):   # normal
        drawText('Score: {0}'.format(score), 10, 15, 20, white)
    else:   # game over
        drawText('Score: {0}'.format(score), 260, 270,
                 30, white, "center")

# Function to show screen


def showScreen():
    gameSurface.fill(black)

    for pos in obslist:
        pygame.draw.rect(gameSurface, white, pygame.Rect(
            pos[0], pos[1], m, m))

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
                check = False
                break

        if (check == True):
            return Xfood, Yfood
        
def randomFood_inWalls():
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
                check = False
                break

        for curobs in obslist:
            if (Xfood == curobs[0] and Yfood == curobs[1]):
                check = False
                break

        if (check == True):
            return Xfood, Yfood
        
def randomObstacles():
    check = True
    counter = 1

    while (counter <= obstacles):
        Xobs = random.randrange(2, mapsize/10 - 2)
        Yobs = random.randrange(6, mapsize/10 - 2)
        if (Xobs % 2 != 0):
            Xobs += 1
        if (Yobs % 2 != 0):
            Yobs += 1
        for obs in obslist:
            if (Xobs == obs[0] or Yobs == obs[1]):
                check = False
                break

        if (check == True):
            obslist.insert(0, [Xobs*10, Yobs*10])
            counter += 1

# Identify direction


def getDirection(changeto, direction):
    if (changeto == 'RIGHT' and not direction == 'LEFT'):
        direction = 'RIGHT'
    if (changeto == 'LEFT' and not direction == 'RIGHT'):
        direction = 'LEFT'
    if (changeto == 'UP' and not direction == 'DOWN'):
        direction = 'UP'
    if (changeto == 'DOWN' and not direction == 'UP'):
        direction = 'DOWN'
    return direction


mainMenu = {}
mainMenu["currentOption"] = 0


def drawMainMenu(gameEvents):
    options = list(map(getText, ["play_btt", "settings_btt",
                                 "about_btt", "quit_btt"]))
    selected = mainMenu["currentOption"]

    for event in gameEvents:
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_UP):
                mainMenu["currentOption"] = selected - \
                    1 if selected > 0 else 3
                playEffect("boop1")

            if (event.key == pygame.K_DOWN):
                mainMenu["currentOption"] = selected + 1 if selected < 3 else 0
                playEffect("boop1")

            if (event.key == pygame.K_RETURN):
                playEffect("select")
                if (selected == 0):
                    gameSurface = pygame.display.set_mode(
                        (mapsize+20, mapsize+60))
                return selected

    drawText(getText("subtitle"), windowWidth / 2, 140, 20, white, "center")

    start = 260
    for i in range(len(options)):
        tag = "{0}"
        color = white

        if (selected == i):
            tag = ">     {0}     <"
            color = yellow

        option = options[i]
        drawText(tag.format(option), windowWidth / 2, start + 60 * i, 25,
                 color, "center", bold=(i == selected))

    pygame.display.flip()

    return -1


def drawMainSettings(gameEvents):
    types = [
        {
            "button": False,
            "title": getText("ln_opt"),
            "options": ["English", "Tiếng Việt"],
            "id": "lang",
        },
        {
            "button": False,
            "title": getText("gvol_opt") + " (0-10)",
            "options": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "id": "gvol",
        },
        {
            "button": False,
            "title": getText("mvol_opt") + " (0-10)",
            "options": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "id": "mvol",
            "onchange": changeMusicVolume
        },
        {
            "button": True,
            "title":  getText("menu_back_btt"),
            "id": "nav_back"
        }

    ]

    selected = mainSettings["currentOption"]
    sData = types[selected]

    isButton = sData["button"]
    currentSIndex = 0
    maxSLength = 0
    onchange = sData.get("onchange")

    if (not isButton):
        currentSIndex = mainSettings[sData["id"]]
        maxSLength = len(sData["options"])

    for event in gameEvents:

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_UP):
                mainSettings["currentOption"] = selected - \
                    1 if selected > 0 else len(types) - 1
                playEffect("boop1")

            if (event.key == pygame.K_DOWN):
                mainSettings["currentOption"] = selected + \
                    1 if selected < len(types) - 1 else 0
                playEffect("boop1")

            if (event.key == pygame.K_LEFT and (not isButton)):
                if (currentSIndex > 0):
                    playEffect("boop1")
                    mainSettings[types[selected]["id"]] -= 1
                    if (onchange):
                        onchange()

            if (event.key == pygame.K_RIGHT and (not isButton)):
                if (currentSIndex < maxSLength - 1):
                    playEffect("boop1")
                    mainSettings[types[selected]["id"]] += 1
                    if (onchange):
                        onchange()

            if (event.key == pygame.K_RETURN and isButton):

                match sData["id"]:
                    case "nav_back":
                        playEffect("select")
                        mainSettings["currentOption"] = 0
                        return -1

    drawText(getText("settings_btt"), windowWidth /
             2, 160, 25, white, "center")

    size = 20
    gap = size * 3
    start = 250

    for i in range(len(types)):
        option = types[i]

        if (option["button"]):
            drawText(option["title"], 40, start + gap * i, size,
                     yellow if selected == i else white, "topleft", bold=(selected == i))

        else:
            current = mainSettings[option["id"]]

            display = str(option["options"][current])
            arrow = "  {0}  "
            color = white

            if (selected == i):
                arrow = "<  {0}  >"
                if (current + 1 == maxSLength):
                    arrow = "<  {0}  "
                elif (current == 0):
                    arrow = "  {0}  >"

                color = yellow

            drawText(option["title"], 40, start + gap * i, size,
                     color, "topleft", bold=(selected == i))

            drawText(arrow.format(display), windowWidth - 40, start + gap * i, size,
                     color, "topright", bold=(selected == i))

    return currentPage


credit = {"p": 0}  # ! Credit's page index


def drawMainCredit(gameEvents):
    x = windowWidth / 2

    drawText(getText("about_btt"), x, 160, 25, white, "center")

    pageNav = "<       {0}/2       >"
    drawText(pageNav.format(credit["p"] + 1), x, 200, 18, white, "center")

    if (credit["p"] == 1):
        drawText(getText("music"), x, 240, 16, white, "center")
        drawText(getText("funnybit"), x, 265, 16, white, "center", bold=True)

        drawText(getText("sound"), x, 300, 16, white, "center")
        drawText(getText("jsxfr"), x, 325, 16, white, "center", bold=True)
    else:
        drawText(getText("idea"), x, 240, 16, white, "center")
        drawText(getText("long"), x, 265, 16, white, "center", bold=True)

        drawText(getText("coder"), x, 300, 16, white, "center")
        drawText(getText("khang"), x, 325, 16, white, "center", bold=True)
        drawText(getText("quan"), x, 350, 16, white, "center", bold=True)

        drawText(getText("paperwork"), x, 390, 16, white, "center")
        drawText(getText("dung"), x, 415, 16, white, "center", bold=True)

        drawText(getText("presenter"), x, 450, 16, white, "center")
        drawText(getText("trung"), x, 475, 16, white, "center", bold=True)

    drawText(getText("any_to_return"), x, 510,
             16, yellow, "center", bold=True)

    for event in gameEvents:
        if (event.type == pygame.KEYDOWN):

            if (event.key == pygame.K_LEFT):
                credit["p"] = credit["p"] - 1 if credit["p"] > 0 else 1
                playEffect("boop1")

            if (event.key == pygame.K_RIGHT):
                credit["p"] = credit["p"] + 1 if credit["p"] < 1 else 0
                playEffect("boop1")

            if (event.key == pygame.K_RETURN):
                playEffect("select")
                return -1

    return currentPage


currentPage = -1


playMusic("music2", fade_ms=2500)

# Main menu options
randomObstacles()
while True:
    gameSurface.fill(black)

    drawText(getText("title"), windowWidth / 2, 100, 40, yellow, "center")

    drawText("Built Alpha 1.0.7", 7, windowHeight - 30, 10, white, "topleft")
    drawText("All Right Reserved - Group 1 (c) 2022 - 2023",
             7, windowHeight - 15, 10, white, "topleft")

    gameEvents = pygame.event.get()

    for event in gameEvents:
        if (event.type == pygame.QUIT):
            pygame.quit()

    match currentPage:
        case 0:
            currentPage = 0

            for event in gameEvents:
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

            if (gameValue["tick"] > 0):
                gameValue["tick"] -= 1
                continue
            else:
                gameValue["tick"] = gameValue["maxtick"]

                direction = getDirection(changeto, direction)

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
                if ((score % 3 == 0 and score > 0 and gameValue["maxtick"] > 5)):
                    gameValue["maxtick"] -= 1
            else:
                snakebody.pop()

            showScreen()

            # food shows up
            if (foodexist == False):
                Xfood, Yfood = randomFood_inWalls()
                foodpos = [Xfood * 10,  Yfood * 10]
            foodexist = True

            for pos in obslist:
                if (snakepos[0] == pos[0] and snakepos[1] == pos[1]):
                    GameOver()

            # if snake get into border
            # walls mode
            if (snakepos[0] > mapsize - 20 or snakepos[0] < 20):
                GameOver()
            if (snakepos[1] > mapsize + 20 or snakepos[1] < 60):
                GameOver()

            # no walls mode
            if (snakepos[0] > mapsize - 20):
                snakepos[0] = 20
            if (snakepos[0] < 20):
                snakepos[0] = mapsize

            if (snakepos[1] > mapsize + 20):
                snakepos[1] = 60
            if (snakepos[1] < 60):
                snakepos[1] = mapsize + 20

            # if snake kills himself
            for b in snakebody[1:]:
                if (snakepos[0] == b[0] and snakepos[1] == b[1]):
                    GameOver()

            # border
            pygame.draw.rect(gameSurface, white, (10, 50, mapsize, mapsize), 1)
            showScore(score, False)
        case 1:
            currentPage = drawMainSettings(gameEvents)
        case 2:
            currentPage = drawMainCredit(gameEvents)
        case 3:
            pygame.mixer.music.fadeout(1000)
            time.sleep(1.25)
            pygame.quit()
        case _:
            currentPage = drawMainMenu(gameEvents)

    pygame.display.update()
