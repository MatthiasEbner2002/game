import logging
from components.other.Classes import Size


class Screen:
    def __init__(self, x, y, screen):
        self.item = None
        self.screen = screen
        self.size = Size(x, y)
        self.backup = Backup(self.size)
        # self._generate_field()

    @classmethod
    def from_terminal_size(cls, screen):
        size = Size.from_terminal_size(screen)
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
            # self.item.run(screen)#  for lvl1
            self.item.run()
        else:
            self.backup.run(screen)


class Backup:
    def __init__(self, size):
        self.size = size
        self.message = '!! Error: no module found! (press any key to quit) !!'
        self.field = [[' ' for i in range(self.size.y)]
                      for j in range(self.size.x)]

    def _clear_field(self):
        self.field = [[j if j != 1 and j != 2 else 0 for j in i]
                      for i in self.field]

    def render(self, screen):
        screen.addstr(0, 0, self.message)

    def _generate_field(self):
        logging.error("Backup: Generate Field without a item to render!")

    def run(self, screen):
        logging.error("Backup: updating without a item to run!")
        self.render(screen)
        screen.refresh()
        screen.getch()
        quit()
