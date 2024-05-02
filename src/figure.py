import copy


class Figure:
    def __init__(self, name, area, form, rotation_angle, position, color, center):
        self.name = name
        self.form = form
        self.area = area
        self.rotationAngle = rotation_angle
        self.position = [0, 8]
        self.center = center

    def rotate(self, area):
        for i in range(len(self.form)):
            for j in range(len(self.form)):
                if (self.form[i][j] > 0):
                    area[self.position[0] + i][self.position[1] + j] = 0
        temp_form = copy.deepcopy(self.form)
        n = len(temp_form)
        for i in range(len(self.form)):
            for j in range(len(self.form)):
                self.form[i][j] = temp_form[n - j - 1][i]

        center_old = copy.deepcopy(self.center)
        temp = copy.deepcopy(self.center[0])
        self.center[0] = self.center[1]
        self.center[1] = n - temp - 1

        position_old = copy.deepcopy(self.position)

        self.position[0] += -self.center[0] + center_old[0]
        self.position[1] += -self.center[1] + center_old[1]

        for i in range(len(self.form)):
            for j in range(len(self.form)):
                if (area[self.position[0] + i][self.position[1] + j] > 0) and (self.form[i][j] > 0):
                    self.position = copy.deepcopy(position_old)
                    self.form = copy.deepcopy(temp_form)
                    self.center = copy.deepcopy(center_old)
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
                    if (self.form[i][j] > 0):
                        area[self.position[0] + i][self.position[1] + j] = 0
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if ((area[self.position[0] + i][self.position[1] + j + 1] > 0) and (self.form[i][j] > 0)) or (
                            self.form[i][j] > 0 and (self.position[1] + j) > 12):
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
                    if (self.form[i][j] > 0):
                        area[self.position[0] + i][self.position[1] + j] = 0
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if ((area[self.position[0] + i][self.position[1] + j - 1] > 0) and (self.form[i][j] > 0)) or (
                            self.form[i][j] > 0 and (self.position[1] + j) < 5):
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
                    if (self.form[i][j] > 0):
                        area[self.position[0] + i][self.position[1] + j] = 0
            for i in range(len(self.form)):
                for j in range(len(self.form)):
                    if ((area[self.position[0] + i + 1][self.position[1] + j] > 0) and (self.form[i][j] > 0)) or (
                            self.form[i][j] > 0 and (self.position[0] + i) > 22):
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

    def spawn(self, area):
        self.position[1] = len(area[0]) // 2 - len(self.form) // 2
        self.position[0] = 3
        self.rotationAngle = 0
        for i in range(len(self.form)):
            for j in range(len(self.form)):
                if area[self.position[0] + i][self.position[1] + j] == 0:
                    area[self.position[0] + i][self.position[1] + j] = self.form[i][j]
                else:
                    return False
        return True
