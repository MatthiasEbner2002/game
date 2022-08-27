import os
import copy
import time
import curses


class Menu:
    def __init__(self, option_list=[]):
        self.option_list = option_list
        self.anzahl_options = len(option_list)
        self.aktiv_option = 0


class Option:
    def __init__(self, x, y, lenght):
        self.x = x
        self.y = y
        self.lenght = lenght


class Size:
    def __init__(self, x, y):
        self.x = (1, x)[x >= 1]
        self.y = (1, y)[y >= 1]

    @classmethod
    def from_terminal_size(cls):
        rows, columns = os.popen('stty size', 'r').read().split()
        return cls(int(rows) - 1, int(columns))


def shutdown(current_screen, screen):
    size = copy.deepcopy(current_screen.size)
    size.x = size.x - 1
    size.y = size.y
    c1 = '#'
    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(y, size.y - y, 1):
            current_screen.field[x][i] = c1
            current_screen.field_color[x][i] = x
            #self.field[size.x - x][i] = c1
        shutdown_render(current_screen, screen)

        x = x + 1
        y = y + 3

    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(x+1, size.x - x, 1):
            #self.field[i][y] = c1
            current_screen.field[i][size.y - y - 1] = c1
            current_screen.field_color[i][size.y - y - 1] = x
        y = y + 1

        for i in range(x+1, size.x - x, 1):
            #self.field[i][y] = c1
            current_screen.field[i][size.y - y - 1] = c1
            current_screen.field_color[i][size.y - y - 1] = x
        y = y + 1

        for i in range(x + 1, size.x - x, 1):
            #self.field[i][y] = c1
            current_screen.field[i][size.y - y - 1] = c1
            current_screen.field_color[i][size.y - y - 1] = x
        y = y + 1
        x = x + 1
        shutdown_render(current_screen, screen)

    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(y, size.y - y, 1):
            #self.field[x][i] = c1
            current_screen.field[size.x - x][i] = c1
            current_screen.field_color[size.x - x][i] = x
        shutdown_render(current_screen, screen)

        x = x + 1
        y = y + 3

    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(x+1, size.x - x, 1):
            current_screen.field[i][y] = c1
            current_screen.field_color[i][y] = x
        y = y + 1

        for i in range(x+1, size.x - x, 1):
            current_screen.field[i][y] = c1
            current_screen.field_color[i][y] = x
        y = y + 1

        for i in range(x + 1, size.x - x, 1):
            current_screen.field[i][y] = c1
            current_screen.field_color[i][y] = x
        y = y + 1
        x = x + 1
        shutdown_render(current_screen, screen)
    time.sleep(.3)
    quit()


def shutdown_render(self, screen):
    render(self, screen)
    screen.refresh()
    time.sleep(0.025)
    return


def render(current_screen, screen):
    size = current_screen.size
    for i in range(size.x):
        row = ''
        for j in range(size.y):
            #row += current_screen.field[i][j]
            if current_screen.field_color[i][j] != -1:
                color = curses.color_pair(
                    current_screen.field_color[i][j] % 6 + 1)
                screen.addstr(
                    i, j, current_screen.field[i][j], color)
            else:
                screen.addstr(
                    i, j, current_screen.field[i][j])
