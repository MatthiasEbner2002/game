from datetime import datetime
from distutils.log import debug
import time
from components.other.ClassesLvl2 import shutdown, Size, Attack2, Input, Player, Enemy, EnemySpawn
import logging
import curses
import keyboard
from threading import Lock
mutex_x = Lock()
mutex_y = Lock()

class Level_Default:
    def __init__(self, term, screen, player=None, blank_field=None) -> None:
        self.term = term
        self.size_x = 100
        self.size_y = 100
        if blank_field != None:
            self.size_y = len(blank_field[0]) - 1
            self.size_x = len(blank_field)
        self.actual_position_x = 0
        self.actual_position_y = 0
        self.player = player
        self.screen = screen
        self.running = True
        self.terminal_size = Size.from_terminal_size(screen=self.screen)
        self.terminal_size.x -= 10
        self.origin = Size(1, 1)
        self.terminal_size_real_x = self.terminal_size.x + 10
        self.blank_field = blank_field
        if self.blank_field == None:
            self.blank_field = self._getStartField()
        self.field =  [[' ' for i in range(self.size_y + 1 if self.size_y + 1 > self.terminal_size.y else self.terminal_size.y)]
                           for j in range(self.size_x + 1 if self.size_x + 1 > self.terminal_size_real_x else self.terminal_size_real_x)]
        self._addCloseFunction()
    
    @classmethod
    def from_txt(self, term, screen, player, path):
        file1 = open(path, 'r')
        Lines = file1.readlines()
        lvl_array = list(Lines)
        logging.debug("size_x: " + str(len(lvl_array)))
        logging.debug("size_y: " + str(len(lvl_array[0])))
        return self(term, screen, player, lvl_array)

    def _generate_field(self, renderPlayer):
        self.field = [[' ' for i in range(self.size_y + 1 if self.size_y + 1 > self.terminal_size.y else self.terminal_size.y)]
                           for j in range(self.size_x + 1 if self.size_x + 1 > self.terminal_size_real_x else self.terminal_size_real_x)]
        
        for i in range(self.size_x):
            for j in range( self.size_y):
                self.field[i][j] = self.blank_field[i][j]

        # Get x-size to render
        x = self.size_x if self.terminal_size.x >= self.size_x else self.terminal_size.x 
        # Get y-size to render
        y = self.size_y if self.terminal_size.y >= self.size_y else self.terminal_size.y

        self.player.attackStep(self.blank_field, self.field)

        if renderPlayer:
            mutex_x.acquire()
            if self.player.x + self.player.x_input > 0 and self.player.x + self.player.x_input < self.size_x:
                if self.blank_field[self.player.x + self.player.x_input][self.player.y + self.player.y_input] == ' ' or self.blank_field[self.player.x + self.player.x_input][self.player.y] == ' ':
                    if self.player.x_input == 1 and self.player.x > self.actual_position_x + x - self.player.border_distance and self.actual_position_x + x < self.size_x  + 2:
                        self.actual_position_x += 1
                    elif self.player.x_input == -1 and self.player.x < self.actual_position_x + self.player.border_distance and self.actual_position_x > 0:
                        self.actual_position_x -= 1
                    self.player.x += self.player.x_input
            self.player.x_input = 0
            mutex_x.release()

            mutex_y.acquire()
            if self.player.y + self.player.y_input > 0 and self.player.y + self.player.y_input < self.size_y:
                if self.player.y_input == 1 and self.player.y > self.actual_position_y + y - self.player.border_distance and self.actual_position_y + y < self.size_y + 2:
                    self.actual_position_y += 1
                elif self.player.y_input == -1 and self.player.y < self.actual_position_y + self.player.border_distance and self.actual_position_y > 0:
                    self.actual_position_y -= 1
                if self.blank_field[self.player.x + self.player.x_input][self.player.y + self.player.y_input] == ' ' or self.blank_field[self.player.x][self.player.y + self.player.y_input] == ' ':
                    self.player.y += self.player.y_input
            self.player.y_input = 0
            mutex_y.release()
        self.field[self.player.x][self.player.y] = self.player.icon

    def run(self):
        logging.info("Level2 | start run")
        start = datetime.now()

        while self.running:
            if (self.player != None and datetime.now() - start).total_seconds() < 0.05:
                # If countdown for movement is not ready
                self._generate_field(False)
            else:
                self.player.calcInput()
                if self.player.x_input != 0 or self.player.y_input != 0:
                    start = datetime.now()
                    self._generate_field(True)
                else:
                    self._generate_field(False)
            self._render()
            self.screen.refresh()
            time.sleep(0.025)

    def _render(self):

        color = curses.color_pair(-1)
        size = Size.from_terminal_size(self.screen)
        size.x -= 10
        for i in range(size.x - self.origin.x):
            for j in range(size.y - self.origin.y):
                self.screen.addstr(i + self.origin.x, j + self.origin.y, self.field[self.actual_position_x + i][self.actual_position_y + j], color)

        
        for i in range(size.y):
            self.screen.addstr(0, i, '═', color)
        for i in range(size.y):
            self.screen.addstr(size.x - 1, i, '═', color)

        for i in range(size.x):
            self.screen.addstr(i, 0, '║', color)
            self.screen.addstr(i, size.y - 1, '║', color)

        self.screen.addstr(0, 0, '╔', color)
        self.screen.addstr(0, size.y - 1, '╗', color)
        self.screen.addstr(size.x - 1, 0, '╚', color)
        self.screen.addstr(size.x - 1, size.y - 1, '╝', color)


        Infos = self.addInfos()
        for i in range(10):
            for j in range(30):
                self.screen.addstr(i + size.x,j, Infos[i][j], color)




    def _addCloseFunction(self):
        keyboard.on_press_key('q', lambda _:self._changeScreen())

    def _changeScreen(self, newItem=None):
        logging.info("Change screen!")
        self.term.item = newItem
        self.running = False

    def _getStartField(self):
        blank_field = [[' ' for i in range(self.size_y)]
                      for j in range(self.size_x)]
        blank_field[0] = ['═' for i in range(self.size_y)]
        blank_field[self.size_x - 1] = ['═' for i in range(self.size_y)]
        for i in range(self.size_x):
            blank_field[i][0] = '║'
            blank_field[i][self.size_y - 1] = '║'
        blank_field[0][0] = '╔'
        blank_field[0][self.size_y - 1] = '╗'
        blank_field[self.size_x - 1][0] = '╚'
        blank_field[self.size_x - 1][self.size_y - 1] = '╝'
        return blank_field

    def addInfos(self):
        size = self.term.size

        infos_size_x = 10
        infos_size_y = 30
        Infos = [[' ' for i in range(infos_size_y  + 1)] 
                    for j in range(infos_size_x + 1)]
        for i in Infos:
            logging.debug(i)
        hpText = "HP:"
        for i in range(self.player.hp):
            hpText += '♥'
        for i in range(5 - self.player.hp):
            hpText += '♡'
        positionLineOne = 2

        for i in range(2, 2 + len(hpText)):
            Infos[positionLineOne][i] = hpText[i - 2]
        logging.debug("")
        for i in Infos:
            logging.debug(i)
        logging.debug(Infos[2][3])
        logging.debug("")

        for i in range(0, infos_size_x):
            Infos[i][0] = '║'
            Infos[i][infos_size_y - 1] = '║'

        for i in range(0, infos_size_y - 1):
            Infos[0][i] = '═'
            Infos[infos_size_x - 1][i] = '═'
        
        Infos[0][infos_size_y - 1] = '╗'
        Infos[infos_size_x - 1][infos_size_y - 1] = '╝'
        Infos[infos_size_x - 1][0] = '╚'
        Infos[0][0] = '╔'
        return Infos

class Level2(Level_Default):
    def __init__(self, screen, player):
        super().__init__(screen, player)

    def run(self):
        super().run()
