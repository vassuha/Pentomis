import sys
import time
import copy
from random import choice
import pygame
from figure import figure
from button import ImageButton


pygame.init()
screenWidth = 1920-500
screenHeight = 1080-300

areaWidth = 10
areaHeight = 20
TEXTURE_WIDTH = 54
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)


def checkCollision(area, figure):
    for i in range(len(figure.form)):
        for j in range(len(figure.form)):
            if figure.form[i][j] > 0  and area[figure.position[0] + i+1][figure.position[1] + j] > 0:
                if i < len(figure.form)-1:
                    if figure.form[i+1][j] == 0:
                        return True
                else:
                    return True
    return False

def checkLine(area, score):
    lines = [0] * 28
    for i in range(3, 24):
        isLine = True
        for j in range(4, 14):
            if area[i][j] == 0:
                isLine = False
        if isLine:
            lines[i] = 1
    for k in range(3, 24):
        if lines[k] == 1:
            for i in range(k, 3, -1):
                area[i] = area[i - 1]
            area[3] = [0] * 18
            area[3][3] = 1
            area[3][14] = 1
    score += sum(lines[3:24])
    return score

def checkEnd(area):
    for j in range(4, 14):
        if area[4][j] > 0:
            return True


clock = pygame.time.Clock()

doomMusic = pygame.mixer.Sound("music/Doom Soundtrack.mp3")
#doomMusic.play()
doomMusic.set_volume(0.2)

area = []
for i in range(28):
    area.append([0] * 18)
    area[i][3] = 1;
    area[i][14] = 1;
area[24] = [1]*18

figures = []

#figures.append(figure("", area, [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, (0, 0), "", [, ]))
figures.append(figure("1", area, [[0, 0, 0], [1, 1, 0], [0, 1, 1]], 0, (0, 0), "red", [1, 1]))
figures.append(figure("2", area, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 2, 2, 2]], 0, (0, 0), "", [3, 2]))
figures.append(figure("3", area, [[0, 0, 0], [3, 0, 0], [3, 3, 3]], 0, (0, 0), "", [2, 1]))
figures.append(figure("4", area, [[0, 0, 0], [0, 0, 4], [4, 4, 4]], 0, (0, 0), "orange", [2, 1]))
figures.append(figure("5", area, [[0, 0, 0], [5, 5, 0], [5, 5, 0]], 0, (0, 0), "", [1, 1]))
figures.append(figure("6", area, [[0, 0, 0], [0, 6, 6], [6, 6, 0]], 0, (0, 0), "", [1, 1]))
figures.append(figure("7", area, [[0, 0, 0], [0, 7, 0], [7, 7, 7]], 0, (0, 0), "", [2, 1]))
figures.append(figure("8", area, [[8, 0], [8, 8]], 0, (0, 0), "", [1, 0]))
figures.append(figure("9", area, [[9, 9, 0], [0, 9, 9], [0, 9, 0]], 0, (0, 0), "", [1, 1]))
figures.append(figure("10", area, [[0, 0, 0, 0], [0, 0, 0, 0], [10, 10, 0, 0], [0, 10, 10, 10]], 0, (0, 0), "", [2, 1]))
figures.append(figure("11", area, [[0, 11, 11], [11, 11, 0], [0, 11, 0]], 0, (0, 0), "", [1, 1]))
figures.append(figure("12", area, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 12, 12], [12, 12, 12, 0]], 0, (0, 0), "", [3, 2]))
#figures.append(figure("13", area, [[13, 13, 0], [0, 13, 0], [0, 13, 13]], 0, (0, 0), "", [1, 1]))
figures.append(figure("14", area, [[0, 0, 0], [14, 0, 14], [14, 14, 14]], 0, (0, 0), "", [2, 1]))
#figures.append(figure("15", area, [[0, 15, 0], [15, 15, 15], [0, 15, 0]], 0, (0, 0), "", [1, 1]))
figures.append(figure("16", area, [[16, 16, 16], [0, 16, 0], [0, 16, 0]], 0, (0, 0), "", [1, 1]))
figures.append(figure("17", area, [[17, 0, 0], [17, 17, 0], [17, 17, 0]], 0, (0, 0), "", [1, 0]))
#figures.append(figure("18", area, [[18, 0, 0], [18, 0, 0], [18, 18, 18]], 0, (0, 0), "", [1, 1]))
figures.append(figure("19", area, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 19, 0], [19, 19, 19, 19]], 0, (0, 0), "", [3, 2]))
#figures.append(figure("20", area, [[0, 20, 20], [0, 20, 0], [20, 20, 0]], 0, (0, 0), "", [1, 1]))
figures.append(figure("21", area, [[0, 21, 0], [21, 21, 0], [21, 21, 0]], 0, (0, 0), "", [1, 1]))
figures.append(figure("22", area, [[0, 0, 0, 0], [0, 0, 0, 0], [22, 22, 22, 22],[0, 0, 22, 0]], 0, (0, 0), "", [2, 2]))

bgColor = 'Black'
tempfigure = choice(figures)

myFont = pygame.font.SysFont('Arial', 20)


isMove = False

def timer(score=0):
    t=900-score*10
    if t<75:
        t = 75
    return t


MOVEMENT, T= pygame.USEREVENT, timer(0)
pygame.time.set_timer(MOVEMENT, T)

try:
    f = open("/record.txt")
except FileNotFoundError:
    f = open("/record.txt", "w")
    f.write("0" + "\n")

blocks = []
blocks.append(pygame.image.load("img/textures/Pentomis_texture_" + str(20) + ".png").convert())
for i in range(1, 22+1):
    blocks.append(pygame.image.load("img/textures/Pentomis_texture_" + str(i) + ".png").convert())


def gaussian_blur(surface, radius):
    scaled_surface = pygame.transform.smoothscale(surface, (surface.get_width() // radius, surface.get_height() // radius))
    scaled_surface = pygame.transform.smoothscale(scaled_surface, (surface.get_width(), surface.get_height()))
    return scaled_surface

def speakerButton(x, y, figureWidth, imageWidth, indent ):
    global sound
    xm, ym = pygame.mouse.get_pos()
    if sound == 2:
        renderVoidButton(x, y, figureWidth, figureWidth)
        image1 = pygame.transform.scale(speaker, (imageWidth, imageWidth))  # картинка динамика
        screen.blit(image1, (x + indent , y + indent))
        doomMusic.set_volume(1)
    elif sound == 1:
        renderVoidButton(x, y, figureWidth, figureWidth)
        image2 = pygame.transform.scale(speakerOnLow, (imageWidth, imageWidth))  # картинка динамика
        screen.blit(image2, (x + indent, y + indent))
        doomMusic.set_volume(0.2)
    else:
        renderVoidButton(x, y, figureWidth, figureWidth)
        image3 = pygame.transform.scale(speakerOff, (imageWidth, imageWidth))  # картинка динамика
        screen.blit(image3, (x + indent, y + indent))
        doomMusic.set_volume(0)

    if x < xm < x + figureWidth and y < ym < y + figureWidth:
        if sound == 2:
            renderVoidButton(x, y, figureWidth, figureWidth)
            image1 = pygame.transform.scale(speaker, (imageWidth, imageWidth))  # картинка динамика
            screen.blit(image1, (x + indent , y + indent))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sound = 1
        elif sound == 1:
            renderVoidButton(x, y, figureWidth, figureWidth)
            image2 = pygame.transform.scale(speakerOnLow, (imageWidth, imageWidth))  # картинка динамика
            screen.blit(image2, (x + indent, y + indent))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sound = 0
        else:
            renderVoidButton(x, y, figureWidth, figureWidth)
            image3 = pygame.transform.scale(speakerOff, (imageWidth, imageWidth))  # картинка динамика
            screen.blit(image3, (x + indent, y + indent))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sound = 2


def buttonTwoStates(x, y, figureWidth, imageWidth, indent, state, passImage1, passImage2  ):
    xm, ym = pygame.mouse.get_pos()
    if state == True:
        renderVoidButton(x, y, figureWidth, figureWidth)
        image1 = pygame.transform.scale(passImage1, (imageWidth, imageWidth))  # картинка динамика
        screen.blit(image1, (x + indent , y + indent))
    elif state == False:
        renderVoidButton(x, y, figureWidth, figureWidth)
        image2 = pygame.transform.scale(passImage2, (imageWidth, imageWidth))  # картинка динамика
        screen.blit(image2, (x + indent, y + indent))

    if x < xm < x + figureWidth and y < ym < y + figureWidth:
        if state == True:
            renderVoidButton(x, y, figureWidth, figureWidth)
            image1 = pygame.transform.scale(passImage1, (imageWidth, imageWidth))  # картинка динамика
            screen.blit(image1, (x + indent , y + indent))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = False
                    return state
        elif state == False:
            renderVoidButton(x, y, figureWidth, figureWidth)
            image2 = pygame.transform.scale(passImage2, (imageWidth, imageWidth))  # картинка динамика
            screen.blit(image2, (x + indent, y + indent))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = True
                    return state



def renderTextButton(x, y, width, height, text, textSize):
    font1 = pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', textSize)
    rounding = screenHeight//36
    border = screenHeight//(270)
    color = (120, 122, 130)
    blockHeight = int(screenHeight // areaHeight * 0.9)
    area = pygame.Surface((width, height), pygame.SRCALPHA)
    translucentArea = pygame.Surface((width, height), pygame.SRCALPHA)
    translucentArea.set_alpha(200)
    pygame.draw.rect(translucentArea, (0, 0, 0), (0, 0, width, height), height, rounding)
    pygame.draw.rect(translucentArea, color, (0, 0, width, height), border, rounding)
    area.blit(translucentArea, (0, 0))
    #area.blit(scoreText, (0 + screenHeight / 100, 0 + screenHeight / 100))
    text = font1.render(str(text), True, "White")
    area.blit(text, (width//2-textSize*len(str(text))//10, height//2-textSize*len(str(text))//10))
    screen.blit(area, (x,y))

pauseIcon = pygame.image.load("img/icons/pause.png")
playIcon = pygame.image.load("img/icons/play.png")
crossIcon = pygame.image.load("img/icons/cross.png")
def renderImgButton(x, y, width, height, img, imgWidth, imgHeight):
    img = pygame.transform.scale(img, (imgWidth, imgHeight))
    rounding = screenHeight//36
    border = screenHeight//(270)
    color = (120, 122, 130)
    blockHeight = int(screenHeight // areaHeight * 0.9)
    area = pygame.Surface((width, height), pygame.SRCALPHA)
    translucentArea = pygame.Surface((width, height), pygame.SRCALPHA)
    translucentArea.set_alpha(200)
    pygame.draw.rect(translucentArea, (0, 0, 0), (0, 0, width, height), height, rounding)
    pygame.draw.rect(translucentArea, color, (0, 0, width, height), border, rounding)
    area.blit(translucentArea, (0, 0))
    #area.blit(scoreText, (0 + screenHeight / 100, 0 + screenHeight / 100))
    area.blit(img, (width//2-imgWidth//2, height//2-imgHeight//2))
    screen.blit(area, (x,y))

def renderVoidButton(x, y, width, height):
    rounding = screenHeight//36
    border = screenHeight//(270)
    color = (120, 122, 130)
    blockHeight = int(screenHeight // areaHeight * 0.9)
    area = pygame.Surface((width, height), pygame.SRCALPHA)
    translucentArea = pygame.Surface((width, height), pygame.SRCALPHA)
    translucentArea.set_alpha(200)
    pygame.draw.rect(translucentArea, (0, 0, 0), (0, 0, width, height), height, rounding)
    pygame.draw.rect(translucentArea, color, (0, 0, width, height), border, rounding)
    area.blit(translucentArea, (0, 0))
    screen.blit(area, (x,y))
bg = pygame.transform.scale(pygame.image.load("img/backgrounds/Minimalistic_landscape_1.jpg").convert(), (screenWidth, screenHeight))
meshColor = (120, 122, 130)
CloseMenuBg = pygame.transform.scale(pygame.image.load("img/backgrounds/Close_bg.jpg").convert(), (screenWidth, screenHeight))


def renderGameplay(area, score, blocks, nextfigure, tempfigure, deltaTime, isPause):
    global screen
    bg1 = pygame.transform.scale(bg, (screenWidth, screenHeight))

    blockHeight = int(screenHeight//areaHeight*0.9)
    border = screenHeight//(270)

    screen.blit(bg1, (0, 0)) #вывод

    gameplayArea = pygame.Surface(( blockHeight*areaWidth+border, blockHeight*(areaHeight+1)+border//2), pygame.SRCALPHA)
    #mesh = pygame.Surface(( 100, 100))

    mesh = pygame.Surface((blockHeight * areaWidth + border, blockHeight * (areaHeight + 1) + border // 2), pygame.SRCALPHA)
    mesh.fill((0, 0, 0))
    mesh.set_alpha(200)

    #pygame.draw.rect(screen, meshColor, (screenWidth//2-blockHeight*(areaWidth//2-1)-border//2, screenHeight//2-blockHeight*(areaHeight//2), blockHeight*areaWidth+border, blockHeight*(areaHeight+1)+border//2), border)
    pygame.draw.rect(mesh, meshColor, (0, 0, blockHeight*areaWidth+border, blockHeight*(areaHeight+1)+border//2), border)

    for i in range(areaWidth):
        pygame.draw.line(mesh, meshColor, (i*blockHeight, 0), (i*blockHeight, blockHeight*(areaHeight+1)))
    for i in range(1, areaHeight+1):
        pygame.draw.line(mesh, meshColor, (0, i*blockHeight), (blockHeight*areaWidth, i*blockHeight))

    #mesh = gaussian_blur(mesh, 100)

    gameplayArea.blit(mesh, (0, 0))

    area1 = copy.deepcopy(area)
    for i in range(len(tempfigure.form)):
        for j in range(len(tempfigure.form)):
            if (tempfigure.form[i][j] > 0):
                area1[tempfigure.position[0] + i][tempfigure.position[1] + j] = 0

    for i in range(len(tempfigure.form[0])):
        for j in range(len(tempfigure.form[1])):
            if tempfigure.form[i][j] != 0:
                if not checkCollision(area, tempfigure):
                    gameplayArea.blit(pygame.transform.scale(blocks[tempfigure.form[i][j]], (blockHeight, blockHeight)),((j+tempfigure.position[1] - 4) * blockHeight + border//2, (i+tempfigure.position[0] - 3) * blockHeight + (deltaTime/timer(score))*blockHeight ))
                else:
                    gameplayArea.blit(pygame.transform.scale(blocks[tempfigure.form[i][j]], (blockHeight, blockHeight)),((j + tempfigure.position[1] - 4) * blockHeight + border // 2,(i + tempfigure.position[0] - 3) * blockHeight))
                    pass

    for i in range(3, 24):
        for j in range(4, 14):
            if area1[i][j] >0:
                gameplayArea.blit(pygame.transform.scale(blocks[area1[i][j]], (blockHeight, blockHeight)), ((j-4)*blockHeight+border//2 , (i-3)*blockHeight) )

    if isPause:
        gameplayArea = gaussian_blur(gameplayArea, 50)
    screen.blit(gameplayArea, (screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) ,
                       screenHeight // 2 - blockHeight * (areaHeight // 2)))



    #Отображение текущего счета
    scoreAreaHeight = screenHeight//9
    scoreAreaWidth = scoreAreaHeight
    gameplayFont =pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', screenHeight//50)
    gameplayFont1 =pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', screenHeight//20)
    scoreArea = pygame.Surface((scoreAreaWidth, scoreAreaHeight), pygame.SRCALPHA)
    scoreText = gameplayFont.render("SCORE", True, "White")
    scoreText1 = gameplayFont1.render(str(score), True, "White")
    translucentArea = pygame.Surface((scoreAreaWidth, scoreAreaHeight), pygame.SRCALPHA)
    translucentArea.set_alpha(200)
    pygame.draw.rect(translucentArea, (0, 0, 0), (0, 0, scoreAreaHeight, scoreAreaHeight), scoreAreaHeight, scoreAreaHeight//4)
    pygame.draw.rect(translucentArea, meshColor, (0, 0, scoreAreaHeight, scoreAreaHeight), border, scoreAreaHeight // 4)
    scoreArea.blit(translucentArea, (0, 0))
    scoreArea.blit(scoreText, (0+screenHeight/75, 0+screenHeight/50))
    scoreArea.blit(scoreText1, (0+screenHeight/100- (len(str(score))-1)*screenHeight//50 +screenHeight//40, 0+screenHeight/50+ screenHeight/50))
    screen.blit(scoreArea, (screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) + blockHeight * areaWidth + border*10, screenHeight // 2 - blockHeight * (areaHeight // 2)))

    #Отображение следующей детали
    nextfigureAreaHeight = screenHeight // 4
    nextfigureAreaWidth = nextfigureAreaHeight
    nextfigureArea = pygame.Surface((nextfigureAreaWidth, nextfigureAreaHeight), pygame.SRCALPHA)
    nextfigureTranslucentArea = pygame.Surface((nextfigureAreaWidth, nextfigureAreaHeight), pygame.SRCALPHA)
    nextfigureTranslucentArea.set_alpha(200)
    pygame.draw.rect(nextfigureTranslucentArea, (0, 0, 0), (0, 0, nextfigureAreaWidth, nextfigureAreaWidth), nextfigureAreaWidth, scoreAreaHeight // 4)
    pygame.draw.rect(nextfigureTranslucentArea, meshColor, (0, 0, nextfigureAreaWidth, nextfigureAreaWidth), border, scoreAreaHeight // 4)
    nextfigureArea.blit(nextfigureTranslucentArea, (0, 0))

    for i in range(len(nextfigure.form)):
        for j in range(len(nextfigure.form[i])):
            if nextfigure.form[i][j] > 0:
                #nextfigureArea.blit(pygame.transform.scale(blocks[nextfigure.form[i][j]], (blockHeight, blockHeight)), (j*blockHeight + (nextfigureAreaHeight//2 - (len(nextfigure.form)+1)//2*blockHeight) + (((len(nextfigure.form)-1)/2+1+len(nextfigure.form)%2)-nextfigure.center[1])*blockHeight, (i)*blockHeight+ (nextfigureAreaHeight//2 - (len(nextfigure.form)+1)//2*blockHeight)+ (((len(nextfigure.form)-1)/2+1+len(nextfigure.form)%2)-nextfigure.center[0])*blockHeight))
                nextfigureArea.blit(pygame.transform.scale(blocks[nextfigure.form[i][j]], (blockHeight, blockHeight)), (j*blockHeight + nextfigureAreaHeight//2-len(nextfigure.form)*blockHeight//2 , i*blockHeight + nextfigureAreaHeight//2-(len(nextfigure.form) + (len(nextfigure.form)-3)*(nextfigure.center[0]))*blockHeight//2 ))
    screen.blit(nextfigureArea, (
    screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) + blockHeight * areaWidth + border * 10,
    screenHeight // 2 - blockHeight * (areaHeight // 2) + scoreAreaHeight + border*10))

    #buttonTwoStates(screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) + blockHeight * areaWidth + border*10 + scoreAreaHeight + border*10, screenHeight // 2 - blockHeight * (areaHeight // 2 ), scoreAreaHeight/1.4, scoreAreaHeight/1.4, isPause, pauseIcon, playIcon)
    renderImgButton(screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) + blockHeight * areaWidth + border*10 + scoreAreaHeight + border*10, screenHeight // 2 - blockHeight * (areaHeight // 2 ), scoreAreaHeight, scoreAreaHeight, pauseIcon, scoreAreaHeight/1.4, scoreAreaHeight/1.4)
    renderImgButton(screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) -scoreAreaWidth - border*10 , screenHeight // 2 - blockHeight * (areaHeight // 2 ), scoreAreaHeight, scoreAreaHeight, crossIcon, scoreAreaHeight/1.4, scoreAreaHeight/1.4)
    #speakerButton(screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) -scoreAreaWidth*2 - border*10*2, screenHeight // 2 - blockHeight * (areaHeight // 2 ), scoreAreaHeight, scoreAreaHeight*0.8, border*4)
    pause_button = ImageButton(screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) -scoreAreaWidth*2 - border*10*2, screenHeight // 2 - blockHeight * (areaHeight // 2 ), scoreAreaHeight, scoreAreaHeight, "",pauseIcon)
    pause_button.check_hover(pygame.mouse.get_pos())
    pause_button.draw(screen, areaHeight)

#звук не знал куда поставить, чтобы не обновлялось меняяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяять
sound = 2
flag = False
bgStart = pygame.transform.scale(pygame.image.load("img/backgrounds/Start1.png"), (screenWidth, screenHeight))
speaker = pygame.image.load("img/backgrounds/speaker.png")
speakerOnLow= pygame.image.load("img/backgrounds/speakerOnLow.png")
speakerOff = pygame.image.load("img/backgrounds/speakerOff.png")
buttonPlayS = pygame.image.load("img/backgrounds/buttonPlay2W.png")
def renderStartMenu():
    global sound
    global flag
    background1 = pygame.transform.scale((bgStart),(screenWidth, screenHeight))
    screen.blit(background1, (0, 0))
    if screenHeight > screenWidth:
        squareWidth = screenHeight//5
    else:
        squareWidth = screenWidth//5

    renderVoidButton(screenWidth//2 - squareWidth//2, screenHeight//2 - squareWidth//2,squareWidth, squareWidth)

    if sound == 2:
        renderVoidButton(screenWidth // 40 , screenHeight // 30 , squareWidth//5,squareWidth//5)
        background = pygame.transform.scale(speaker, (squareWidth//6, squareWidth//6)) #картинка динамика
        screen.blit(background, (screenWidth // 35 , screenHeight // 26 ))
        doomMusic.set_volume(1)
    elif sound == 1:
        renderVoidButton(screenWidth // 40, screenHeight // 30, squareWidth // 5, squareWidth // 5)
        background = pygame.transform.scale(speakerOnLow, (squareWidth//6, squareWidth//6)) #картинка динамика
        screen.blit(background, (screenWidth // 35 , screenHeight // 26 ))
        doomMusic.set_volume(0.2)
    else:
        renderVoidButton(screenWidth // 40, screenHeight // 30, squareWidth // 5, squareWidth // 5)
        background = pygame.transform.scale(speakerOff, (squareWidth//6, squareWidth//6)) #картинка динамика
        screen.blit(background, (screenWidth // 35 , screenHeight // 26 ))
        doomMusic.set_volume(0)
    mouse1, mouse2, mouse3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    if screenWidth * 0.025 < x < screenWidth * 0.063:
        if screenHeight * 0.031 < y < screenHeight * 0.1:
            if sound == 2:
                if mouse1 == False: flag = True
                renderVoidButton(screenWidth // 45, screenHeight // 35, squareWidth // 5 + squareWidth // 30, squareWidth // 5 + squareWidth // 30)
                background = pygame.transform.scale(speaker,(squareWidth // 5.3, squareWidth // 5.3))  # картинка динамика
                screen.blit(background, (screenWidth // 37, screenHeight // 28))
                if mouse1 == True and flag == True:
                    sound = 1
                    flag = False
            elif sound == 1:
                if mouse1 == False: flag = 1
                renderVoidButton(screenWidth // 45, screenHeight // 35, squareWidth // 5 + squareWidth // 30,squareWidth // 5 + squareWidth // 30)
                background = pygame.transform.scale(speakerOnLow,(squareWidth // 5.3, squareWidth // 5.3))  # картинка динамика
                screen.blit(background, (screenWidth // 37, screenHeight // 28))
                if mouse1 == True and flag == True:
                    sound = 0
                    flag = False
            else:
                if mouse1 == False: flag = 1
                renderVoidButton(screenWidth // 45, screenHeight // 35, squareWidth // 5 + squareWidth // 30,squareWidth // 5 + squareWidth // 30)
                background = pygame.transform.scale(speakerOff,(squareWidth // 5.3, squareWidth // 5.3))  # картинка динамика
                screen.blit(background, (screenWidth // 37, screenHeight // 28))
                if mouse1 == True and flag == True:
                    sound = 2
                    flag = False
    buttonPlay = pygame.transform.scale(buttonPlayS,(squareWidth // 2, squareWidth // 2))  # картинка динамика
    screen.blit(buttonPlay, (screenWidth // 2 - squareWidth // 2 * 0.45, screenHeight // 2 - squareWidth // 2 * 0.35))
    if (screenWidth * 0.47 < x < screenWidth * 0.542) and (screenHeight * 0.46 < y < screenHeight * 0.59):
        if mouse1 == False: flag = 1
        buttonPlay = pygame.transform.scale(buttonPlayS,(squareWidth // 1.7, squareWidth // 1.7))  # картинка динамика
        screen.blit(buttonPlay, (screenWidth//2 - squareWidth//2 * 0.52   , screenHeight//2 - squareWidth//2 * 0.435))
        if mouse1 == True and flag == True:
            sound = 2
            flag = False
            return True

    startFont =pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', squareWidth//7)
    startText = startFont.render("Pentomis", True, "White")
    screen.blit(startText, (screenWidth//2 - squareWidth//2 * 0.95   , screenHeight//2 - squareWidth//2 + squareWidth//9))

    pygame.display.update()
    return False


running = True
while running:
    #Создание игрового поля
    area = []
    for i in range(28):
        area.append([0] * 18)
        area[i][3] = 1;
        area[i][14] = 1;
    area[24] = [1] * 18

    score = 0

    tempfigure = choice(figures)
    nextfigure = copy.deepcopy(choice(figures))
    pausefigure = figure("-1", area, [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, (0, 0), "", [1, 1])


    #Стартовое меню
    gameplay = False
    flagCheckMouseClik = False
    while not gameplay:
        screenWidth = screen.get_size()[0]
        screenHeight = screen.get_size()[1]
        gameplay = renderStartMenu()
        if gameplay == True:
            flagCheckMouseClik = True
        for event in pygame.event.get():
            if event.type == event.type == pygame.KEYDOWN:
                gameplay = True
                isThrowing = False

    pygame.event.clear()
    if flagCheckMouseClik == False:
        ready = False
        while not ready:
            for e in pygame.event.get():
                if e.type == pygame.KEYUP:
                    ready = True

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                sys.exit()
    #Игровой процесс
    deltaTime = pygame.time.get_ticks()
    timeMove = pygame.time.get_ticks()
    isPause = False
    tempfigure.spawn(area)
    while gameplay:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            if pygame.time.get_ticks() - timeMove > 100:
                tempfigure.move(area, "right")
                timeMove = pygame.time.get_ticks()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and isMove==False:
            if pygame.time.get_ticks() - timeMove > 100:
                tempfigure.move(area, "left")
                timeMove = pygame.time.get_ticks()
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and isMove==False:
            isMove = True
            tempfigure.throw(area)
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and isMove==False:
            tempfigure.rotate(area)
            isMove = True
        if keys[pygame.K_SPACE] and isMove==False:
            isMove = True
            isPause = not(isPause)
            tempfigure, pausefigure = pausefigure, tempfigure



        screenWidth = screen.get_size()[0]
        screenHeight = screen.get_size()[1]
        renderGameplay(area, score, blocks, nextfigure, tempfigure, pygame.time.get_ticks()-deltaTime, isPause)
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                sys.exit()
            if event.type == MOVEMENT:
                if checkCollision(area, tempfigure):
                    score = checkLine(area, score)
                    if checkEnd(area):
                        gameplay = False
                    tempfigure = nextfigure
                    nextfigure = copy.deepcopy(choice(figures))
                    isThrowing = False
                    if not tempfigure.spawn(area):
                        gameplay = False
                tempfigure.move(area, "down")
                MOVEMENT, T = pygame.USEREVENT, timer(score)
                pygame.time.set_timer(MOVEMENT, T)
                deltaTime = pygame.time.get_ticks()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    isMove = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    isMove = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    isMove = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    isMove = False
                if event.key == pygame.K_SPACE:
                    isMove = False
            if event.type == pygame.VIDEORESIZE:

                width = min(1920, max(300, event.w))
                height = min(1080, max(300, event.h))

                if (width, height) != event.size:
                    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        clock.tick(60)


    #Завершающее меню
    with open("./record.txt") as f:
        record = int(f.readline())
    if score > record:
        record = score
    with open("/record.txt", "w") as f:
            f.write(str(record) + "\n")
    screen.fill(bgColor)
    screen.blit(myFont.render("You lose. Score: " + str(score) + " , record: " + str(record), True, "White"), (0, 20))
    screen.blit(myFont.render("Do you want to continue?", True, "White"), (0, 100))
    screen.blit(myFont.render("Play again (Y)                   Quit (N)", True, "White"), (0, 200))
    pygame.display.update()
    time.sleep(0.5)

    #Продолжить или завершить
    isContinue = False
    while not isContinue:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    isContinue = True
                if event.key == pygame.K_n:
                    running = False
                    print("Stop")
                    isContinue = True
running = False
pygame.quit()
sys.exit()