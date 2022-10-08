
import msvcrt

while True:
    if msvcrt.kbhit():
        ch = msvcrt.getch()
        if ch in '\x00\xe0':  # arrow or function key prefix?
            ch = msvcrt.getch()  # second call returns the scan code
        if ch == 'q':
           print ("Q was pressed")
        elif ch == 'x':
           sys.exit()
        else:
           print ("Key Pressed:", ch)