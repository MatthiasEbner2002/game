from datetime import datetime
from datetime import datetime
from distutils.log import debug
import time
from components.other.Classes import shutdown, Size, Attack2, Input, Player, Enemy
import logging
import curses
import keyboard
from threading import Lock

mutex_x = Lock()
mutex_y = Lock()
class Level1:
    def __init__(self, term):
        self.size_x = 150
        self.size_y = 250

        self.actual_position_x = 0
        self.actual_position_y = 0

        self.input = Input()
        self.player = Player()

        # Terminal
        self.term = term

        self.player_attack1 = 0
        self.player_attack_step1 = 0
        
        self.attack_2 = []
        self.enemys = []
        self.enemys.append(Enemy(self.player, self.size_y, self.size_x))
        self.enemys.append(Enemy(self.player, self.size_y, self.size_x))

        self.running = True
        self.field = None

        self.setStartField()
        self.show_field = [[' ' for i in range(self.size_y + 1 if self.size_y + 1 > self.term.size.y else self.term.size.y)]
                           for j in range(self.size_x + 1 if self.size_x + 1 > self.term.size.x else self.term.size.x)]
        self._generate_field(True)

    def _generate_field(self, renderPlayer):
        # Get x-size to render
        x = self.size_x if self.term.size.x >= self.size_x else self.term.size.x 
        # Get y-size to render
        y = self.size_y if self.term.size.y >= self.size_y else self.term.size.y

        for i in range(0, self.size_x):
            for j in range(0, self.size_y):
                self.show_field[i][j] = self.field[i][j]
        """
        # add entire field
        for i in range(self.actual_position_x, self.actual_position_x + x):
            for j in range(self.actual_position_y,self.actual_position_y + y):
                self.show_field[i][j] = self.field[i][j]
        """
        if self.player_attack1 == 1:
            self.player_attack_step1 += 1
            if self.player_attack_step1 > 20:
                self.player_attack1 = 0
                self.player_attack_step1 = 0
            else:
                for i in range(self.player.x - (self.player_attack_step1), self.player.x + (self.player_attack_step1 + 1)):
                    if (self.player.y + (self.player_attack_step1) < y - 1  and i > 0 and i < x - 1): 
                        self.show_field[i][self.player.y + (self.player_attack_step1)] = '│'
                    if self.player.y - (self.player_attack_step1) > 0 and i > 0 and i < x -1:
                        self.show_field[i][self.player.y - (self.player_attack_step1)] = '│'

                for i in range(self.player.y - (self.player_attack_step1), self.player.y + (self.player_attack_step1 + 1)):
                    if self.player.x + self.player_attack_step1 < x - 1 and i > 0 and i < y - 1: 
                        self.show_field[self.player.x + (self.player_attack_step1)][i] = '─'
                    if self.player.x - self.player_attack_step1 > 0 and i > 0 and i < y - 1:
                        self.show_field[self.player.x - (self.player_attack_step1)][i] = '─'
                
                if self.player.x - (self.player_attack_step1) > 0 and self.player.y - (self.player_attack_step1) > 0:
                    self.show_field[self.player.x - (self.player_attack_step1)][self.player.y - (self.player_attack_step1)] = '╭'
                if self.player.x + (self.player_attack_step1) < x - 1 and self.player.y - (self.player_attack_step1) > 0:
                    self.show_field[self.player.x + (self.player_attack_step1)][self.player.y - (self.player_attack_step1)] = '╰'

                if self.player.x - (self.player_attack_step1) > 0 and self.player.y + (self.player_attack_step1) < y - 1:
                    self.show_field[self.player.x - (self.player_attack_step1)][self.player.y + (self.player_attack_step1)] = '╮'
                if self.player.x + (self.player_attack_step1) < x - 1 and self.player.y + (self.player_attack_step1) < y - 1:
                    self.show_field[self.player.x + (self.player_attack_step1)][self.player.y + (self.player_attack_step1)] = '╯'
        
        for attack2 in self.attack_2:
            if attack2.play_end_animation == False:
                if attack2.hasNext(self.size_y, self.size_x) == False:
                    attack2.play_end_animation = True
                else:
                    attack2.nextStep()
                    self.show_field[attack2.calcPosition_x()][attack2.calcPosition_y()] = attack2.icon
            else:
                if attack2.hasNextEndAnimation() == False:
                    self.attack_2.remove(attack2)
                else:
                    attack2.addAnimationTo_show_field(self.show_field)

        for enemy in self.enemys:
            enemy.step()
            self.show_field[enemy.x][enemy.y] = enemy.icon

        # Check if Player moved
        if renderPlayer:
            # logging.debug("player is moving" + str(datetime.now()))
            mutex_x.acquire()
            if self.player.x + self.player.x_input > 0 and self.player.x + self.player.x_input < self.actual_position_x + x - 1:    
                if self.player.x_input == 1 and self.player.x > self.actual_position_x + x -  self.player.border_distance and self.actual_position_x + x < self.size_x:
                    self.actual_position_x = self.actual_position_x + 1
                elif self.player.x_input == -1 and self.player.x < self.actual_position_x + self.player.border_distance and self.actual_position_x > 0:
                    self.actual_position_x = self.actual_position_x - 1
                self.player.x = self.player.x + self.player.x_input
            self.player.x_input = 0
            mutex_x.release()
            
            mutex_y.acquire()
            if self.player.y + self.player.y_input > 0 and self.player.y + self.player.y_input < self.actual_position_x + y - 1:
                if self.player.y_input == 1 and self.player.y > self.actual_position_y + y -  self.player.border_distance and self.actual_position_y + y < self.size_y:
                    self.actual_position_y = self.actual_position_y + 1
                elif self.player.y_input == -1 and self.player.y < self.actual_position_y + self.player.border_distance and self.actual_position_y > 0:
                    self.actual_position_y = self.actual_position_y - 1
                self.player.y = self.player.y + self.player.y_input
            self.player.y_input = 0
            mutex_y.release()
        self.show_field[self.player.x][self.player.y] = self.player.icon
        self.addInfos()

    def _clear_field(self, screen):
        size = self.term.size
        for i in range(0, size.x):
            for j in range(0, size.y):
                color = curses.color_pair(-1)
                screen.addstr(i, j, self.show_field[i][j], color)
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
        y = self.size_y if size.y >= self.size_y else size.y
        x = self.size_x if size.x >= self.size_x else size.x
        for i in range(0, x):
            for j in range(0, y):
                color = curses.color_pair(-1)
                screen.addstr(i, j, self.show_field[self.actual_position_x + i][self.actual_position_y + j], color)

    def run(self, screen):
        keyboard.on_press_key('a', lambda _:self.key_down('a'))
        keyboard.on_press_key('d', lambda _:self.key_down('d'))
        keyboard.on_press_key('s', lambda _:self.key_down('s'))
        keyboard.on_press_key('w', lambda _:self.key_down('w'))

        keyboard.on_release_key('a', lambda _:self.key_up('a'))
        keyboard.on_release_key('d', lambda _:self.key_up('d'))
        keyboard.on_release_key('s', lambda _:self.key_up('s'))
        keyboard.on_release_key('w', lambda _:self.key_up('w'))

        keyboard.on_press_key('q', lambda _:self.changeScreen())

        keyboard.on_press_key('u', lambda _:self.attack1())
        keyboard.on_press_key('i', lambda _:self.attack2())

        logging.debug("start running")
        self._clear_field(screen)
        self.render(screen)
        start = datetime.now()

        while self.running:
            x, y = screen.getmaxyx()
            if self.term.size.x - 1 != x or self.term.size.y != y:
                self.resize(screen)

            if (datetime.now() - start).total_seconds() > 0.05:
                
                # calc movement for x and y
                self.player.y_input = self.input.d - self.input.a
                self.player.x_input = self.input.s - self.input.w
                
                # if player moved generate player
                if self.player.x_input != 0 or self.player.y_input != 0:
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

    def resize(self, screen):
        self.term.size = Size.from_terminal_size(screen)
        # self.show_field = [[' ' for i in range(self.term.size.y)]
        #                    for j in range(self.term.size.x)]

    def setStartField(self):
        self.field = [[' ' for i in range(self.size_y)]
                      for j in range(self.size_x)]
        self.field[0] = ['═' for i in range(self.size_y)]
        self.field[self.size_x - 1] = ['═' for i in range(self.size_y)]
        for i in range(self.size_x):
            self.field[i][0] = '║'
            self.field[i][self.size_y - 1] = '║'
        self.field[0][0] = '╔'
        self.field[0][self.size_y - 1] = '╗'
        self.field[self.size_x - 1][0] = '╚'
        self.field[self.size_x - 1][self.size_y - 1] = '╝'
        logging.debug("Level1: finished generate Field")

    def key_down(self, key):
        match key:
            case 'a':
                self.input.a = 1 
            case 'd':
                self.input.d = 1
            case 'w':
                self.input.w = 1
            case 's':
                self.input.s = 1

    def key_up(self, key):
        match key:
            case 'a':
                self.input.a = 0 
            case 'd':
                self.input.d = 0
            case 'w':
                self.input.w = 0
            case 's':
                self.input.s = 0

    def attack1(self):
        self.player_attack1 = 1

    def attack2(self):
        if self.input.d - self.input.a != 0 or self.input.s - self.input.w != 0:
            attack = Attack2((self.player.y, self.player.x), (self.input.d - self.input.a),  (self.input.s - self.input.w))
            self.attack_2.append(attack)

    def addInfos(self):
        infos_size_x = 10
        infos_size_y = 30
        size = self.term.size
        for i in range(size.x - infos_size_x, size.x - 2):
            self.show_field[self.actual_position_x + i][self.actual_position_y + 2] = '║'
            self.show_field[self.actual_position_x + i][self.actual_position_y + infos_size_y + 2] = '║'

        for i in range( 3, 2 + infos_size_y):
            self.show_field[self.actual_position_x + size.x - 2][self.actual_position_y + i] = '═'
            self.show_field[self.actual_position_x + size.x - infos_size_x - 1][self.actual_position_y + i] = '═'
        
        self.show_field[self.actual_position_x + size.x - infos_size_x - 1][self.actual_position_y + infos_size_y + 2] = '╗'
        self.show_field[self.actual_position_x + size.x - 2][self.actual_position_y + infos_size_y + 2] = '╝'
        self.show_field[self.actual_position_x + size.x - 2][self.actual_position_y + 2] = '╚'
        self.show_field[self.actual_position_x + size.x - infos_size_x - 1][self.actual_position_y + 2] = '╔'

def exit():
    quit()