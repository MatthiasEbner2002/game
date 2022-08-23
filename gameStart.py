import time
import curses
from components.MyClass import Field, Main_Menu
import logging


def main(screen):
    logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s | %(name)s | %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

    num_rows, num_cols = screen.getmaxyx()
    field = Field.from_terminal_size(screen)
    field.item = Main_Menu(field.size)

    while (True):
        field.run(screen)
        logging.info("render again")


if __name__ == '__main__':
    curses.wrapper(main)
