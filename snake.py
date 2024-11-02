# Import libraries
import pygame
import random
import time
import configparser
import os
from text import text

pygame.init()


# Default values

m = 20  # unit pixel
speed = 0

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

obslist = []
spawned = False

defaultSettings = {
    "lang": 0,  # ? Language
    "gvol":  3,  # ? Sound effect volume
    "mvol":  1,  # ? Music volume
    # "midx": 0,
    "currentOption": 0  # ! Current option / Don't touch this shit
}

defaultHighscore = {
    "endless": 0,
    "obstacles": 0,
    "classic": 0
}

# ? Game Settings
mainSettings = defaultSettings
gameHighscore = defaultHighscore

config = configparser.ConfigParser()
if os.path.exists('dat.ini'):
    config.read('dat.ini')

    mainSettings = {
        "lang": int(config.get("Settings", "lang")),
        "gvol":  int(config.get("Settings", "gvol")),
        "mvol":  int(config.get("Settings", "mvol")),
        "currentOption": 0
    }

    gameHighscore = {
        "endless": int(config.get("Highscore", "endless")),
        "obstacles": int(config.get("Highscore", "obstacles")),
        "classic": int(config.get("Highscore", "classic"))
    }
else:
    config['Settings'] = defaultSettings
    config['Highscore'] = defaultHighscore

    with open('dat.ini', 'w') as configfile:
        config.write(configfile)


gameAEffect = {
    "boop1": pygame.mixer.Sound("./audio/boop1.wav"),
    "select": pygame.mixer.Sound("./audio/select.wav"),
    "explosion": pygame.mixer.Sound("./audio/explosion.wav"),
}

gameValue = {
    "tick": 0,
    "maxtick": 30,
}

page = {
    "index": -1
}


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


def saveConfigFile():
    global config

    config["Settings"] = {
        "lang": str(mainSettings["lang"]),
        "gvol": str(mainSettings["gvol"]),
        "mvol": str(mainSettings["mvol"]),
    }

    config["Highscore"] = {
        "classic": str(gameHighscore["classic"]),
        "endless": str(gameHighscore["endless"]),
        "obstacles": str(gameHighscore["obstacles"]),
    }

    with open('dat.ini', 'w') as configfile:
        config.write(configfile)


def resetGameValue():
    global snakepos, snakebody, foodpos, foodexist, direction, changeto, score, obslist, spawned
    snakepos = [100, 60]
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

    obslist = []
    spawned = False

# Function when game is over


def getHighScore():
    hsCode = ["classic", "endless", "obstacles"]
    type_ = hsCode[lobby["mode"]]
    prevScore = gameHighscore[type_]

    return prevScore


def setHighScore(news):
    hsCode = ["classic", "endless", "obstacles"]
    type_ = hsCode[lobby["mode"]]
    gameHighscore[type_] = news


def GameOver():

    global gameSurface
    x = pygame.display.Info().current_w / 2

    prevScore = getHighScore()
    niceJOB = False

    if (score > prevScore):
        setHighScore(score)
        niceJOB = True

    drawText("Game Over!", x, 150, 50, orange, "center")
    showScore(score, True)

    drawText("{0} Highscore: {1}".format(
        "Previous" if niceJOB else "", prevScore), x, 250, 30, white, "center")

    drawText("Press [R] to retry", x, 330, 15, white, "center")
    drawText("Press [F] to return to option menu",
             x, 360, 15, white, "center")
    drawText("Press [Esc] to exit", x, 390, 15, white, "center")

    sss = {"wait": True}

    while sss["wait"]:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_r):
                    sss["wait"] = False
                    # YOU_NEED_TO = "Insert variable reset function here"
                    resetGameValue()
                    #! Code retry
                if (event.key == pygame.K_f):
                    sss["wait"] = False
                    # YOU_NEED_TO = "Insert variable reset function here"
                    resetGameValue()
                    page["index"] = 0
                if (event.key == pygame.K_ESCAPE):
                    sss["wait"] = False
                    app["running"] = False

        pygame.display.update()

    gameSurface = pygame.display.set_mode((windowWidth, windowHeight))


# Function to show score
def showScore(score, failed):
    if (failed == False):   # normal
        drawText('Score: {0}'.format(score), 10, 15, 20, white)
        drawText('Hi-Score: {0}'.format(getHighScore()),
                 windowWidth - 10, 15, 20, white, "topright")
    else:   # game over
        drawText('Score: {0}'.format(score), windowWidth / 2, 200,
                 30, white, "center")

# Function to show screen


def showScreen(skins):
    gameSurface.fill(black)

    for pos in obslist:
        pygame.draw.rect(gameSurface, white, pygame.Rect(
            pos[0], pos[1], m, m))
    if (skins == 0):
        for pos in snakebody:
            pygame.draw.rect(gameSurface, red, pygame.Rect(
                pos[0], pos[1], m-1, m-1))
        pygame.draw.rect(gameSurface, orange, pygame.Rect(
            snakebody[0][0], snakebody[0][1], m-1, m-1))    # snake's head
    else:
        if (skins == 1):
            Imgbody = pygame.transform.scale(
                pygame.image.load(".\skins\Plant\Body.png"), (m, m))
            Imghead = pygame.transform.scale(
                pygame.image.load(".\skins\Plant\Head.png"), (m, m))
            Imgtail = pygame.transform.scale(
                pygame.image.load(".\skins\Plant\Tail.png"), (m, m))
        if (skins == 2):
            Imgbody = pygame.transform.scale(
                pygame.image.load(".\skins\Flower\Body.png"), (m, m))
            Imghead = pygame.transform.scale(
                pygame.image.load(".\skins\Flower\Head.png"), (m, m))
            Imgtail = pygame.transform.scale(
                pygame.image.load(".\skins\Flower\Tail.png"), (m, m))
        if (skins == 3):
            Imgbody = pygame.transform.scale(
                pygame.image.load(".\skins\Ruin\Body.png"), (m, m))
            Imghead = pygame.transform.scale(
                pygame.image.load(".\skins\Ruin\Head.png"), (m, m))
            Imgtail = pygame.transform.scale(
                pygame.image.load(".\skins\Ruin\Tail.png"), (m, m))
        for pos in snakebody:
            gameSurface.blit(Imgbody, pygame.Rect(pos[0], pos[1], m-1, m-1))
        gameSurface.blit(Imghead, pygame.Rect(
            snakebody[0][0], snakebody[0][1], m-1, m-1))    # snake's head
        gameSurface.blit(Imgtail, pygame.Rect(
            snakebody[len(snakebody)-1][0], snakebody[len(snakebody)-1][1], m-1, m-1))    # snake's tail

    # food
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


def randomFood_withWalls():
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

    obstacles = lobby["obsc"] + 1
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
                # if (selected == 0):
                #     gameSurface = pygame.display.set_mode(
                #         (mapsize+20, mapsize+60))
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

    return page["index"]


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

    return page["index"]


lobby = {
    "currentOption": 0,
    "skin": 0,  # ? Snake skin (0 default/ 1 plant/ 2 flower / 3 ruin)
    "mode": 0,  # ? Gamemode (0 classic/ 1 endless / 2 obsst)
    "wall": 0,
    "obsc": 0
}


def drawMainLobby(gameEvents):

    x = windowWidth / 2
    selected = lobby["currentOption"]
    drawText(getText("game_opt"), x, 150, 30, yellow, "center")

    skinOpt = [getText("default"), "Plant", "Flower", "Ruin"]
    modeOpt = [getText("classic_opt"), getText(
        "endless_opt"), getText("obstacles_opt")]
    wallOpt = [getText("no"), getText("yes")]
    obscOpt = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    arr = [skinOpt, modeOpt, wallOpt, obscOpt, [], []]

    def gf(a):
        name = ["skin", "mode", "wall", "obsc"][a]

        def func(i):
            playEffect("boop1")
            lobby[name] += i
            if (lobby[name] < 0):
                lobby[name] = len(arr[a]) - 1
            if (lobby[name] > len(arr[a]) - 1):
                lobby[name] = 0
        return func

    def ef(i):
        return page["index"]

    def toMainMenu(i):
        global gameSurface
        playEffect("select")
        gameSurface = pygame.display.set_mode(
            (mapsize+20, mapsize+60))
        return -1

    def toGame(i):
        playEffect("select")
        return 4

    func = [gf(0), gf(1), gf(2) if lobby["mode"] != 0 else ef,
            gf(3) if lobby["mode"] != 0 else ef, ef, ef]
    rtrn = [ef, ef, ef, ef, toGame, toMainMenu]

    for event in gameEvents:
        if (event.type == pygame.QUIT):
            app["running"] = False

        # key input
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_RIGHT):
                func[selected](1)
            if (event.key == pygame.K_LEFT):
                func[selected](-1)
            if (event.key == pygame.K_UP):
                lobby["currentOption"] = 5 if selected == 0 else selected - 1
                if (selected == 4 and lobby["mode"] != 2):
                    lobby["currentOption"] = 1
                playEffect("boop1")
            if (event.key == pygame.K_DOWN):
                lobby["currentOption"] = 0 if selected == 5 else selected + 1
                if (selected == 1 and lobby["mode"] != 2):
                    lobby["currentOption"] = 4
                playEffect("boop1")

            if (event.key == pygame.K_RETURN):
                return rtrn[selected](0)

    def getColor(i):
        return yellow if i == selected else white

    def getAlpha(i):
        return white if i == selected and len(arr[i]) > 1 else pygame.Color(0, 0, 0, 0)

    drawText("Snake skin", x, 200, 20, white, "center")
    drawText("<", x - 150, 240, 40, getAlpha(0), "center")
    drawText(">", x + 150, 240, 40, getAlpha(0), "center")
    drawText(skinOpt[lobby["skin"]], x, 240, 24, getColor(0), "center")

    prevScore = getHighScore()

    gameType = "{0} - {1}: {2}".format("Gamemode",
                                       "Highscore", str(prevScore))

    drawText(gameType, x, 290, 20, white, "center")
    drawText("<", x - 150, 330, 40, getAlpha(1), "center")
    drawText(">", x + 150, 330, 40, getAlpha(1), "center")
    drawText(modeOpt[lobby["mode"]], x, 330, 24, getColor(1), "center")

    drawText(getText("play_btt"), x, 470, 25, getColor(4), "center")
    drawText(getText("menu_back_btt"), x, 510, 25, getColor(5), "center")

    if (lobby["mode"] != 2):
        return page["index"]

    drawText("Enable walls", 30, 360, 20, white, "topleft")
    drawText("<          >", 2 * x - 40, 360, 20, getAlpha(2), "topright")
    drawText(wallOpt[lobby["wall"]], 2 * x - 60,
             360, 20, getColor(2), "topright")

    drawText("Number of obstacles (1-15)", 30, 400, 20, white, "topleft")
    drawText("<          >", 2 * x - 40, 400, 20, getAlpha(3), "topright")
    drawText(str(obscOpt[lobby["obsc"]]),  2 * x - 60,
             400, 20, getColor(3), "topright")

    return page["index"]


playMusic("music2", fade_ms=2500)
page["index"] = -1


app = {"running": True}
# Main menu options
while app["running"]:
    gameSurface.fill(black)

    drawText(getText("title"), windowWidth / 2, 100, 40, yellow, "center")

    drawText("Built Alpha 1.0.7", 7, windowHeight - 30, 10, white, "topleft")
    drawText("All Right Reserved - Group 1 (c) 2022 - 2023",
             7, windowHeight - 15, 10, white, "topleft")

    gameEvents = pygame.event.get()

    for event in gameEvents:
        if (event.type == pygame.QUIT):
            #!SAVE CONFIG FILE
            app["running"] = False

    match page["index"]:
        case 0:
            page["index"] = drawMainLobby(gameEvents)
        case 1:
            page["index"] = drawMainSettings(gameEvents)
        case 2:
            page["index"] = drawMainCredit(gameEvents)
        case 3:
            pygame.mixer.music.fadeout(1000)
            time.sleep(1.25)
            app["running"] = False
        case 4:
            page["index"] = 4
            if (lobby["mode"] == 2 and spawned == False):
                randomObstacles()
                spawned = True

            for event in gameEvents:
                if (event.type == pygame.QUIT):
                    app["running"] = False

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

            showScreen(lobby["skin"])

            # if snake crash into the obstacles
            for pos in obslist:
                if (snakepos[0] == pos[0] and snakepos[1] == pos[1]):
                    GameOver()

            # food shows up
            if (foodexist == False):
                if (lobby["mode"] == 2 and lobby["wall"] == 1):
                    Xfood, Yfood = randomFood_withWalls()
                else:
                    Xfood, Yfood = randomFood()
                foodpos = [Xfood * 10,  Yfood * 10]
            foodexist = True

            # if snake get into border
            if (lobby["mode"] == 0 or (lobby["mode"] == 2 and lobby["wall"] == 1)):
                if (snakepos[0] > mapsize - 20 or snakepos[0] < 20):
                    GameOver()
                if (snakepos[1] > mapsize + 20 or snakepos[1] < 60):
                    GameOver()
            else:
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
            pygame.draw.rect(gameSurface, white,
                             (10, 50, mapsize + 20, mapsize + 15), 1)
            showScore(score, False)
        case _:
            page["index"] = drawMainMenu(gameEvents)

    pygame.display.update()


saveConfigFile()
print("Config file saving")

pygame.quit()
