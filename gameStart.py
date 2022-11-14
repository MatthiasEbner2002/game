import logging
import curses
from components.screen import Screen
from components.menus.screen_mainMenu import Screen_MainMenu


def main(screen):
    curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 1, -1)                # red
    curses.init_pair(2, 12, -1)              # orange
    curses.init_pair(3, 3, -1)                # yellow
    curses.init_pair(4, 2, -1)                # green
    curses.init_pair(5, 4, -1)                # blue
    curses.init_pair(6, 5, -1)                # purple

    # for i in range(4, 255):
    #   curses.init_pair(i + 1, i, -1)
    curses.curs_set(0)
    logging.basicConfig(filename='log.log',
                        filemode='a',
                        format='%(asctime)s | %(name)s | %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    term = Screen.from_terminal_size(screen)
    term.item = Screen_MainMenu(screen, term)

    while (True):
        term.run(screen=screen)
        logging.info("GameStart: render again")


if __name__ == '__main__':
    curses.wrapper(main)
