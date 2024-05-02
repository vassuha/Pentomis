import sys
import time
import copy
from random import choice
import pygame
from figure import figure
from button import ImageButton, BoxButton
from globals import *
from functions import checkCollision, timer

def gaussian_blur(surface, radius):
    scaled_surface = pygame.transform.smoothscale(surface, (surface.get_width() // radius, surface.get_height() // radius))
    scaled_surface = pygame.transform.smoothscale(scaled_surface, (surface.get_width(), surface.get_height()))
    return scaled_surface
def renderVoidBox(x, y, width, height, screen):
    screenHeight = screen.get_height()
    global areaHeight
    rounding = screenHeight//36
    border = screenHeight//(270)
    color = meshColor
    area = pygame.Surface((width, height), pygame.SRCALPHA)
    translucentArea = pygame.Surface((width, height), pygame.SRCALPHA)
    translucentArea.set_alpha(200)
    pygame.draw.rect(translucentArea, (0, 0, 0), (0, 0, width, height), height, rounding)
    pygame.draw.rect(translucentArea, color, (0, 0, width, height), border, rounding)
    area.blit(translucentArea, (0, 0))
    screen.blit(area, (x,y))

def renderGameplay(area, score, blocks, nextfigure, tempfigure, deltaTime, isPause, sound):
    global screen
    screenHeight = screen.get_height()
    screenWidth = screen.get_width()
    scoreAreaHeight = screenHeight // 9
    scoreAreaWidth = scoreAreaHeight
    bg1 = pygame.transform.scale(bg, (screenWidth, screenHeight))

    blockHeight = int(screenHeight // areaHeight * 0.9)
    border = screenHeight // (270)

    screen.blit(bg1, (0, 0))  # вывод

    gameplayArea = pygame.Surface((blockHeight * areaWidth + border, blockHeight * (areaHeight + 1) + border // 2),
                                  pygame.SRCALPHA)
    mesh = pygame.Surface((blockHeight * areaWidth + border, blockHeight * (areaHeight + 1) + border // 2),
                          pygame.SRCALPHA)
    mesh.fill((0, 0, 0))
    mesh.set_alpha(200)

    pygame.draw.rect(mesh, meshColor,
                     (0, 0, blockHeight * areaWidth + border, blockHeight * (areaHeight + 1) + border // 2), border)

    for i in range(areaWidth):
        pygame.draw.line(mesh, meshColor, (i * blockHeight, 0), (i * blockHeight, blockHeight * (areaHeight + 1)))
    for i in range(1, areaHeight + 1):
        pygame.draw.line(mesh, meshColor, (0, i * blockHeight), (blockHeight * areaWidth, i * blockHeight))

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
                    gameplayArea.blit(pygame.transform.scale(blocks[tempfigure.form[i][j]], (blockHeight, blockHeight)),
                                      ((j + tempfigure.position[1] - 4) * blockHeight + border // 2,
                                       (i + tempfigure.position[0] - 3) * blockHeight + (
                                                   deltaTime / timer(score)) * blockHeight))
                else:
                    gameplayArea.blit(pygame.transform.scale(blocks[tempfigure.form[i][j]], (blockHeight, blockHeight)),
                                      ((j + tempfigure.position[1] - 4) * blockHeight + border // 2,
                                       (i + tempfigure.position[0] - 3) * blockHeight))
                    pass

    for i in range(3, 24):
        for j in range(4, 14):
            if area1[i][j] > 0:
                gameplayArea.blit(pygame.transform.scale(blocks[area1[i][j]], (blockHeight, blockHeight)),
                                  ((j - 4) * blockHeight + border // 2, (i - 3) * blockHeight))

    if isPause:
        gameplayArea = gaussian_blur(gameplayArea, 50)
    screen.blit(gameplayArea, (screenWidth // 2 - blockHeight * (areaWidth // 2 - 1),
                               screenHeight // 2 - blockHeight * (areaHeight // 2)))

    # Отображение текущего счета

    gameplayFont = pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', screenHeight // 50)
    gameplayFont1 = pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', screenHeight // 20)
    scoreText = gameplayFont.render("SCORE", True, "White")
    scoreText1 = gameplayFont1.render(str(score), True, "White")


    score_area_x = screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) + blockHeight * areaWidth + border * 10
    score_area_y = screenHeight // 2 - blockHeight * (areaHeight // 2)

    renderVoidBox(score_area_x, score_area_y, scoreAreaHeight, scoreAreaHeight, screen)
    screen.blit(scoreText, (score_area_x + screenHeight / 75, score_area_y + screenHeight / 50))
    screen.blit(scoreText1, (score_area_x + screenHeight / 100 - (len(str(score)) - 1) * screenHeight // 50 + screenHeight // 40, score_area_y+ screenHeight / 50 + screenHeight / 50))

    # Отображение следующей детали
    nextfigureAreaHeight = screenHeight // 4
    nextfigureArea = pygame.Surface((nextfigureAreaHeight, nextfigureAreaHeight), pygame.SRCALPHA)

    next_figure_area_x = screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) + blockHeight * areaWidth + border * 10
    next_figure_area_y = screenHeight // 2 - blockHeight * (areaHeight // 2) + scoreAreaHeight + border * 10
    renderVoidBox(next_figure_area_x, next_figure_area_y, nextfigureAreaHeight, nextfigureAreaHeight, screen)

    for i in range(len(nextfigure.form)):
        for j in range(len(nextfigure.form[i])):
            if nextfigure.form[i][j] > 0:
                nextfigureArea.blit(pygame.transform.scale(blocks[nextfigure.form[i][j]], (blockHeight, blockHeight)), (
                j * blockHeight + nextfigureAreaHeight // 2 - len(nextfigure.form) * blockHeight // 2,
                i * blockHeight + nextfigureAreaHeight // 2 - (len(nextfigure.form) + (len(nextfigure.form) - 3) * (
                nextfigure.center[0])) * blockHeight // 2))
    screen.blit(nextfigureArea, (
        screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) + blockHeight * areaWidth + border * 10,
        screenHeight // 2 - blockHeight * (areaHeight // 2) + scoreAreaHeight + border * 10))

    #Отображение кнопки громкости
    global speaker_button

    if sound == 1:
        speaker_button = BoxButton("speaker", screenWidth // 2 - blockHeight * (
                    areaWidth // 2 - 1) - scoreAreaWidth * 2 - border * 10 * 2,
                                   screenHeight // 2 - blockHeight * (areaHeight // 2), scoreAreaHeight,
                                   scoreAreaHeight, "", speaker1Icon)

    if sound == 2:
        speaker_button = BoxButton("speaker", screenWidth // 2 - blockHeight * (
                areaWidth // 2 - 1) - scoreAreaWidth * 2 - border * 10 * 2,
                                   screenHeight // 2 - blockHeight * (areaHeight // 2), scoreAreaHeight,
                                   scoreAreaHeight, "", speaker2Icon)
    if sound == 3:
        speaker_button = BoxButton("speaker", screenWidth // 2 - blockHeight * (
                areaWidth // 2 - 1) - scoreAreaWidth * 2 - border * 10 * 2,
                                   screenHeight // 2 - blockHeight * (areaHeight // 2), scoreAreaHeight,
                                   scoreAreaHeight, "", speakerOffIcon)
    speaker_button.check_hover(pygame.mouse.get_pos())
    speaker_button.draw(screen, areaHeight)

    #Отображение кнопки пауза
    if not isPause:
        global pause_button
        pause_button = BoxButton("pause", screenWidth // 2 - blockHeight * (
                    areaWidth // 2 - 1) + blockHeight * areaWidth + border * 10 + scoreAreaHeight + border * 10,
                                 screenHeight // 2 - blockHeight * (areaHeight // 2), scoreAreaHeight, scoreAreaHeight,
                                 "", pauseIcon)
        pause_button.check_hover(pygame.mouse.get_pos())
        pause_button.draw(screen, areaHeight)
    else:
        global play_button
        play_button = BoxButton("play", screenWidth // 2 - blockHeight * (
                areaWidth // 2 - 1) + blockHeight * areaWidth + border * 10 + scoreAreaHeight + border * 10,
                                screenHeight // 2 - blockHeight * (areaHeight // 2), scoreAreaHeight, scoreAreaHeight,
                                "", playIcon)
        play_button.check_hover(pygame.mouse.get_pos())
        play_button.draw(screen, areaHeight)

    # Отображение кнопки закрыть
    global cross_button
    cross_button = BoxButton("cross",
                             screenWidth // 2 - blockHeight * (areaWidth // 2 - 1) - scoreAreaWidth - border * 10,
                             screenHeight // 2 - blockHeight * (areaHeight // 2), scoreAreaHeight, scoreAreaHeight,
                             "", crossIcon)
    cross_button.check_hover(pygame.mouse.get_pos())
    cross_button.draw(screen, areaHeight)
    pygame.display.update()
    buttons = [speaker_button, pause_button, play_button, cross_button]
    return buttons


def renderStartMenu(sound):
    global bgStart, playIcon_hovered, crossIcon
    screenHeight = screen.get_height()
    screenWidth = screen.get_width()
    border = screenHeight // (270)
    scoreAreaHeight = screenHeight // 9
    background1 = pygame.transform.scale((bgStart), (screenWidth, screenHeight))
    screen.blit(background1, (0, 0))
    squareWidth = screenWidth // 5

    renderVoidBox(screenWidth // 2 - squareWidth // 2, screenHeight // 2 - squareWidth // 2, squareWidth, squareWidth,
                  screen)

    startFont = pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', squareWidth // 7)
    startText = startFont.render("Pentomis", True, "White")
    screen.blit(startText,
                (screenWidth // 2 - squareWidth // 2 * 0.95, screenHeight // 2 - squareWidth // 2 + squareWidth // 9))

    # Отображение кнопки старт
    global start_button

    if start_button.check_hover(pygame.mouse.get_pos()):
        start_button = ImageButton("start", screenWidth // 2 - squareWidth // 2 * 0.45,
                                   screenHeight // 2 - squareWidth // 2 * 0.35, squareWidth // 2, squareWidth // 2, "",
                                   playIcon_hovered)
    else:
        start_button = ImageButton("start", screenWidth // 2 - squareWidth // 2 * 0.45,
                                   screenHeight // 2 - squareWidth // 2 * 0.35, squareWidth // 2, squareWidth // 2, "",
                                   playIcon)

    start_button.draw(screen)

    # Отображение кнопки громкости
    global speaker_button

    if sound == 1:
        speaker_button = BoxButton("speaker", screenWidth // 2 - squareWidth // 2 - scoreAreaHeight - border * 10,
                                   screenHeight // 2 - squareWidth // 2, scoreAreaHeight,
                                   scoreAreaHeight, "", speaker1Icon)

    if sound == 2:
        speaker_button = BoxButton("speaker", screenWidth // 2 - squareWidth // 2 - scoreAreaHeight - border * 10,
                                   screenHeight // 2 - squareWidth // 2, scoreAreaHeight,
                                   scoreAreaHeight, "", speaker2Icon)
    if sound == 3:
        speaker_button = BoxButton("speaker", screenWidth // 2 - squareWidth // 2 - scoreAreaHeight - border * 10,
                                   screenHeight // 2 - squareWidth // 2, scoreAreaHeight,
                                   scoreAreaHeight, "", speakerOffIcon)
    speaker_button.check_hover(pygame.mouse.get_pos())
    speaker_button.draw(screen, areaHeight)

    # Отображение кнопки закрыть
    global cross_button

    cross_button = BoxButton("cross",
                             screenWidth // 2 - squareWidth // 2 + squareWidth + border * 10,
                             screenHeight // 2 - squareWidth // 2, scoreAreaHeight, scoreAreaHeight,
                             "", crossIcon)
    cross_button.check_hover(pygame.mouse.get_pos())
    cross_button.draw(screen, areaHeight)

    pygame.display.update()
    start_menu_buttons = [start_button, speaker_button, cross_button]
    return start_menu_buttons