from components.other.Classes import Menu, Option, shutdown
import logging
import time
import math
import copy
import curses


class Screen_MainMenu:
    def __init__(self, size):
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
            shutdown(self, screen)

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
