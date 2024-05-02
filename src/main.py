import copy
from random import choice
import sys
import time
import pygame
from figure import figure
from functions import *
from render import *
from globals import *

try:
    f = open("./record.txt")
except FileNotFoundError:
    f = open("./record.txt", "w")
    f.write("0" + "\n")

gameplay = False
while not gameplay:
    screen_width = screen.get_size()[0]
    screen_height = screen.get_size()[1]
    start_menu_buttons = render_start_menu(sound)
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
            is_throwing = False
            while not gameplay:
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP:
                        gameplay = True
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT + 1:
            if event.button == "start":
                gameplay = True
                running = True
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

while running:
    # Создание игрового поля
    area = []
    for i in range(28):
        area.append([0] * 18)
        area[i][3] = 1
        area[i][14] = 1
    area[24] = [1] * 18
    score = 0

    temp_figure = choice(figures)
    next_figure = copy.deepcopy(choice(figures))
    pause_figure = figure("-1", area, [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, (0, 0), "", [1, 1])

    # Стартовое меню

    delta_time = pygame.time.get_ticks()
    time_move = pygame.time.get_ticks()
    is_pause = False
    is_move = False
    temp_figure.spawn(area)
    gameplay_music.play(loops=-1)
    MOVEMENT, T = pygame.USEREVENT, timer(0)
    pygame.time.set_timer(MOVEMENT, T)
    # Игровой процесс
    while gameplay:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            if pygame.time.get_ticks() - time_move > 100:
                temp_figure.move(area, "right")
                time_move = pygame.time.get_ticks()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and is_move == False:
            if pygame.time.get_ticks() - time_move > 100:
                temp_figure.move(area, "left")
                time_move = pygame.time.get_ticks()
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and is_move == False:
            is_move = True
            temp_figure.throw(area)
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and is_move == False:
            temp_figure.rotate(area)
            is_move = True
        if keys[pygame.K_SPACE] and is_move == False:
            is_move = True
            is_pause = not (is_pause)
            temp_figure, pause_figure = pause_figure, temp_figure

        screen_width = screen.get_size()[0]
        screen_height = screen.get_size()[1]
        buttons = render_gameplay(area, score, blocks, next_figure, temp_figure, pygame.time.get_ticks() - delta_time,
                                  is_pause, sound)
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
                if check_collision(area, temp_figure):
                    score = check_line(area, score)
                    if check_end(area):
                        gameplay = False
                    temp_figure = next_figure
                    next_figure = copy.deepcopy(choice(figures))
                    is_throwing = False
                    if not temp_figure.spawn(area):
                        gameplay = False
                temp_figure.move(area, "down")
                MOVEMENT, T = pygame.USEREVENT, timer(score)
                pygame.time.set_timer(MOVEMENT, T)
                delta_time = pygame.time.get_ticks()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    is_move = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    is_move = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    is_move = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    is_move = False
                if event.key == pygame.K_SPACE:
                    is_move = False
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
            if event.type == pygame.USEREVENT + 1:
                if event.button == "pause":
                    is_pause = not (is_pause)
                    temp_figure, pause_figure = pause_figure, temp_figure
                if event.button == "play":
                    is_pause = not (is_pause)
                    temp_figure, pause_figure = pause_figure, temp_figure
                if event.button == "speaker":
                    sound = (sound) % 3 + 1
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

    # Завершающее меню
    gameplay_music.stop()
    is_new_best = False
    with open("./record.txt") as f:
        record = int(f.readline())
    if score > record:
        record = score
        is_new_best = True
    with open("./record.txt", "w") as f:
        f.write(str(record) + "\n")
    while not gameplay:
        screen_width = screen.get_size()[0]
        screen_height = screen.get_size()[1]
        start_menu_buttons = render_end_menu(sound, score, is_new_best)
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
                is_throwing = False
                while not gameplay:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            gameplay = True
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT + 1:
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
running = False
pygame.quit()
sys.exit()
