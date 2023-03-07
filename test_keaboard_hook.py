from pynput import keyboard


def keyboardTEST(info):
        print(info)

keyboard.hook(keyboardTEST)
while True:
    pass