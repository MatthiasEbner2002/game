import curses
import logging
from components.screen import Screen
from components.menus.screen_mainMenu import Screen_MainMenu


def main(screen):
    curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 1, -1)                # red
    curses.init_pair(2, 202, -1)              # orange
    curses.init_pair(3, 3, -1)                # yellow
    curses.init_pair(4, 2, -1)                # green
    curses.init_pair(5, 4, -1)                # blue
    curses.init_pair(6, 5, -1)                # purple

    for i in range(4, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    logging.basicConfig(filename='log.log',
                        filemode='a',
                        format='%(asctime)s | %(name)s | %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    num_rows, num_cols = screen.getmaxyx()
    field = Screen.from_terminal_size(screen)
    field.item = Screen_MainMenu(field.size)

    while (True):
        field.run(screen)
        logging.info("render again")


if __name__ == '__main__':
    curses.wrapper(main)
