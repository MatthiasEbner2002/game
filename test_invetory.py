import curses
from components.other.ClassesDefault import Size


def render(screen, values):
    size = Size.from_terminal_size(screen)
    size.x = size.x if size.x <= len(values) else len(values)
    screen.clear()
    color = curses.color_pair(-1)
    for i in range(size.x):
        y = size.y if size.y <= len(values[i]) else len(values[i])
        for j in range(y):
            screen.addstr(i, j, values[i][j], color)
    screen.refresh()


def main(screen):

    file1 = open('components/lvl/inventar_test.txt', 'r', encoding="utf8")
    Lines = file1.readlines()
    Lines = list(Lines)
    curses.initscr()
    curses.start_color()
    curses.curs_set(0)
    render(screen, Lines)
    screen.getch()


curses.wrapper(main)
