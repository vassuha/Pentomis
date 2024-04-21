import sys
import time

import pygame
import copy
from random import choice

pygame.init()
screenWidth = 1920-500
screenHeight = 1080-300

areaWidth = 10
areaHeight = 20
TEXTURE_WIDTH = 54
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)

class Figure:
    def __init__(self, name, area, form, rotationAngle, position, color, center):
        self.name = name
        self.form = form
        self.area = area
        self.rotationAngle = rotationAngle
        self.position = [0, 8]
        self.center = center

    def rotate(self, area):
        for i in range(len(self.form)):
            for j in range(len(self.form)):
                if (self.form[i][j] > 0):
                    area[self.position[0] + i][self.position[1] + j] = 0
        tempForm = copy.deepcopy(self.form)
        n = len(tempForm)
        for i in range(len(self.form)):
            for j in range(len(self.form)):
                self.form[i][j] = tempForm[n-j-1][i]

        centerOld = copy.deepcopy(self.center)
        temp = copy.deepcopy(self.center[0])
        self.center[0] = self.center[1]
        self.center[1] = n - temp - 1

        positionOld = copy.deepcopy(self.position)

        self.position[0] += -self.center[0] +centerOld[0]
        self.position[1] += -self.center[1] +centerOld[1]

        for i in range(len(self.form)):
            for j in range(len(self.form)):
                if (area[self.position[0] + i][self.position[1] + j] >0) and (self.form[i][j] >0):
                    self.position = copy.deepcopy(positionOld)
                    self.form = copy.deepcopy(tempForm)
                    self.center = copy.deepcopy(centerOld)
                    for i in range(len(self.form)):
                        for j in range(len(self.form)):
                            if self.form[i][j] > 0:
                                area[self.position[0] + i][self.position[1] + j] = self.form[i][j]
                    return False
        for i in range(len(self.form)):
            for j in range(len(self.form)):
                if self.form[i][j] > 0:
                    area[self.position[0] + i][self.position[1] + j] = self.form[i][j]


    def move(self, area, dir):
        if dir == "right":
            if self.position[1] + len(self.form) + 1 > len(area[0]):
                return False
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if(self.form[i][j] > 0):
                        area[self.position[0] + i][self.position[1] + j] = 0
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if ((area[self.position[0] + i][self.position[1] + j + 1] > 0) and (self.form[i][j] > 0)) or (self.form[i][j] > 0 and (self.position[1]+j) > 12):
                        for i in range(len(self.form)):
                            for j in range(len(self.form)):
                                if (self.form[i][j] > 0):
                                    area[self.position[0] + i][self.position[1] + j] = self.form[i][j]
                        return False
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if self.form[i][j] > 0:
                        area[self.position[0] + i][self.position[1] + j + 1] = self.form[i][j]
            self.position[1] += 1
        if dir == "left":
            if self.position[1] < 1:
                return False
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if(self.form[i][j] > 0):
                        area[self.position[0] + i][self.position[1] + j] = 0
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if ((area[self.position[0] + i][self.position[1] + j - 1] > 0) and (self.form[i][j] > 0)) or (self.form[i][j] > 0 and (self.position[1]+j) < 5):
                        for i in range(len(self.form)):
                            for j in range(len(self.form)):
                                if (self.form[i][j] > 0):
                                    area[self.position[0] + i][self.position[1] + j] = self.form[i][j]
                        return False
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if self.form[i][j] > 0:
                        area[self.position[0] + i][self.position[1] + j - 1] = self.form[i][j]
            self.position[1] -= 1
        if dir == "down":
            if self.position[0] + len(self.form) > len(area) - 1:
                return False

            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if(self.form[i][j] > 0):
                        area[self.position[0] + i][self.position[1] + j] = 0
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if ((area[self.position[0] + i + 1][self.position[1] + j] >0) and (self.form[i][j] > 0)) or (self.form[i][j] > 0 and (self.position[0]+i) > 22):
                        for i in range(len(self.form)):
                            for j in range(len(self.form)):
                                if (self.form[i][j] > 0):
                                    area[self.position[0] + i][self.position[1] + j] = self.form[i][j]
                        return False
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if self.form[i][j] > 0:
                        area[self.position[0] + i + 1][self.position[1] + j] = self.form[i][j]
            self.position[0] += 1
            return True

    def throw(self, area):
        while self.move(area, "down"):
            pass

def spawn(area, figure):
    figure.position[1] = len(area[0])//2 - len(figure.form)//2
    figure.position[0] = 3
    figure.rotationAngle = 0
    for i in range(len(figure.form)):
        for j in range(len(figure.form)):
            area[figure.position[0] + i][figure.position[1] + j] = figure.form[i][j]

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

running = True
area = []
for i in range(28):
    area.append([0] * 18)
    area[i][3] = 1;
    area[i][14] = 1;
area[24] = [1]*18

figures = []

pointForm= [[0, 0, 0], [0, 0, 0], [1, 0, 0]]
pointFigure = Figure("point", area, pointForm, 0, (0, 0), "red", [2, 0])
figures.append(pointFigure)

blueForm = [[0, 0, 0], [3, 0, 0], [3, 3, 3]]
blueFigure = Figure("blue", area, blueForm, 0, (0, 0), "blue", [2, 1])
figures.append(blueFigure)

greenForm = [[0, 0, 0], [0, 6, 6], [6, 6, 0]]
greenFigure = Figure("green", area, greenForm, 0, (0, 0), "green", [1, 1])
figures.append(greenFigure)

blackForm = [[18, 18, 0], [18, 18, 0], [18, 18, 0]]
blackFigure = Figure("black", area, blackForm, 0, (0, 0), "black", [1, 1])
figures.append(blackFigure)

lineForm = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 2, 2, 2]]
lineFigure = Figure("line", area, lineForm, 0, (0, 0), "purple", [3, 2])
figures.append(lineFigure)


bgColor = 'Black'
screen.fill(bgColor)
tempFigure = choice(figures)

spawn(area, tempFigure)

myFont = pygame.font.SysFont('Arial', 20)
text1 = [0]*28
for i in range(28):
    s = str(area[i])
    s = s.replace("1", "@");
    s = s.replace("1", " ");
    text1[i] = myFont.render(s, True, "White")

isMove = False

def timer(score=0):
    t=900-score*10
    if t<75:
        t = 75
    return t


MOVEMENT, T= pygame.USEREVENT, timer()
pygame.time.set_timer(MOVEMENT, T)

try:
    f = open("record.txt")
except FileNotFoundError:
    f = open("record.txt", "w")
    f.write("0" + "\n")

blocks = []
for i in range(1, 20):
    blocks.append(pygame.image.load("img/textures/Pentomis_texture_" + str(i) + ".png").convert())
def renderGameplay(area, background, score, blocks):
    bg = pygame.transform.scale(pygame.image.load(background).convert(), (screenWidth, screenHeight))

    blockHeight = screenHeight/areaHeight*0.9
    border = screenHeight//(270)

    screen.blit(bg, (0, 0)) #вывод
    pygame.draw.rect(screen, (255, 0, 0), (screenWidth/2-blockHeight*(areaWidth/2-1)-border/2, screenHeight/2-blockHeight*(areaHeight/2)-border/2, blockHeight*areaWidth+border, blockHeight*(areaHeight+1)+border/2), border)

    for i in range(3, 24):
        for j in range(4, 14):
            #Отладкаааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааа
            if area[i][j] >0:
                screen.blit(pygame.transform.scale(blocks[area[i][j]], (blockHeight, blockHeight)), (screenWidth/2+(j-8)*blockHeight, (i-2)*blockHeight))
    pygame.display.update()



def renderStartMenu(width, height):
    background = pygame.transform.scale(pygame.image.load("img/background/start.png").convert(), (width, height))
    screen.blit(background, (0, 0))
    menu = pygame.draw.rect(surface, color, pygame.Rect(30, 30, 60, 60),  2, 3)
    screen.blit(menu, (0, 0))

while running:
    #Создание игрового поля
    area = []
    for i in range(28):
        area.append([0] * 18)
        area[i][3] = 1;
        area[i][14] = 1;
    area[24] = [1] * 18

    score = 0
    bgColor = 'Black'
    screen.fill(bgColor)

    tempFigure = choice(figures)
    nextFigure = choice(figures)
    spawn(area, tempFigure)

    #Стартовое меню
    gameplay = False
    screen.fill(bgColor)
    screen.blit(myFont.render("Press any key to continue", True, "White"), (0, 20))
    while not gameplay:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == event.type == pygame.KEYDOWN:
                gameplay = True

    pygame.event.clear()
    ready = False
    while not ready:
        for e in pygame.event.get():
            if e.type == pygame.KEYUP:
                ready = True
    #Игровой процесс
    while gameplay:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and isMove==False:
            isMove = True
            tempFigure.move(area, "right")
        if keys[pygame.K_LEFT] and isMove==False:
            isMove = True
            tempFigure.move(area, "left")
        if keys[pygame.K_DOWN] and isMove==False:
            isMove = True
            tempFigure.throw(area)
        if keys[pygame.K_UP] and isMove==False:
            isMove = True
            tempFigure.rotate(area)

        #Отрисовка
        # screen.fill(bgColor)
        # for i in range(3, 24):
        #     s = str(area[i][4:14])
        #     #s = s.replace("1", "@");
        #     s = s.replace("2", "  ");
        #     text1[i] = myFont.render(s, True, "White")
        #     screen.blit(text1[i], (0, i*20))
        #
        # pygame.display.update()
        screenWidth = screen.get_size()[0]
        screenHeight = screen.get_size()[1]
        renderGameplay(area, "img/backgrounds/Minimalistic_landscape_1.jpg", score, blocks)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                sys.exit()
            if event.type == MOVEMENT:
                if checkCollision(area, tempFigure):
                    score = checkLine(area, score)
                    if checkEnd(area):
                        gameplay = False
                    tempFigure = nextFigure
                    nextFigure = choice(figures)
                    spawn(area, tempFigure)
                    isMove = False
                    pygame.display.update()
                tempFigure.move(area, "down")
                pygame.display.update()
                MOVEMENT, T = pygame.USEREVENT, timer(score)
                pygame.time.set_timer(MOVEMENT, T)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    isMove = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    isMove = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    isMove = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    isMove = False


        clock.tick(60)


    #Завершающее меню
    with open("record.txt") as f:
        record = int(f.readline())
    if score > record:
        record = score
    with open("record.txt", "w") as f:
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