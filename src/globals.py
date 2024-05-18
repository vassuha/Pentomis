import pygame
from render import *
from button import ImageButton, BoxButton
from figure import Figure

screen_width = 1920 - 500
screen_height = 1080 - 300
AREA_WIDTH = 10
AREA_HEIGHT = 20
TEXTURE_WIDTH = 54
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
gameplay_music = pygame.mixer.Sound("music/Tetris_soundtrack.mp3")
gameplay_music.set_volume(1)
clock = pygame.time.Clock()

area = []
for i in range(28):
    area.append([0] * 18)
    area[i][3] = 1
    area[i][14] = 1
area[24] = [1] * 18

figures = []
# figures.append(figure("", area, [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, (0, 0), "", [, ]))
figures.append(Figure("1", area, [[0, 0, 0], [1, 1, 0], [0, 1, 1]], 0, (0, 0), "red", [1, 1]))
figures.append(Figure("2", area, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 2, 2, 2]], 0, (0, 0), "", [3, 2]))
figures.append(Figure("3", area, [[0, 0, 0], [3, 0, 0], [3, 3, 3]], 0, (0, 0), "", [2, 1]))
figures.append(Figure("4", area, [[0, 0, 0], [0, 0, 4], [4, 4, 4]], 0, (0, 0), "orange", [2, 1]))
figures.append(Figure("5", area, [[0, 0, 0], [5, 5, 0], [5, 5, 0]], 0, (0, 0), "", [1, 1]))
figures.append(Figure("6", area, [[0, 0, 0], [0, 6, 6], [6, 6, 0]], 0, (0, 0), "", [1, 1]))
figures.append(Figure("7", area, [[0, 0, 0], [0, 7, 0], [7, 7, 7]], 0, (0, 0), "", [2, 1]))
figures.append(Figure("8", area, [[8, 0], [8, 8]], 0, (0, 0), "", [1, 0]))
figures.append(Figure("9", area, [[9, 9, 0], [0, 9, 9], [0, 9, 0]], 0, (0, 0), "", [1, 1]))
figures.append(Figure("10", area, [[0, 0, 0, 0], [0, 0, 0, 0], [10, 10, 0, 0], [0, 10, 10, 10]], 0, (0, 0), "", [2, 1]))
figures.append(Figure("11", area, [[0, 11, 11], [11, 11, 0], [0, 11, 0]], 0, (0, 0), "", [1, 1]))
figures.append(Figure("12", area, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 12, 12], [12, 12, 12, 0]], 0, (0, 0), "", [3, 2]))
figures.append(
    Figure("13", area, [[0, 0, 0], [0, 0, 0], [13, 13, 13]], 0,(0, 0), "", [2, 1]))
figures.append(Figure("14", area, [[0, 0, 0], [14, 0, 14], [14, 14, 14]], 0, (0, 0), "", [2, 1]))
# figures.append(figure("15", area, [[0, 15, 0], [15, 15, 15], [0, 15, 0]], 0, (0, 0), "", [1, 1]))
figures.append(Figure("16", area, [[16, 16, 16], [0, 16, 0], [0, 16, 0]], 0, (0, 0), "", [1, 1]))
figures.append(Figure("17", area, [[17, 0, 0], [17, 17, 0], [17, 17, 0]], 0, (0, 0), "", [1, 0]))
# figures.append(figure("18", area, [[18, 0, 0], [18, 0, 0], [18, 18, 18]], 0, (0, 0), "", [1, 1]))
figures.append(Figure("19", area, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 19, 0], [19, 19, 19, 19]], 0, (0, 0), "", [3, 2]))
# figures.append(figure("20", area, [[0, 20, 20], [0, 20, 0], [20, 20, 0]], 0, (0, 0), "", [1, 1]))
figures.append(Figure("21", area, [[0, 21, 0], [21, 21, 0], [21, 21, 0]], 0, (0, 0), "", [1, 1]))
figures.append(Figure("22", area, [[0, 0, 0, 0], [0, 0, 0, 0], [22, 22, 22, 22], [0, 0, 22, 0]], 0, (0, 0), "", [2, 2]))

bg_color = 'Black'
my_font = pygame.font.SysFont('Arial', 20)

blocks = []
blocks.append(pygame.image.load("img/textures/Pentomis_texture_" + str(20) + ".png").convert())
for i in range(1, 22 + 1):
    blocks.append(pygame.image.load("img/textures/Pentomis_texture_" + str(i) + ".png").convert())

bg = pygame.transform.scale(pygame.image.load("img/backgrounds/Minimalistic_landscape_1.jpg").convert(),
                            (screen_width, screen_height))
mesh_color = (120, 122, 130)

delite_line_texture = pygame.image.load("img/textures/Delite_line_texture.png")
trail_texture = pygame.image.load("img/textures/Trail.png")
pause_icon = pygame.image.load("img/icons/pause.png")
play_icon = pygame.image.load("img/icons/play.png")
cross_icon = pygame.image.load("img/icons/cross.png")
speaker1_icon = pygame.image.load("img/icons/speaker1.png")
speaker2_icon = pygame.image.load("img/icons/speaker2.png")
speaker_off_icon = pygame.image.load("img/icons/speakerOff.png")
play_icon_hovered = pygame.image.load("img/icons/play_large.png")
bg_start = pygame.transform.scale(pygame.image.load("img/backgrounds/Start1.png"), (screen_width, screen_height))
bg_end = pygame.transform.scale(pygame.image.load("img/backgrounds/Close_bg.jpg").convert(),
                                (screen_width, screen_height))

cross_button = BoxButton("cross", 100, 0, 100, 100, "", cross_icon)
pause_button = BoxButton("pause", 0, 0, 100, 100, "", pause_icon)
play_button = BoxButton("play", 100, 0, 100, 100, "", play_icon)
speaker_button = BoxButton("speaker", 100, 0, 100, 100, "", speaker1_icon)
start_button = ImageButton("start", 100, 0, 100, 100, "", play_icon)
sound = 2
