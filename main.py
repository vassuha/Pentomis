import sys

import pygame
import time

pygame.init()
screen = pygame.display.set_mode((1920, 1080))

class Figure:
    def __init__(self, name, form, rotationAngle, position, color):
        self.name = name
        self.form = form
        self.rotationAngle = rotationAngle
        self.position = [0, 0]

    def rotate(self, side):
        self.rotationAngle = (self.rotationAngle)%4+(1*side)

        form_temp = self.form
        n = len(self.form[0])
        for i in range(n):
            for j in range(n):
                if side > 0:
                    self.form[i][j] = form_temp[j][n-i]
                else:
                    self.form[i][j] = form_temp[n - j][i]

    def throw(self):
        pass

def spawn(area, figure, pos):
    figure.position = pos
    figure.rotationAngle = 0
    for i in range(len(figure.form)):
        for j in range(len(figure.form)):
            area[figure.position[0] + i][figure.position[1] + j] = figure.form[i][j]
def move(area, figure, dir):
    if dir == "right":
        if figure.position[1] + len(figure.form)+1 > len(area[0]):
            return False
        print(figure.position)
        for i in range(len(figure.form)):
            for j in range(len(figure.form)):
                area[figure.position[0] + i][figure.position[1] + j] = 0
        isCorrect = True
        for i in range(len(figure.form)):
            for j in range(len(figure.form)):
                area[figure.position[0] + i][figure.position[1] + j+1] += figure.form[i][j]
                if area[figure.position[0] + i][figure.position[1] + j+1] > 1:
                    return False
        figure.position[1] += 1


blueForm = [[0, 0, 0], [1, 0, 0], [1, 1, 1]]
blueFigure = Figure('blue', blueForm, 0, (0, 0), "blue")
clock = pygame.time.Clock()



running = True
area = []
for i in range(20):
    area.append([0] * 10)

screen.fill('Yellow')

spawn(area, blueFigure, [0, 0])

myFont = pygame.font.SysFont('Arial', 20)
text1 = [0]*20
for i in range(20):
    text1[i] = myFont.render(str(area[i]), True, "Red")

isMove = False

while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and isMove==False:
        isMove = True
        screen.fill("Yellow")
        pygame.display.update()
        move(area, blueFigure, "right")
        pygame.display.update()
        time.sleep(0.1);
        isMove=False



    pygame.display.update()
    for i in range(20):
        text1[i] = myFont.render(str(area[i]), True, "Red")
        screen.blit(text1[i], (0, 0+i*20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            pygame.quit()
            sys.exit()


