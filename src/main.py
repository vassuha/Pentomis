import sys
import time
import copy
from random import choice
import pygame
from figure import figure
from render import *
from globals import *


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



def timer(score=0):
    t=900-score*10
    if t<75:
        t = 75
    return t


MOVEMENT, T= pygame.USEREVENT, timer(0)
pygame.time.set_timer(MOVEMENT, T)

try:
    f = open("./record.txt")
except FileNotFoundError:
    f = open("./record.txt", "w")
    f.write("0" + "\n")



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
    while not gameplay:
        screenWidth = screen.get_size()[0]
        screenHeight = screen.get_size()[1]
        start_menu_buttons = renderStartMenu(sound)
        start_button = start_menu_buttons[0]
        speaker_button = start_menu_buttons[1]
        cross_button = start_menu_buttons[2]
        for event in pygame.event.get():
            start_button.check_hover(pygame.mouse.get_pos())
            start_button.handle_event(event)
            speaker_button.check_hover(pygame.mouse.get_pos())
            speaker_button.handle_event(event)
            cross_button.check_hover(pygame.mouse.get_pos())
            cross_button.handle_event(event)

            if event.type == event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
                isThrowing = False
                while not gameplay:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            gameplay = True
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT+1:
                if event.button == "start":
                    gameplay = True
                if event.button == "speaker":
                    sound = (sound) % 3 + 1
                    if sound == 1:
                        gameplay_music.set_volume(0.2)
                    elif sound == 2:
                        gameplay_music.set_volume(1)
                    elif sound == 3:
                        gameplay_music.set_volume(0)
                if event.button == "cross":
                    running = False
                    pygame.quit()
                    sys.exit()

    #Игровой процесс
    deltaTime = pygame.time.get_ticks()
    timeMove = pygame.time.get_ticks()
    isPause = False
    tempfigure.spawn(area)
    gameplay_music.play(loops=-1)
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
        buttons = renderGameplay(area, score, blocks, nextfigure, tempfigure, pygame.time.get_ticks()-deltaTime, isPause, sound)
        speaker_button = buttons[0]
        pause_button = buttons[1]
        play_button = buttons[2]
        cross_button = buttons[3]
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

                height = min(1080, max(300, event.h))
                width = min(1920, max(300, event.w))

                if (width, height) != event.size:
                    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            pause_button.check_hover(pygame.mouse.get_pos())
            pause_button.handle_event(event)
            speaker_button.check_hover(pygame.mouse.get_pos())
            speaker_button.handle_event(event)
            cross_button.handle_event(event)
            if event.type == pygame.USEREVENT+1:
                if event.button == "pause":
                    isPause = not (isPause)
                    tempfigure, pausefigure = pausefigure, tempfigure
                if event.button == "play":
                    isPause = not (isPause)
                    tempfigure, pausefigure = pausefigure, tempfigure
                if event.button == "speaker":
                    sound = (sound)%3+1
                    if sound == 1:
                        gameplay_music.set_volume(0.2)
                    elif sound == 2:
                        gameplay_music.set_volume(1)
                    elif sound == 3:
                        gameplay_music.set_volume(0)
                if event.button == "cross":
                    with open("./record.txt") as f:
                        record = int(f.readline())
                    if score > record:
                        record = score
                    with open("/record.txt", "w") as f:
                        f.write(str(record) + "\n")
                    running = False
                    pygame.quit()
                    sys.exit()

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
                    isContinue = True
running = False
pygame.quit()
sys.exit()