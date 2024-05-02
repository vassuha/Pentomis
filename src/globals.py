import pygame
from render import *

screenWidth = 1920-500
screenHeight = 1080-300
areaWidth = 10
areaHeight = 20
TEXTURE_WIDTH = 54
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
gameplay_music = pygame.mixer.Sound("music/Doom Soundtrack.mp3")
gameplay_music.set_volume(0.2)
clock = pygame.time.Clock()

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

blocks = []
blocks.append(pygame.image.load("img/textures/Pentomis_texture_" + str(20) + ".png").convert())
for i in range(1, 22+1):
    blocks.append(pygame.image.load("img/textures/Pentomis_texture_" + str(i) + ".png").convert())

bg = pygame.transform.scale(pygame.image.load("img/backgrounds/Minimalistic_landscape_1.jpg").convert(), (screenWidth, screenHeight))
meshColor = (120, 122, 130)
CloseMenuBg = pygame.transform.scale(pygame.image.load("img/backgrounds/Close_bg.jpg").convert(), (screenWidth, screenHeight))

pauseIcon = pygame.image.load("img/icons/pause.png")
playIcon = pygame.image.load("img/icons/play.png")
crossIcon = pygame.image.load("img/icons/cross.png")
speaker1Icon = pygame.image.load("img/icons/speaker1.png")
speaker2Icon = pygame.image.load("img/icons/speaker2.png")
speakerOffIcon = pygame.image.load("img/icons/speakerOff.png")
playIcon_hovered = pygame.image.load("img/icons/play_large.png")
bgStart = pygame.transform.scale(pygame.image.load("img/backgrounds/Start1.png"), (screenWidth, screenHeight))

cross_button = BoxButton("cross", 100, 0, 100, 100, "", crossIcon)
pause_button = BoxButton("pause", 0, 0, 100, 100, "", pauseIcon)
play_button = BoxButton("play", 100, 0, 100, 100, "", playIcon)
speaker_button = BoxButton("speaker", 100, 0, 100, 100, "", speaker1Icon)
start_button = ImageButton("start", 100, 0, 100, 100, "", playIcon)
sound = 2

