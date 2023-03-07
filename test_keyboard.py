from threading import Thread
import time
from pynput import keyboard
from datetime import datetime


class Test_Keyboard:
    up = 0
    down = 0
    left = 0
    right = 0
    t = datetime.now()


def mywait():
    # print(keyboard.read_key())
    # time.sleep(10)
    print("s")


def my_function():
    print("Hello")
    time.sleep(10)


def player(test):
    while True:
        if keyboard.is_pressed('a'):
            test.left = 1
        if keyboard.is_pressed('d'):
            test.right = 1
        if keyboard.is_pressed('w'):
            test.up = 1
        if keyboard.is_pressed('s'):
            test.down = 1
        time.sleep(0.025)


def my_exit():
    quit()


test = Test_Keyboard()

new_thread = Thread(target=player, args=(test,), daemon=True)
new_thread.start()
start = datetime.now()
while True:
    if (datetime.now()-start).total_seconds() > 1: 
        print("x= " + str(test.left - test.right) +
            ", y= " + str(test.up - test.down))
        if test.left == 1 or test.right == 1 or test.up == 1 or test.down == 1:
            print("time")
            test.left = 0
            test.right = 0
            test.up = 0
            test.down = 0
            start = datetime.now()
    time.sleep(0.5)
