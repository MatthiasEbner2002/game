from cmath import log
import copy
import math
from random import randint
import os
import curses
import logging
import time
from console.utils import wait_key
import keyboard
#import msvcrt as msv
import getch


class Field:
    def __init__(self, x, y, screen):
        self.item = None
        self.screen = screen
        self.size = Size(x, y)
        self.backup = Backup(self.size)
        self.field = [['.' for i in range(self.size.y)]
                      for j in range(self.size.x)]
        # self._generate_field()

    @classmethod
    def from_terminal_size(cls, screen):
        size = Size.from_terminal_size()
        return cls(size.x, size.y, screen)

    def _generate_field(self):
        if self.item is not None:
            self.item.generate_field()
        else:
            self.backup._generate_field()

    def _clear_field(self):
        self.field = [[j if j != 1 and j != 2 else 0 for j in i]
                      for i in self.field]

    def render(self, screen):
        if self.item is not None:
            self.item.generate_field()
            self.item.render(screen)
        else:
            self.backup.generate_field()
            self.backup.render(screen)

    def run(self, screen):
        if self.item is not None:
            self.item.run(screen)
        else:
            self.backup.run(screen)


class Size:
    def __init__(self, x, y):
        self.x = (1, x)[x >= 1]
        self.y = (1, y)[y >= 1]

    @classmethod
    def from_terminal_size(cls):
        rows, columns = os.popen('stty size', 'r').read().split()
        return cls(int(rows) - 1, int(columns))


class Main_Menu:
    def __init__(self, size):
        self.size = size
        self.running = True
        self.field = [[' ' for i in range(self.size.y)]
                      for j in range(self.size.x)]
        self.item = [
            ' /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\',
            '|#################################################|',
            '|#|                                             |#|',
            '|#|    __________.__                            |#|',
            '|#|    \______   \__| ______ _________.__.      |#|',
            '|#|     |    |  _/  |/  ___//  ___<   |  |      |#|',
            '|#|     |    |   \  |\___ \ \___ \ \___  |      |#|',
            '|#|     |______  /__/____  >____  >/ ____|      |#|',
            '|#|            \/        \/     \/ \/           |#|',
            '|#|                                             |#|',
            '|#|    (P)LAY       (S)ETTINGS       (Q)UIT     |#|',
            '|#|_____________________________________________|#|',
            '|#################################################|',
            ' \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/'
        ]
        self.menu_size_x = 14
        self.menu_size_y = 51
        self.menu = Menu([
            Option(9, 7, 6),
            Option(9, 20, 10),
            Option(9, 37, 6)
        ])
        self._generate_field()

    def _generate_field(self):
        start_x = math.floor((self.size.x - self.menu_size_x) / 2)
        start_y = math.floor((self.size.y - self.menu_size_y) / 2)

        for i in range(self.menu_size_x):
            for j in range(self.menu_size_y):
                self.field[i + start_x][j + start_y] = self.item[i][j]

        aktiv_item = self.menu.option_list[self.menu.aktiv_option]
        for i in range(aktiv_item.lenght):
            self.field[start_x + aktiv_item.x][start_y +
                                               aktiv_item.y + i] = '_'

    def _clear_field(self):
        logging.debug("cleaning")
        # self.field = [[j if j != 1 and j != 2 else 0 for j in i]
        #             for i in self.field]
        # self.field = [[' ' for i in range(self.size.y)]
        #            for j in range(self.size.x)]

    def _move(self, screen):
        ch = screen.getch()
        if ch != -1:
            if ch == curses.KEY_LEFT:
                self.menu.aktiv_option = (
                    self.menu.aktiv_option - 1) % self.menu.anzahl_options
            elif ch == curses.KEY_RIGHT:
                self.menu.aktiv_option = (
                    self.menu.aktiv_option + 1) % self.menu.anzahl_options
            elif ch == 10:  # ENTER
                self._enter(self.menu.aktiv_option, screen)
            elif ch == 112:
                self._enter(0, screen)
            elif ch == 115:
                self._enter(1, screen)
            elif ch == 113:
                self._enter(2, screen)
        return

    def _enter(self, option, screen):
        if option == 0:
            logging.debug("PLAY")
        elif option == 1:
            logging.debug("SETTING")
        elif option == 2:
            logging.debug("QUITING")
            self._shutdown(screen)

    def _shutdown(self, screen):
        size = copy.deepcopy(self.size)
        size.x = size.x - 1
        size.y = size.y
        c1 = '#'
        x, y = 0, 0
        while x <= size.x - x and y <= size.y - y:
            for i in range(y, size.y - y, 1):
                self.field[x][i] = c1
                #self.field[size.x - x][i] = c1
                a = 1
            self._shutdown_render(screen)

            x = x + 1
            y = y + 3
            #self.field[x][y] = '\\'
            #self.field[size.x - x][y] = '/'
            #self.field[x][size.y - y - 1] = '/'
            #self.field[size.x - x][size.y - y - 1] = '\\'
        x, y = 0, 0
        while x <= size.x - x and y <= size.y - y:
            for i in range(x+1, size.x - x, 1):
                #self.field[i][y] = c1
                self.field[i][size.y - y - 1] = c1
                a = 1
            y = y + 1

            for i in range(x+1, size.x - x, 1):
                #self.field[i][y] = c1
                self.field[i][size.y - y - 1] = c1
                a = 1
            y = y + 1

            for i in range(x + 1, size.x - x, 1):
                #self.field[i][y] = c1
                self.field[i][size.y - y - 1] = c1
                a = 1
            y = y + 1
            x = x + 1
            self._shutdown_render(screen)

        x, y = 0, 0
        while x <= size.x - x and y <= size.y - y:
            for i in range(y, size.y - y, 1):
                #self.field[x][i] = c1
                self.field[size.x - x][i] = c1
                a = 1
            self._shutdown_render(screen)

            x = x + 1
            y = y + 3

        x, y = 0, 0
        while x <= size.x - x and y <= size.y - y:
            for i in range(x+1, size.x - x, 1):
                self.field[i][y] = c1
                #self.field[i][size.y - y - 1] = c1
                a = 1
            y = y + 1

            for i in range(x+1, size.x - x, 1):
                self.field[i][y] = c1
                #self.field[i][size.y - y - 1] = c1
                a = 1
            y = y + 1

            for i in range(x + 1, size.x - x, 1):
                self.field[i][y] = c1
                #self.field[i][size.y - y - 1] = c1
                a = 1
            y = y + 1
            x = x + 1
            self._shutdown_render(screen)
        time.sleep(.3)
        quit()

    def _shutdown_render(self, screen):
        self.render(screen)
        screen.refresh()
        time.sleep(0.025)
        return

    def render(self, screen):
        size = self.size
        # self._clear_field()
        for i in range(size.x):
            row = ''
            for j in range(size.y):
                row += self.field[i][j]
            screen.addstr(i, 0, row)

    def run(self, screen):
        while self.running:
            self._generate_field()
            self.render(screen)
            screen.refresh()
            self._move(screen)


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


class Backup:
    def __init__(self, size):
        self.size = size
        self.message = 'no module found!'
        self.field = [[' ' for i in range(self.size.y)]
                      for j in range(self.size.x)]

    def _clear_field(self):
        self.field = [[j if j != 1 and j != 2 else 0 for j in i]
                      for i in self.field]

    def render(self, screen):
        screen.addstr(0, 0, "Error: " + self.message)

    def _generate_field(self):
        logging.error("Generate Field without a item to render!")

    def run(self):
        logging.error("updating without a item to run!")
