from myLogger import error, logLines, error_text, info_text, debug_text
from .ClassesDefault import Size
import curses


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.terminal_size = Size.from_terminal_size(self.screen)
        self.elements = []

    def render(self):
        self.screen.clear()
        for i in self.elements:
            i.render()

    def addElement(self, component):
        if component is None:
            error("cant add component that is None")
        else:
            self.elements.append(component)

    def update_Terminal_Size(self, from_terminal=True, x=None, y=None):
        if from_terminal is True or x is None or y is None:
            self.terminal_size = Size.from_terminal_size(self.screen)
        else:
            self.terminal_size = Size(x=x, y=y)


class UI_Component:
    def __init__(self, screen, size_x, size_y, start_x, start_y, start_x_direction=1, start_y_direction=1):
        self.screen = screen
        self.default_color = curses.color_pair(16)
        self.terminal_size = Size.from_terminal_size(self.screen)
        self.start_x = start_x
        self.start_y = start_y
        self.start_x_direction = start_x_direction
        self.start_y_direction = start_y_direction

        if size_x is None:
            self.size_x = self.terminal_size.x
        else:
            self.size_x = size_x
        if size_y is None:
            self.size_y = self.terminal_size.y
        else:
            self.size_y = size_y
        self.field = [[(' ', 16) for i in range(self.size_y)]
                      for j in range(self.size_x)]

    def render(self):
        self.update_Terminal_Size()
        self.generate_field()
        x = self.size_x
        if self.size_x == -1:
            x = self.terminal_size.x - self.start_x
        y = self.size_y
        if self.size_y == -1:
            y = self.terminal_size.y - self.start_y - 1
        add_x = self.start_x
        if self.start_x_direction < 0:
            add_x = self.terminal_size.x - x - self.start_x + 1
        add_y = self.start_y
        if self.start_y_direction < 0:
            add_y = self.terminal_size.y - y - self.start_y
        for i in range(x):
            for j in range(y):
                self.screen.addstr(i + add_x, j + add_y, self.field[i][j][0], self.field[i][j][1])

    def generate_field(self):
        error("UI_Component")
        self.field = [[(' ', 16) for i in range(self.size_y)]
                      for j in range(self.size_x)]

    def update_Terminal_Size(self):
        self.terminal_size = Size.from_terminal_size(self.screen)


class UI_Menu_Bottom(UI_Component):
    def __init__(self, screen, player, split_at, size_x):
        size = Size.from_terminal_size(screen=screen)
        super().__init__(screen, size_x, -1, size.x - size_x, 0)
        self.player = player
        self.left = UI_Info(screen=screen, player=player, size_x=split_at, size_y=-1, start_x=size.x - size_x, start_y=0)
        self.right = UI_Logger()
        self.split_at = split_at

    def generate_field(self):
        self.field = getArrayWithBorderAndColor(self.size_x, self.size_y, 3)
        hpText = self.getHpText()
        positionLineOne = 2
        for i in range(2, 2 + len(hpText)):
            self.field[positionLineOne][i] = hpText[i - 2]


class UI_Info(UI_Component):
    def __init__(self, screen, player, size_x=None, size_y=None, start_x=0, start_y=0, start_x_direction=1, start_y_direction=1):
        super().__init__(screen, size_x, size_y, start_x, start_y, start_x_direction, start_y_direction)
        self.player = player

    def generate_field(self):
        self.field = getArrayWithBorderAndColor(self.size_x, self.size_y, 3)
        hpText = self.getHpText()
        positionLineOne = 2
        for i in range(2, 2 + len(hpText)):
            self.field[positionLineOne][i] = hpText[i - 2]

    def getHpText(self):
        heart_color = 5
        hpText = [(' ', self.default_color) for i in range((self.player.max_hp // 2) + (self.player.max_hp % 2) + 3)]
        hpText[0] = ('H', self.default_color)
        hpText[1] = ('P', self.default_color)
        hpText[2] = (':', self.default_color)
        i = 0
        while i < self.player.hp // 2:
            i += 1
            hpText[i + 2] = ('♥', heart_color)
        if self.player.hp % 2 == 1:
            i += 1
            hpText[i + 2] = ('½', 16)
        while i < self.player.max_hp // 2 + self.player.max_hp % 2:
            i += 1
            hpText[i + 2] = ('♡', 16)
        return hpText


class UI_Logger(UI_Component):
    def __init__(self, screen, size_x=None, size_y=None, start_x=0, start_y=0, start_x_direction=1, start_y_direction=1):
        super().__init__(screen, size_x, size_y, start_x, start_y, start_x_direction, start_y_direction)

    def generate_field(self):
        amountLines = self.size_x - 2
        log_size_x = self.size_x
        if log_size_x == -1:
            log_size_x = self.terminal_size.x - self.start_x
        log_size_y = self.size_y
        if log_size_y == -1:
            log_size_y = self.terminal_size.y - self.start_y - 1
        self.field = getArrayWithBorderAndColor(log_size_x, log_size_y, 6)

        lines = amountLines if amountLines < len(logLines) else len(logLines)
        res = logLines[-lines:]

        for i in range(lines):
            color = 16
            s = str(res[i][0:5])
            if error_text == s:
                color = 5
            elif info_text == s:
                color = 3
            elif debug_text == s:
                color = 6

            for j in range(log_size_y - 1 if log_size_y - 1 < len(res[i]) else len(res[i])):
                if j < 5:
                    self.field[i + 1][j + 1] = (res[i][j], color)
                else:
                    self.field[i + 1][j + 1] = (res[i][j], 16)


class UI_Inventory(UI_Component):
    def __init__(self, x=10, y=10):
        super().__init__(x=x, y=y)


def getArrayWithBorder(x, y):
    ret = [[' ' for i in range(y + 1)]
           for j in range(x + 1)]

    for i in range(0, x):
        ret[i][0] = '║'
        ret[i][y - 1] = '║'

    for i in range(0, y - 1):
        ret[0][i] = '═'
        ret[x - 1][i] = '═'

    ret[0][y - 1] = '╗'
    ret[x - 1][y - 1] = '╝'
    ret[x - 1][0] = '╚'
    ret[0][0] = '╔'

    return ret


def getArrayWithBorderAndColor(x, y, border_color):
    ret = [[(' ', 16) for i in range(y + 1)]
           for j in range(x + 1)]

    for i in range(0, x):
        ret[i][0] = ('║', border_color)
        ret[i][y - 1] = ('║', border_color)

    for i in range(0, y - 1):
        ret[0][i] = ('═', border_color)
        ret[x - 1][i] = ('═', border_color)

    ret[0][y - 1] = ('╗', border_color)
    ret[x - 1][y - 1] = ('╝', border_color)
    ret[x - 1][0] = ('╚', border_color)
    ret[0][0] = ('╔', border_color)

    return ret
