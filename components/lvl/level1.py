from datetime import datetime
from datetime import datetime
from distutils.log import debug
import time
from components.other.Classes import shutdown, Size
import logging
import curses
import keyboard
from threading import Lock, Thread

mutex_x = Lock()
mutex_y = Lock()
class Level1:
    def __init__(self, term):
        self.size_x = 100
        self.size_y = 100

        self.actual_position_x = 0
        self.actual_position_y = 0

        self.term = term
        self.player = '█'

        self.player_x = 10
        self.player_y = 10

        self.player_border_distance = 8

        self.player_x_input = 0
        self.player_y_input = 0

        self.player_attack = 0
        self.player_attack_start_position = (0,0)
        self.player_attack_step = 0

        self.running = True
        self.field = None

        self.setStartField()
        self.show_field = [[' ' for i in range(self.term.size.y)]
                           for j in range(self.term.size.x)]
        self._generate_field(True)

    def _generate_field(self, renderPlayer):
        # Get x-size to render
        if self.term.size.x >= self.size_x:
            x = self.size_x
        else:
            x = self.term.size.x

        # Get y-size to render
        if self.term.size.y >= self.size_y:
            y = self.size_y
        else:
            y = self.term.size.y

        for i in range(self.actual_position_x, x + self.actual_position_x):
            for j in range(self.actual_position_y, y + self.actual_position_y):
                self.show_field[i - self.actual_position_x][j -
                                                            self.actual_position_y] = self.field[i][j]
        if self.player_attack == 1:
            self.player_attack_step += 1
            if self.player_attack_step > 8:
                self.player_attack = 0
                self.player_attack_step = 0
            else:
                for i in range(self.player_attack_start_position[0] - (self.player_attack_step), self.player_attack_start_position[0] + (self.player_attack_step + 1)):
                    if (self.player_attack_start_position[1] + (self.player_attack_step) < y - 1  and i > 0 and i < x - 1): 
                        self.show_field[i][self.player_attack_start_position[1] + (self.player_attack_step)] = '│'
                    if self.player_attack_start_position[1] - (self.player_attack_step) > 0 and i > 0 and i < x -1:
                        self.show_field[i][self.player_attack_start_position[1] - (self.player_attack_step)] = '│'

                for i in range(self.player_attack_start_position[1] - (self.player_attack_step), self.player_attack_start_position[1] + (self.player_attack_step + 1)):
                    if self.player_attack_start_position[0] + self.player_attack_step < x - 1 and i > 0 and i < y - 1: 
                        self.show_field[self.player_attack_start_position[0] + (self.player_attack_step)][i] = '─'
                    if self.player_attack_start_position[0] - self.player_attack_step > 0 and i > 0 and i < y - 1:
                        self.show_field[self.player_attack_start_position[0] - (self.player_attack_step)][i] = '─'
                
                if self.player_attack_start_position[0] - (self.player_attack_step) > 0 and self.player_attack_start_position[1] - (self.player_attack_step) > 0:
                    self.show_field[self.player_attack_start_position[0] - (self.player_attack_step)][self.player_attack_start_position[1] - (self.player_attack_step)] = '╭'
                if self.player_attack_start_position[0] + (self.player_attack_step) < x - 1 and self.player_attack_start_position[1] - (self.player_attack_step) > 0:
                    self.show_field[self.player_attack_start_position[0] + (self.player_attack_step)][self.player_attack_start_position[1] - (self.player_attack_step)] = '╰'

                if self.player_attack_start_position[0] - (self.player_attack_step) > 0 and self.player_attack_start_position[1] + (self.player_attack_step) < y - 1:
                    self.show_field[self.player_attack_start_position[0] - (self.player_attack_step)][self.player_attack_start_position[1] + (self.player_attack_step)] = '╮'
                if self.player_attack_start_position[0] + (self.player_attack_step) < x - 1 and self.player_attack_start_position[1] + (self.player_attack_step) < y - 1:
                    self.show_field[self.player_attack_start_position[0] + (self.player_attack_step)][self.player_attack_start_position[1] + (self.player_attack_step)] = '╯'
        
        # Check if Player moved
        if renderPlayer:
            mutex_x.acquire()
            if self.player_x + self.player_x_input > 0 and self.player_x + self.player_x_input < x - 1:    
                if self.player_x_input == 1 and self.player_x > x -  self.player_border_distance and self.actual_position_x + x < self.size_x:
                    self.actual_position_x = self.actual_position_x + 1
                elif self.player_x_input == -1 and self.player_x <  self.player_border_distance and self.actual_position_x > 0:
                    self.actual_position_x = self.actual_position_x - 1
                else:
                    self.player_x = self.player_x + self.player_x_input
            self.player_x_input = 0
            mutex_x.release()
            
            mutex_y.acquire()
            if self.player_y + self.player_y_input > 0 and self.player_y + self.player_y_input < y - 1:
                if self.player_y_input == 1 and self.player_y > y -  self.player_border_distance and self.actual_position_y + y < self.size_y:
                    self.actual_position_y = self.actual_position_y + 1
                elif self.player_y_input == -1 and self.player_y <  self.player_border_distance and self.actual_position_y > 0:
                    self.actual_position_y = self.actual_position_y - 1
                else:
                    self.player_y = self.player_y + self.player_y_input
            self.player_y_input = 0
            mutex_y.release()
        self.show_field[self.player_x][self.player_y] = self.player

        if self.player_y > y - 10 and self.actual_position_y + y < self.size_y:
            self.actual_position_y = self.actual_position_y + 1

    def _clear_field(self):
        logging.debug("cleaning")
        return

    def _enter(self, option, screen):
        if option == 0:
            logging.debug("PLAY")
            self.changeScreen()
        elif option == 1:
            logging.debug("SETTING")
            self.changeScreen()
        elif option == 2:
            logging.debug("QUITING")
            shutdown(self, screen)

    def changeScreen(self):
        self.term.item = None
        self.running = False

    def render(self, screen):
        size = self.term.size
        # self._clear_field()
        for i in range(size.x):
            for j in range(size.y):
                color = curses.color_pair(-1)
                screen.addstr(i, j, self.show_field[i][j], color)

    def run(self, screen):
        # Hotkey 'q' to exit game
        #
        # keyboard.add_hotkey('q', exit)
        # start player-Thread with gets input from keyboard (daemon = stop if program is terminated)
        new_thread = Thread(target=player, args=(self,), daemon=True)
        new_thread.start()
        logging.debug("start running")
        start = datetime.now()

        while self.running:
            x, y = screen.getmaxyx()
            if self.term.size.x - 1 != x or self.term.size.y != y:
                self.resize(screen)

            if (datetime.now() - start).total_seconds() > 0.1:
                if self.player_x_input != 0 or self.player_y_input != 0:
                    # logging.debug("Input received: " + str(start) + ", x: " + str(self.player_x_input) + ", y: " + str(self.player_y_input) )
                    start = datetime.now()
                    self._generate_field(True)
                else:
                    self._generate_field(False)
                    time.sleep(0.025)
            else:
                self._generate_field(False)
                time.sleep(0.025)
            self.render(screen)
            screen.refresh()
        new_thread.join()

    def resize(self, screen):
        self.term.size = Size.from_terminal_size(screen)
        self.show_field = [[' ' for i in range(self.term.size.y)]
                           for j in range(self.term.size.x)]

    def setStartField(self):
        self.field = [[' ' for i in range(self.size_x)]
                      for j in range(self.size_y)]
        self.field[0] = ['═' for i in range(self.size_x)]
        self.field[self.size_y - 1] = ['═' for i in range(self.size_x)]
        for i in range(self.size_y):
            self.field[i][0] = '║'
            self.field[i][self.size_y - 1] = '║'
        self.field[0][0] = '╔'
        self.field[0][self.size_y - 1] = '╗'
        self.field[self.size_x - 1][0] = '╚'
        self.field[self.size_x - 1][self.size_y - 1] = '╝'
        logging.debug("Level1: finished generate Field")


def exit():
    quit()

def player(lvl1):
    while True:
        if keyboard.is_pressed('a'):
            mutex_y.acquire()
            lvl1.player_y_input = -1 if lvl1.player_y_input == 0 else 0
            mutex_y.release()
        if keyboard.is_pressed('d'):
            mutex_y.acquire()
            lvl1.player_y_input = 1 if lvl1.player_y_input == 0 else 0
            mutex_y.release()
        if keyboard.is_pressed('w'):
            mutex_x.acquire()
            lvl1.player_x_input = -1 if lvl1.player_x_input == 0 else 0
            mutex_x.release()
        if keyboard.is_pressed('s'):
            mutex_x.acquire()    
            lvl1.player_x_input = 1 if lvl1.player_x_input == 0 else 0
            mutex_x.release()
        if keyboard.is_pressed('o'):
            lvl1.player_attack = 1
            lvl1.player_attack_start_position = (lvl1.player_x, lvl1.player_y)
        time.sleep(0.001)
