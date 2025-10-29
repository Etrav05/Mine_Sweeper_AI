from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

## first block = 271, 271
## Change = 32
## Unknown block RGB = 189, 189, 189

gameBoard = 9
change = 32

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

while not keyboard.is_pressed('q'):  ## Kill button
    x, y = 271, 271

    for i in range(gameBoard + 1):
        y = 271 + (change * i)

        for j in range(gameBoard + 1):
            if pyautogui.pixel(x, y)[0] == 189:
                click(x, y)
            x = 271 + (change * i)

