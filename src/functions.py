def check_collision(area, figure):
    for i in range(len(figure.form)):
        for j in range(len(figure.form)):
            if figure.form[i][j] > 0 and area[figure.position[0] + i + 1][figure.position[1] + j] > 0:
                if i < len(figure.form) - 1:
                    if figure.form[i + 1][j] == 0:
                        return True
                else:
                    return True
    return False


def check_line(area, score):
    lines = [0] * 28
    for i in range(3, 24):
        is_line = True
        for j in range(4, 14):
            if area[i][j] == 0:
                is_line = False
        if is_line:
            lines[i] = 1
    for k in range(3, 24):
        if lines[k] == 1:
            for i in range(k, 3, -1):
                area[i] = area[i - 1]
            area[3] = [0] * 18
            area[3][3] = 1
            area[3][14] = 1
    score += sum(lines[3:24])
    return score, lines


def check_end(area):
    for j in range(4, 14):
        if area[4][j] > 0:
            return True


def timer(score=0):
    t = 900 - score * 10
    if t < 75:
        t = 75
    return t
