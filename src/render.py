import copy
from random import choice
from math import sin
import sys
import time
import pygame
from button import *
from figure import Figure
from functions import check_collision, timer
from globals import *


def gaussian_blur(surface, radius):
    scaled_surface = pygame.transform.smoothscale(surface,
                                                  (surface.get_width() // radius, surface.get_height() // radius))
    scaled_surface = pygame.transform.smoothscale(scaled_surface, (surface.get_width(), surface.get_height()))
    return scaled_surface


def render_void_box(x, y, width, height, screen):
    screen_height = screen.get_height()
    global AREA_HEIGHT
    rounding = screen_height // 36
    border = screen_height // 270
    color = mesh_color
    area = pygame.Surface((width, height), pygame.SRCALPHA)
    translucent_area = pygame.Surface((width, height), pygame.SRCALPHA)
    translucent_area.set_alpha(200)
    pygame.draw.rect(translucent_area, (0, 0, 0), (0, 0, width, height), height, rounding)
    pygame.draw.rect(translucent_area, color, (0, 0, width, height), border, rounding)
    area.blit(translucent_area, (0, 0))
    screen.blit(area, (x, y))


def render_gameplay(area, score, blocks, next_figure, temp_figure, delta_time, is_pause, sound, delete_lines,
                    time_delete, throwing, bounce_time):
    global screen
    screen_height = screen.get_height()
    screen_width = screen.get_width()
    score_area_height = screen_height // 9
    score_area_width = score_area_height
    bg1 = pygame.transform.scale(bg, (screen_width, screen_height))

    block_height = int(screen_height // AREA_HEIGHT * 0.9)
    border = screen_height // 270

    screen.blit(bg1, (0, 0))

    gameplay_area = pygame.Surface((block_height * AREA_WIDTH + border, block_height * (AREA_HEIGHT + 1) + border // 2),
                                   pygame.SRCALPHA)
    mesh = pygame.Surface((block_height * AREA_WIDTH + border, block_height * (AREA_HEIGHT + 1) + border // 2),
                          pygame.SRCALPHA)
    mesh.fill((0, 0, 0))
    mesh.set_alpha(200)

    pygame.draw.rect(mesh, mesh_color,
                     (0, 0, block_height * AREA_WIDTH + border, block_height * (AREA_HEIGHT + 1) + border // 2), border)

    for i in range(AREA_WIDTH):
        pygame.draw.line(mesh, mesh_color, (i * block_height, 0), (i * block_height, block_height * (AREA_HEIGHT + 1)))
    for i in range(1, AREA_HEIGHT + 1):
        pygame.draw.line(mesh, mesh_color, (0, i * block_height), (block_height * AREA_WIDTH, i * block_height))

    gameplay_area.blit(mesh, (0, 0))

    if throwing:
        gameplay_area.blit(pygame.transform.scale(trail_texture, (
            block_height * len(temp_figure.form[0]), (temp_figure.position[0] - throwing) * block_height)),
                           ((temp_figure.position[1] - 4) * block_height + border // 2,
                            (throwing + len(temp_figure.form) / 2 - 3) * block_height))

    area1 = copy.deepcopy(area)
    for i in range(len(temp_figure.form)):
        for j in range(len(temp_figure.form)):
            if (temp_figure.form[i][j] > 0):
                area1[temp_figure.position[0] + i][temp_figure.position[1] + j] = 0

    for i in range(len(temp_figure.form[0])):
        for j in range(len(temp_figure.form[1])):
            if temp_figure.form[i][j] != 0:
                if not check_collision(area, temp_figure):
                    gameplay_area.blit(
                        pygame.transform.scale(blocks[temp_figure.form[i][j]], (block_height, block_height)),
                        ((j + temp_figure.position[1] - 4) * block_height + border // 2,
                         (i + temp_figure.position[0] - 3) * block_height + (
                                 delta_time / timer(score)) * block_height))
                else:
                    gameplay_area.blit(
                        pygame.transform.scale(blocks[temp_figure.form[i][j]], (block_height, block_height)),
                        ((j + temp_figure.position[1] - 4) * block_height + border // 2,
                         (i + temp_figure.position[0] - 3) * block_height))
                    pass

    for i in range(3, 24):
        for j in range(4, 14):
            if area1[i][j] > 0:
                gameplay_area.blit(pygame.transform.scale(blocks[area1[i][j]], (block_height, block_height)),
                                   ((j - 4) * block_height + border // 2, (i - 3) * block_height))

    for i in range(len(delete_lines)):
        if delete_lines[i] == 1 and time_delete / timer(score) < 1:
            delete_line_area = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            delete_line_area.set_alpha(max(256 - time_delete * 2 / timer(score) * 256, 0))
            delete_line_area.blit(
                pygame.transform.scale(delite_line_texture, (block_height * AREA_WIDTH, block_height)),
                (border // 2, (i - 3) * block_height))
            gameplay_area.blit(delete_line_area, (0, 0))

    if is_pause:
        gameplay_area = gaussian_blur(gameplay_area, 50)
    if bounce_time >= 0:
        bounce_time = pygame.time.get_ticks() - bounce_time
        screen.blit(gameplay_area, (screen_width // 2 - block_height * (AREA_WIDTH // 2 - 1),
                                    screen_height // 2 - block_height * (AREA_HEIGHT // 2) + border * 1.5 * (
                                        sin(3.1415 * (bounce_time / (timer(score) / 3)))) ** 2))
    else:
        screen.blit(gameplay_area, (screen_width // 2 - block_height * (AREA_WIDTH // 2 - 1),
                                    screen_height // 2 - block_height * (AREA_HEIGHT // 2)))

    # Отображение текущего счета

    gameplay_font = pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', screen_height // 50)
    gameplay_font_1 = pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', screen_height // 20)
    score_text = gameplay_font.render("SCORE", True, "White")
    score_text_1 = gameplay_font_1.render(str(score), True, "White")

    score_area_x = screen_width // 2 - block_height * (AREA_WIDTH // 2 - 1) + block_height * AREA_WIDTH + border * 10
    score_area_y = screen_height // 2 - block_height * (AREA_HEIGHT // 2)

    render_void_box(score_area_x, score_area_y, score_area_height, score_area_height, screen)
    screen.blit(score_text, (score_area_x + screen_height / 75, score_area_y + screen_height / 50))
    screen.blit(score_text_1, (
        score_area_x + screen_height / 100 - (len(str(score)) - 1) * screen_height // 50 + screen_height // 40,
        score_area_y + screen_height / 50 + screen_height / 50))

    # Отображение следующей детали
    nextfigureAreaHeight = screen_height // 4
    nextfigureArea = pygame.Surface((nextfigureAreaHeight, nextfigureAreaHeight), pygame.SRCALPHA)

    next_figure_area_x = screen_width // 2 - block_height * (
            AREA_WIDTH // 2 - 1) + block_height * AREA_WIDTH + border * 10
    next_figure_area_y = screen_height // 2 - block_height * (AREA_HEIGHT // 2) + score_area_height + border * 10
    render_void_box(next_figure_area_x, next_figure_area_y, nextfigureAreaHeight, nextfigureAreaHeight, screen)

    for i in range(len(next_figure.form)):
        for j in range(len(next_figure.form[i])):
            if next_figure.form[i][j] > 0:
                nextfigureArea.blit(
                    pygame.transform.scale(blocks[next_figure.form[i][j]], (block_height, block_height)), (
                        j * block_height + nextfigureAreaHeight // 2 - len(next_figure.form) * block_height // 2,
                        i * block_height + nextfigureAreaHeight // 2 - (
                                len(next_figure.form) + (len(next_figure.form) - 3) * (
                            next_figure.center[0])) * block_height // 2))
    screen.blit(nextfigureArea, (
        screen_width // 2 - block_height * (AREA_WIDTH // 2 - 1) + block_height * AREA_WIDTH + border * 10,
        screen_height // 2 - block_height * (AREA_HEIGHT // 2) + score_area_height + border * 10))

    # Отображение кнопки громкости
    global speaker_button

    if sound == 1:
        speaker_button = BoxButton("speaker", screen_width // 2 - block_height * (
                AREA_WIDTH // 2 - 1) - score_area_width * 2 - border * 10 * 2,
                                   screen_height // 2 - block_height * (AREA_HEIGHT // 2), score_area_height,
                                   score_area_height, "", speaker1_icon)

    if sound == 2:
        speaker_button = BoxButton("speaker", screen_width // 2 - block_height * (
                AREA_WIDTH // 2 - 1) - score_area_width * 2 - border * 10 * 2,
                                   screen_height // 2 - block_height * (AREA_HEIGHT // 2), score_area_height,
                                   score_area_height, "", speaker2_icon)
    if sound == 3:
        speaker_button = BoxButton("speaker", screen_width // 2 - block_height * (
                AREA_WIDTH // 2 - 1) - score_area_width * 2 - border * 10 * 2,
                                   screen_height // 2 - block_height * (AREA_HEIGHT // 2), score_area_height,
                                   score_area_height, "", speaker_off_icon)
    speaker_button.check_hover(pygame.mouse.get_pos())
    speaker_button.draw(screen, AREA_HEIGHT)

    # Отображение кнопки пауза
    global pause_button
    global play_button
    if not is_pause:
        pause_button = BoxButton("pause", screen_width // 2 - block_height * (
                AREA_WIDTH // 2 - 1) + block_height * AREA_WIDTH + border * 10 + score_area_height + border * 10,
                                 screen_height // 2 - block_height * (AREA_HEIGHT // 2), score_area_height,
                                 score_area_height,
                                 "", pause_icon)
        pause_button.check_hover(pygame.mouse.get_pos())
        pause_button.draw(screen, AREA_HEIGHT)
    else:

        play_button = BoxButton("play", screen_width // 2 - block_height * (
                AREA_WIDTH // 2 - 1) + block_height * AREA_WIDTH + border * 10 + score_area_height + border * 10,
                                screen_height // 2 - block_height * (AREA_HEIGHT // 2), score_area_height,
                                score_area_height,
                                "", play_icon)
        play_button.check_hover(pygame.mouse.get_pos())
        play_button.draw(screen, AREA_HEIGHT)

    # Отображение кнопки закрыть
    global cross_button
    cross_button = BoxButton("cross",
                             screen_width // 2 - block_height * (AREA_WIDTH // 2 - 1) - score_area_width - border * 10,
                             screen_height // 2 - block_height * (AREA_HEIGHT // 2), score_area_height,
                             score_area_height,
                             "", cross_icon)
    cross_button.check_hover(pygame.mouse.get_pos())
    cross_button.draw(screen, AREA_HEIGHT)
    pygame.display.update()
    buttons = [speaker_button, pause_button, play_button, cross_button]
    return buttons


def render_start_menu(sound):
    global bg_start, play_icon_hovered, cross_icon
    screen_height = screen.get_height()
    screen_width = screen.get_width()
    border = screen_height // 270
    score_area_height = screen_height // 9
    background1 = pygame.transform.scale((bg_start), (screen_width, screen_height))
    screen.blit(background1, (0, 0))
    square_width = screen_height // 3

    render_void_box(screen_width // 2 - square_width // 2, screen_height // 2 - square_width // 2, square_width,
                    square_width,
                    screen)

    start_font = pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', square_width // 7)
    start_text = start_font.render("Pentomis", True, "White")
    screen.blit(start_text,
                (screen_width // 2 - square_width // 2 * 0.95,
                 screen_height // 2 - square_width // 2 + square_width // 9))

    # Отображение кнопки старт
    global start_button

    if start_button.check_hover(pygame.mouse.get_pos()):
        start_button = ImageButton("start", screen_width // 2 - square_width // 2 * 0.45,
                                   screen_height // 2 - square_width // 2 * 0.35, square_width // 2, square_width // 2,
                                   "",
                                   play_icon_hovered)
    else:
        start_button = ImageButton("start", screen_width // 2 - square_width // 2 * 0.45,
                                   screen_height // 2 - square_width // 2 * 0.35, square_width // 2, square_width // 2,
                                   "",
                                   play_icon)

    start_button.draw(screen)

    # Отображение кнопки громкости
    global speaker_button

    if sound == 1:
        speaker_button = BoxButton("speaker", screen_width // 2 - square_width // 2 - score_area_height - border * 10,
                                   screen_height // 2 - square_width // 2, score_area_height,
                                   score_area_height, "", speaker1_icon)

    if sound == 2:
        speaker_button = BoxButton("speaker", screen_width // 2 - square_width // 2 - score_area_height - border * 10,
                                   screen_height // 2 - square_width // 2, score_area_height,
                                   score_area_height, "", speaker2_icon)
    if sound == 3:
        speaker_button = BoxButton("speaker", screen_width // 2 - square_width // 2 - score_area_height - border * 10,
                                   screen_height // 2 - square_width // 2, score_area_height,
                                   score_area_height, "", speaker_off_icon)
    speaker_button.check_hover(pygame.mouse.get_pos())
    speaker_button.draw(screen, AREA_HEIGHT)

    # Отображение кнопки закрыть
    global cross_button
    cross_button = BoxButton("cross",
                             screen_width // 2 - square_width // 2 + square_width + border * 10,
                             screen_height // 2 - square_width // 2, score_area_height, score_area_height,
                             "", cross_icon)
    cross_button.check_hover(pygame.mouse.get_pos())
    cross_button.draw(screen, AREA_HEIGHT)

    pygame.display.update()
    start_menu_buttons = [start_button, speaker_button, cross_button]
    return start_menu_buttons


def render_end_menu(sound, score, is_new_best, record):
    global bg_end, play_icon_hovered, cross_icon
    screen_height = screen.get_height()
    screen_width = screen.get_width()
    border = screen_height // 270
    score_area_height = screen_height // 9
    background1 = pygame.transform.scale((bg_end), (screen_width, screen_height))
    screen.blit(background1, (0, 0))
    square_width = screen_height // 3

    render_void_box(screen_width // 2 - square_width // 2, screen_height // 2 - square_width // 2, square_width,
                    square_width,
                    screen)

    start_font = pygame.font.Font('fonts/RubikMonoOne-Regular.ttf', square_width // 8)
    if not is_new_best:
        start_text = []
        start_text.append(start_font.render("score "+str(score), True, "White"))
        start_text.append(start_font.render("best "+ str(record), True, "White"))
        screen.blit(start_text[0],
                    (screen_width // 2 - square_width // 2  * 0.105 * (len(str(score))+6),
                     screen_height // 2 - square_width // 2 + square_width // 18))
        screen.blit(start_text[1],
                    (screen_width // 2 - square_width // 2 * 0.105 * (len(str(record))+5),
                     screen_height // 2 - square_width // 2 + square_width // 18 + square_width // 5))

    else:
        start_text = []
        start_text.append(start_font.render("New", True, "White"))
        start_text.append(start_font.render("record!", True, "White"))
        start_text.append(start_font.render(str(score), True, "White"))
        screen.blit(start_text[0],
                    (screen_width // 2 - square_width // 2 * 0.35,
                     screen_height // 2 - square_width // 2 + square_width // 18))
        screen.blit(start_text[1],
                    (screen_width // 2 - square_width // 2 * 0.7,
                     screen_height // 2 - square_width // 2 + square_width // 18 + square_width // 8))
        screen.blit(start_text[2],
                    (screen_width // 2 - square_width // 2 * 0.1 * len(str(score)),
                     screen_height // 2 - square_width // 2 + square_width // 18 + square_width // 4))
    # Отображение кнопки старт
    global start_button

    if start_button.check_hover(pygame.mouse.get_pos()):
        start_button = ImageButton("start", screen_width // 2 - square_width // 2 * 0.45,
                                   screen_height // 2 - square_width // 2 * 0.35 + square_width // 7, square_width // 2,
                                   square_width // 2,
                                   "",
                                   play_icon_hovered)
    else:
        start_button = ImageButton("start", screen_width // 2 - square_width // 2 * 0.45,
                                   screen_height // 2 - square_width // 2 * 0.35 + square_width // 7, square_width // 2,
                                   square_width // 2,
                                   "",
                                   play_icon)

    start_button.draw(screen)

    # Отображение кнопки громкости
    global speaker_button

    if sound == 1:
        speaker_button = BoxButton("speaker", screen_width // 2 - square_width // 2 - score_area_height - border * 10,
                                   screen_height // 2 - square_width // 2, score_area_height,
                                   score_area_height, "", speaker1_icon)

    if sound == 2:
        speaker_button = BoxButton("speaker", screen_width // 2 - square_width // 2 - score_area_height - border * 10,
                                   screen_height // 2 - square_width // 2, score_area_height,
                                   score_area_height, "", speaker2_icon)
    if sound == 3:
        speaker_button = BoxButton("speaker", screen_width // 2 - square_width // 2 - score_area_height - border * 10,
                                   screen_height // 2 - square_width // 2, score_area_height,
                                   score_area_height, "", speaker_off_icon)
    speaker_button.check_hover(pygame.mouse.get_pos())
    speaker_button.draw(screen, AREA_HEIGHT)

    # Отображение кнопки закрыть
    global cross_button

    cross_button = BoxButton("cross",
                             screen_width // 2 - square_width // 2 + square_width + border * 10,
                             screen_height // 2 - square_width // 2, score_area_height, score_area_height,
                             "", cross_icon)
    cross_button.check_hover(pygame.mouse.get_pos())
    cross_button.draw(screen, AREA_HEIGHT)

    pygame.display.update()
    start_menu_buttons = [start_button, speaker_button, cross_button]
    return start_menu_buttons
