import curses
from components.other.ClassesDefault import Size


import random


def render(screen, values, x, y):
    size = Size.from_terminal_size(screen)
    screen.clear()
    color = curses.color_pair(-1)
    for i in range(100):
        screen.addstr(round(values[i] * size.x), i, '.', color)
    screen.refresh()


def calc(people):
    uniqueYears = 0
    times = 10000
    for i in range(times):
        days = []
        for i in range(people):
            days.append(random.randint(1, 365))

        if (len(set(days)) == len(days)):
            uniqueYears += 1
    return (1 - uniqueYears / times)


def main(screen):
    curses.initscr()
    curses.start_color()
    curses.curs_set(0)
    term = Size.from_terminal_size(screen)

    values = [0 for i in range(100)]
    for i in range(100):
        values[i] = (calc(i))
        render(screen, values, term.x, term.y)
    screen.getch()


curses.wrapper(main)
