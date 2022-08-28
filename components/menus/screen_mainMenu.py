from curses.ascii import isdigit
from components.other.Classes import Menu, Option, shutdown
import logging
import time
import math
import copy
import curses


class Screen_MainMenu:
    def __init__(self, size):
        self.menu_size_x = 14
        self.menu_size_y = 51
        self.size = size
        self.running = True
        self.field = [[' ' for i in range(self.size.y)]
                      for j in range(self.size.x)]
        self.field_color = [[-1 for i in range(self.size.y)]
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
        self.item_color_raw_2 = [
            [-1, -1, -1, ],
            []
        ]

        self.item_color_raw = [
            ' /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\',
            '|#################################################|',
            '|#|                                             |#|',
            '|#|    1111111111122                            |#|',
            '|#|    1111111   1222 333333 4444445555555      |#|',
            '|#|     1    1  11  23  33334  4445   5  5      |#|',
            '|#|     1    1   1  23333 3 4444 4 5555  5      |#|',
            '|#|     1111111  12223333  34444  45 55555      |#|',
            '|#|            11        33     44 55           |#|',
            '|#|                                             |#|',
            '|#|    (P)LAY       (S)ETTINGS       (Q)UIT     |#|',
            '|#|_____________________________________________|#|',
            '|#################################################|',
            ' \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/'
        ]
        self.item_color = [[-1 for i in range(self.menu_size_y)]
                           for j in range(self.menu_size_x)]

        for i in range(self.menu_size_x):
            for j in range(self.menu_size_y):
                if isdigit(self.item_color_raw[i][j]) and int(self.item_color_raw[i][j]) <= 6 and int(self.item_color_raw[i][j]) >= 1:
                    self.item_color[i][j] = self.item_color_raw[i][j]

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
                self.field_color[i + start_x][j + start_y] = int(self.item_color[i][j])

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
            shutdown(self, screen)

    def render(self, screen):
        size = self.size
        # self._clear_field()
        for i in range(size.x):
            for j in range(size.y):
                color = curses.color_pair(self.field_color[i][j])
                screen.addstr(i, j, self.field[i][j], color)

    def run(self, screen):
        while self.running:
            self._generate_field()
            self.render(screen)
            screen.refresh()
            self._move(screen)
