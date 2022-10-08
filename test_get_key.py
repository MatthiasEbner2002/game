import curses

screen = curses.initscr()
screen.addstr("Press any key...")
screen.refresh()

c = screen.getch()

curses.endwin()

# Convert the key to ASCII and print ordinal value
print("You pressed %s which is keycode %d." % (chr(c), c))