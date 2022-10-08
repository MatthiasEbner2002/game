import os
import copy
import time
import curses
import logging


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
    def from_terminal_size(cls, screen):
        rows, columns = screen.getmaxyx()
        return cls(int(rows) - 1, int(columns))

# TODO: make it more efficent

def getColorIndex(x):
    return x % 6 + 1


def shutdown(current_screen, screen):
    size = copy.deepcopy(current_screen.term.size)
    size.x = size.x - 1
    size.y = size.y
    c1 = '#'
    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(y, size.y - y, 1):
            current_screen.field[x][i] = c1
            current_screen.field_color[x][i] = getColorIndex(x)
            #self.field[size.x - x][i] = c1
        shutdown_render(current_screen, screen)

        x = x + 1
        y = y + 3

    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(x+1, size.x - x, 1):
            #self.field[i][y] = c1
            current_screen.field[i][size.y - y - 1] = c1
            current_screen.field_color[i][size.y - y - 1] = getColorIndex(x)
        y = y + 1

        for i in range(x+1, size.x - x, 1):
            #self.field[i][y] = c1
            current_screen.field[i][size.y - y - 1] = c1
            current_screen.field_color[i][size.y - y - 1] = getColorIndex(x)
        y = y + 1

        for i in range(x + 1, size.x - x, 1):
            #self.field[i][y] = c1
            current_screen.field[i][size.y - y - 1] = c1
            current_screen.field_color[i][size.y - y - 1] = getColorIndex(x)
        y = y + 1
        x = x + 1
        shutdown_render(current_screen, screen)

    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(y, size.y - y, 1):
            #self.field[x][i] = c1
            current_screen.field[size.x - x][i] = c1
            current_screen.field_color[size.x - x][i] = getColorIndex(x)
        shutdown_render(current_screen, screen)

        x = x + 1
        y = y + 3

    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(x+1, size.x - x, 1):
            current_screen.field[i][y] = c1
            current_screen.field_color[i][y] = getColorIndex(x)
        y = y + 1

        for i in range(x+1, size.x - x, 1):
            current_screen.field[i][y] = c1
            current_screen.field_color[i][y] = getColorIndex(x)
        y = y + 1

        for i in range(x + 1, size.x - x, 1):
            current_screen.field[i][y] = c1
            current_screen.field_color[i][y] = getColorIndex(x)
        y = y + 1
        x = x + 1
        shutdown_render(current_screen, screen)
    time.sleep(0.3)
    quit()


def shutdown_render(self, screen):
    render(self, screen)
    screen.refresh()
    time.sleep(0.025)
    return


def render(current_screen, screen):
    size = current_screen.term.size
    for i in range(size.x):
        row = ''
        for j in range(size.y):
            #row += current_screen.field[i][j]
            color = curses.color_pair(
                current_screen.field_color[i][j])
            screen.addstr(
                i, j, current_screen.field[i][j], color)

class Player:
    def __init__(self):
        self.x = 10
        self.y = 10
    