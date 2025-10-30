import pyautogui
import time
import keyboard
import random
import win32api, win32con

## first blocks top corner = 258, 256
## Change = 32
## Unknown block RGB = 189, 189, 189

gameBoard = 9
change = 32
startX, startY = 258, 256
numColX, numColY = 18, 21  ## how much you have to move to find the num

unsolved = 255  ## unsolved block colour
## one   -   0,   0, 255
## two   -   0, 128, 0
## three - 255,   0, 0
## four  -   0,   0, 128
## five  - 128,   0, 0
## six   -   0, 128, 128
## seven -   0,   0, 0
## eight - 128, 128, 128

loseFaceX, loseFaceY = 392, 210
winFaceX, winFaceY = 401, 196

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def moveMouse(x, y):
    win32api.SetCursorPos((x, y))

def clickEachBox():
    for i in range(9):
        y = startY + i * 32
        for j in range(9):
           click(startX + j * 32, y)

def randomClicks():
    random_x = random.randint(0, 8) * 32
    random_y = random.randint(0, 8) * 32

    click(startX + random_x, startY + random_y)

def checkNum(x, y):
    num = 0

    if pyautogui.pixel(x, y) == (255, 255, 255):
        return '-'

    match pyautogui.pixel(x + numColX, y + numColY):
        case (0, 0, 255):      ## Blue 1
            num = 1
        case (0, 123, 0):      ## Green 2
            num = 2
        case (255, 0, 0):      ## Red 3
            num = 3
        case (0, 0, 128):      ## Dark blue 4
            num = 4
        case (128, 0, 0):      ## Green 5
            num = 5
        case (0, 128, 128):    ## Cyan 6
            num = 6
        case (0, 0, 0):        ## Black 7
            num = 7
        case (128, 128, 128):  ## Grey 8
            num = 8

    return num

def defineMap():
    grid = [[0 for _ in range(9)] for _ in range(9)]

    for i in range(9):
        y = startY + i * 32

        for j in range(9):
            x = startX + j * 32
            moveMouse(x, y)
            num = checkNum(x, y)
            grid[i][j] = num

    return grid

def dispayMap(grid):
    for i in range(9):
        for j in range(9):
            print(f"{grid[i][j]}  ", end="")
        print()  ## new line

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

    grid = defineMap()
    dispayMap(grid)

    while not keyboard.is_pressed('q') and not state:  ## Kill button
        ## clickEachBox()
        ## randomClicks()
        state, plays = winLose(plays)

if __name__ == "__main__":
    main()
