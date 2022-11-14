import os
import copy
import time
import curses
import logging
import random


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

def getColorIndex(x):
    return x % 6 + 1

def shutdown(screen, show_field, field_color=None):
    size = Size.from_terminal_size(screen)
    show_field = copy.deepcopy(show_field)
    if field_color == None:
        field_color = [[-1 for i in range(size.y)] for j in range(size.x)]
    c1 = '#'
    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(y, size.y - y, 1):
            show_field[x][i] = c1
            field_color[x][i] = getColorIndex(x)
        shutdown_render(screen, show_field, field_color)

        x = x + 1
        y = y + 3

    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(x+1, size.x - x, 1):
            show_field[i][size.y - y - 1] = c1
            field_color[i][size.y - y - 1] = getColorIndex(x)
        y = y + 1

        for i in range(x+1, size.x - x, 1):
            show_field[i][size.y - y - 1] = c1
            field_color[i][size.y - y - 1] = getColorIndex(x)
        y = y + 1

        for i in range(x + 1, size.x - x, 1):
            show_field[i][size.y - y - 1] = c1
            field_color[i][size.y - y - 1] = getColorIndex(x)
        y = y + 1
        x = x + 1
        shutdown_render(screen, show_field, field_color)

    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(y, size.y - y, 1):
            show_field[size.x - x - 1][i] = c1
            field_color[size.x - x - 1][i] = getColorIndex(x)
        shutdown_render(screen, show_field, field_color)

        x = x + 1
        y = y + 3

    x, y = 0, 0
    while x <= size.x - x and y <= size.y - y:
        for i in range(x+1, size.x - x, 1):
            show_field[i][y] = c1
            field_color[i][y] = getColorIndex(x)
        y = y + 1

        for i in range(x+1, size.x - x, 1):
            show_field[i][y] = c1
            field_color[i][y] = getColorIndex(x)
        y = y + 1

        for i in range(x + 1, size.x - x, 1):
            show_field[i][y] = c1
            field_color[i][y] = getColorIndex(x)
        y = y + 1
        x = x + 1
        shutdown_render(screen, show_field, field_color)
    time.sleep(0.3)
    quit()

def shutdown_render(screen, show_field, field_color):
    render(screen, show_field, field_color)
    screen.refresh()
    time.sleep(0.025)
    return

def render(screen, show_field, field_color):
    size = Size.from_terminal_size(screen)
    for i in range(size.x):
        for j in range(size.y):
            color = curses.color_pair(field_color[i][j])
            #logging.debug(str(i) + ' ' + str(j) + ' ' + str(show_field[i][j]))
            screen.addstr(i, j, str(show_field[i][j]), color)
class Player:
    def __init__(self):
        self.icon = '█'

        self.x = 10
        self.y = 10
        
        self.hp = 5

        self.x_input = 0
        self.y_input = 0

        self.border_distance = 8

        self.player_attack1 = 0
        self.player_attack_step1 = 0
        
        self.attack_2 = []
        self.isAlive = True

    def getHit(self, hp):
        logging.debug("player getting hit")
        self.hp -= hp
        if self.hp <= 0:
            self.isAlive = False

class Attack2:
    def __init__(self, startpoint, direction_y, direction_x):
        self.maxSteps = 50
        self.steps = 1
        self.start_point = startpoint
        self.direction_x = direction_x
        self.direction_y = direction_y

        self.play_end_animation = False
        self.end_animation_maxSteps = 6
        self.end_animation_steps = 0

        self.end_animation = [
            [
            '       ',
            '   ┼   ',
            '       '
            ],
            [
            '   ┬   ',
            ' ├─┼─┤ ',
            '   ┴   '
            ],
             [
            '       ',
            '  ═╬═  ',
            '       '
            ]
        ]

        self.icon = '↺'

        if  direction_y == 1 and direction_x == 1:
            self.icon = '↘'
        elif direction_y == -1 and direction_x == -1:
            self.icon = '↖'
        elif direction_y == 1 and direction_x == -1:
            self.icon = '↗'
        elif direction_y == -1 and direction_x == 1:
            self.icon = '↙'
        elif direction_y == 0 and direction_x == 1:
            self.icon = '↓'
        elif direction_y == 0 and direction_x == -1:
            self.icon = '↑'
        elif direction_y == -1 and direction_x == 0:
            self.icon = '←'
        elif direction_y == 1 and direction_x == 0:
            self.icon = '→'
    
    def hasNext(self, size_y, size_x):
        if self.start_point[1] + self.direction_x * ((self.steps + 1) // 2) <= 0 or self.start_point[1] + self.direction_x * ((self.steps + 1) // 2) >= size_x - 1: 
            return False
        if self.start_point[0] + self.direction_y * (self.steps + 1) <= 0 or self.start_point[0] + self.direction_y * (self.steps + 1) >= size_y - 1: 
            return False
        if self.steps >= self.maxSteps:
            return False
        return True
    
    def nextStep(self):
        self.steps += 1

    def calcPosition_x(self):
        return self.start_point[1] + self.direction_x * (self.steps // 2)   
    
    def calcPosition_y(self):
        return self.start_point[0] + self.direction_y  * self.steps

    def addAnimationTo_show_field(self, show_field):
        animation = self.end_animation[self.end_animation_steps // 2]
        for i in range(len(animation)):
            for j in range(len(animation[1])):
                if animation[i][j] != ' ':
                    show_field[self.start_point[1] + self.direction_x * (self.steps // 2) - 1 + i][self.start_point[0] + self.direction_y * self.steps - 3 + j] = animation[i][j]
        self.end_animation_steps += 1
    def hasNextEndAnimation(self):
        return self.end_animation_steps < self.end_animation_maxSteps

class Input:
    def __init__(self):
        self.a = 0
        self.d = 0
        
        self.w = 0
        self.s = 0

class Enemy: 
    def __init__(self, player, size_y, size_x, position_x=None, position_y=None):
        self.player = player
        self.icon = '@'
        self.size_x = size_x
        self.size_y = size_y
        self.x = position_x
        self.y = position_y

        self.die_to = ['↖','↘','↗','↙','↓', '↑','←', '→']

        if self.x  == None or self.y == None:
            self.spawnRandom()
        
        self.steps = 0
        self.isAlive = True

    def spawnRandom(self):
        self.y = random.randint(1, self.size_y - 1)
        self.x = random.randint(1, self.size_x - 1)
    
    def step(self, show_field):
        if self.player.y == self.y and self.player.x == self.x:
            self.player.getHit(1)
            self.isAlive = False
        if show_field[self.x][self.y] in self.die_to:
            self.isAlive = False
        if self.steps % 15 == 0:
            self.steps = 1
            if self.player.x < self.x:
                self.x -= 1
            elif self.player.x > self.x:
                self.x += 1

            if self.player.y < self.y:
                self.y -= 1
            elif self.player.y > self.y:
                self.y += 1

        else:
            self.steps += 1

class EnemySpawn:
    def __init__(self, player,lvl1, y, x, position_x, position_y):
        self.player = player
        
        self.lvl1 = lvl1

        self.icon ='֎'
        
        self.size_x = x
        self.size_y = y

        self.spawn_enemys = True

        self.isAlive = True

        self.x = position_x
        self.y = position_y
        self.steps = 0
        self.max_steps = 100
        
    def step(self):
        self.steps += 1
        if self.spawn_enemys and self.steps % self.max_steps == 0:
            self.spawn_enemy()
            self.steps = 0

    def spawn_enemy(self):
        ran_x = random.randint(-3, 3)
        while ran_x == 0:
            ran_x = random.randint(-3, 3)
        ran_y = random.randint(-3, 3)
        while ran_y == 0:
            ran_y = random.randint(-3, 3)
        self.lvl1.enemys.append(Enemy(self.player, self.size_y, self.size_x, self.x + ran_x, self.y + ran_y))
