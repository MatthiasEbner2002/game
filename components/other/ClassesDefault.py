import copy
import time
import curses
import logging
import keyboard
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
    if field_color is None:
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
        for i in range(x + 1, size.x - x, 1):
            show_field[i][y] = c1
            field_color[i][y] = getColorIndex(x)
        y = y + 1

        for i in range(x + 1, size.x - x, 1):
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
            screen.addstr(i, j, str(show_field[i][j]), color)


class Player:
    def __init__(self, start_position_y=None, start_position_x=None):
        logging.info("Player created!")
        self.x = 10 if start_position_x is None else start_position_x
        self.y = 10 if start_position_y is None else start_position_y
        self.icon = '█'
        self.max_hp = 10
        self.hp = self.max_hp
        self.x_input = 0
        self.y_input = 0
        self.border_distance = 8
        self.player_attack1 = 0
        self.player_attack_step1 = 0
        self.attacks = []
        self.isAlive = True
        self.input = Input()

        self.addMovement()
        self.addAttack2()

    def getHit(self, hp):
        logging.debug("player getting hit")
        self.hp -= hp
        if self.hp <= 0:
            self.isAlive = False

    def addMovement(self):
        keyboard.on_press_key('a', lambda _: self.keyDown('a'))
        keyboard.on_press_key('d', lambda _: self.keyDown('d'))
        keyboard.on_press_key('s', lambda _: self.keyDown('s'))
        keyboard.on_press_key('w', lambda _: self.keyDown('w'))

        keyboard.on_release_key('a', lambda _: self.keyUp('a'))
        keyboard.on_release_key('d', lambda _: self.keyUp('d'))
        keyboard.on_release_key('s', lambda _: self.keyUp('s'))
        keyboard.on_release_key('w', lambda _: self.keyUp('w'))
        logging.debug("add Player movement")

    def keyDown(self, key):
        match key:
            case 'a':
                self.input.a = 1
            case 'd':
                self.input.d = 1
            case 'w':
                self.input.w = 1
            case 's':
                self.input.s = 1

    def keyUp(self, key):
        match key:
            case 'a':
                self.input.a = 0
            case 'd':
                self.input.d = 0
            case 'w':
                self.input.w = 0
            case 's':
                self.input.s = 0

    def calcInput(self):
        self.y_input = self.input.d - self.input.a
        self.x_input = self.input.s - self.input.w

    def addAttack2(self):
        keyboard.on_press_key('i', lambda _: self.attack2())

    def attack2(self):
        if self.input.d - self.input.a != 0 or self.input.s - self.input.w != 0:
            attack = Attack2((self.y, self.x), (self.input.d - self.input.a),  (self.input.s - self.input.w))
            self.addAttack(attack=attack)

    def addAttack(self, attack):
        self.attacks.append(attack)

    def attackStep(self, blank_field, field):
        for attack in self.attacks:
            attack.step(self.attacks, blank_field, field)


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

        if direction_y == 1 and direction_x == 1:
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

    def hasNext(self, blank_field):
        next_x = self.start_point[1] + self.direction_x * ((self.steps + 1) // 2)
        next_y = self.start_point[0] + self.direction_y * (self.steps + 1)

        if blank_field[next_x][next_y] != ' ':
            return False
        if self.steps >= self.maxSteps:
            return False
        return True

    def step(self, attacks, blank_field, field):
        if self.play_end_animation is False:
            if self.hasNext(blank_field) is False:
                self.play_end_animation = True
            else:
                self.steps += 1
                field[self.calcPosition_x()][self.calcPosition_y()] = self.icon
        else:
            if self.hasNextEndAnimation() is False:
                attacks.remove(self)
            else:
                self.addAnimationTo_show_field(field)

    def calcPosition_x(self):
        return self.start_point[1] + self.direction_x * (self.steps // 2)

    def calcPosition_y(self):
        return self.start_point[0] + self.direction_y * self.steps

    def addAnimationTo_show_field(self, show_field):
        animation = self.end_animation[self.end_animation_steps // 2]
        for i in range(len(animation)):
            for j in range(len(animation[1])):
                if animation[i][j] != ' ':
                    animation_next_position_x = self.start_point[1] + self.direction_x * (self.steps // 2) - 1 + i
                    animation_next_position_y = self.start_point[0] + self.direction_y * self.steps - 3 + j
                    show_field[animation_next_position_x][animation_next_position_y] = animation[i][j]
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
    def __init__(self, player, size_y, size_x, position_x=None, position_y=None, field=None):
        self.player = player
        self.icon = '@'
        self.size_x = size_x
        self.size_y = size_y
        self.x = position_x
        self.y = position_y
        self.field = field

        self.die_to = ['↖', '↘', '↗', '↙', '↓', '↑', '←', '→']
        if self.x is None or self.y is None:
            self.spawnRandom()

        self.steps = 0
        self.isAlive = True

    def spawnRandom(self):
        self.y = random.randint(1, self.size_y - 1)
        self.x = random.randint(1, self.size_x - 1)

    def step(self, field):
        if self.player.y == self.y and self.player.x == self.x:
            self.player.getHit(1)
            self.isAlive = False
        if field[self.x][self.y] in self.die_to:
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
    countEnemy = 1

    def __init__(self, player, lvl1, y, x, position_x, position_y):
        self.player = player

        self.lvl1 = lvl1

        self.icon = '֎'

        self.size_x = x
        self.size_y = y

        self.spawn_enemys = True

        self.isAlive = True

        self.x = position_x
        self.y = position_y
        self.steps = 0
        self.max_steps = 100

    def step(self, field):
        self.steps += 1
        if self.spawn_enemys and self.steps % self.max_steps == 0:
            logging.debug("spawn enemy")
            self.spawn_enemy()
            self.steps = 0

    def spawn_enemy(self):
        ran_x = random.randint(-3, 3)
        while ran_x == 0:
            ran_x = random.randint(-3, 3)
        ran_y = random.randint(-3, 3)
        while ran_y == 0:
            ran_y = random.randint(-3, 3)
        self.countEnemy += 1
        self.lvl1.enemys.append(
            Enemy(
                self.player,
                self.size_y,
                self.size_x,
                self.x + ran_x,
                self.y + ran_y,
                self.lvl1.field)
        )
