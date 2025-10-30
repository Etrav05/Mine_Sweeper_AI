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
x, y = 271, 271

loseFaceX, loseFaceY = 392, 210
winFaceX, winFaceY = 401, 196

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def randomClicks():
    random_x = random.randint(0, 8) * 32
    random_y = random.randint(0, 8) * 32

    click(x + random_x, y + random_y)

def winLose(plays):
    state = False

    ## check frown/glasses (win/lose)
    if pyautogui.pixel(winFaceX, winFaceY)[0] == 0:
        print("==== WINNER ====")
        state = True

    if pyautogui.pixel(loseFaceX, loseFaceY)[0] == 0:
        plays += 1
        click(390, 213)
        print(f"Restarting, now on game: {plays}")
        state = False

    return state, plays

def main():
    plays = 0
    state = False

    while not keyboard.is_pressed('q') and not state:  ## Kill button
        randomClicks()
        state, plays = winLose(plays)

if __name__ == "__main__":
    main()
