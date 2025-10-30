import pyautogui
import time
import keyboard
import random
import win32api, win32con
import threading

running = True  ## shared flag for stopping threads
def watch_for_quit():
    global running
    keyboard.wait('q')  ## block until 'q' is pressed
    running = False
    print("\n[!] Quit key pressed — stopping...")

## first blocks top corner = 258, 256
## Change = 32
## Unknown block RGB = 189, 189, 189

rows, columns = 9, 9
change = 32
startX, startY = 258, 256
numColX, numColY = 18, 21  ## how much you have to move to find the num
flagX, flagY = 8, 9

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

def right_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def move_mouse(x, y):
    win32api.SetCursorPos((x, y))

def click_each_cell():
    for i in range(9):
        y = startY + i * 32
        for j in range(9):
           click(startX + j * 32, y)

def random_clicks():
    random_x = random.randint(0, 8) * 32
    random_y = random.randint(0, 8) * 32

    click(startX + random_x, startY + random_y)

def check_cell_state(x, y):
    num = 0

    if pyautogui.pixel(x + flagX, y + flagY) == (255, 0, 0):
        return 'f'

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

def define_map():
    grid = [[0 for i in range(9)] for j in range(9)]

    for i in range(9):
        y = startY + i * 32

        for j in range(9):
            x = startX + j * 32
            move_mouse(x, y)
            num = check_cell_state(x, y)
            grid[i][j] = num

    return grid

def display_map(grid):
    for i in range(9):
        for j in range(9):
            print(f"{grid[i][j]}  ", end="")
        print()  ## new line

def win_lose(plays):
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

def check_around_cell(grid, i, j, image):
    unknown_count = 0
    flag_count = 0

    for di in [-1, 0, 1]:  ## using delta offsets to get all combinations of 9 cell area
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:  ## skip the cell itself
                continue

            ni, nj = i + di, j + dj  ## using each offset
            if 0 <= ni < rows and 0 <= nj < columns:  ## stay in the game bounds
                x = startX + nj * 32
                y = startY + ni * 32

                color = image.getpixel((x, y))
                if color == (255, 255, 255):
                    unknown_count += 1

                if image.getpixel((x + flagX, y + flagY)) == (255, 0, 0):
                    flag_count += 1

    return unknown_count, flag_count

def flag_around_cell(grid, i, j, image):
    flagged_any = False

    for di in [-1, 0, 1]:  ## using delta offsets to get all combinations of 9 cell area
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:  ## skip the cell itself
                continue

            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < columns:
                if grid[ni][nj] == '-':
                    x = startX + nj * 32
                    y = startY + ni * 32

                    if image.getpixel((x + flagX, y + flagY)) != (255, 0, 0) or grid[ni][nj] != 'f':  ## Check if not already flagged
                        pyautogui.rightClick(x, y)
                        time.sleep(0.05)
                        flagged_any = True
                        grid[ni][nj] = 'f'

    return flagged_any

def flag_area_around_cell(grid):
    image = pyautogui.screenshot()  ## just capture one image for performance
    flagged = False

    for i in range(9):
        for j in range(9):
            val = grid[i][j]
            if val == '-' or val == 0:
                continue

            unknown_count, flag_count = check_around_cell(grid, i, j, image)

            ## skip useless cells
            if flag_count == val or unknown_count == 0:
                continue

            if val == unknown_count:  ## if the value of a cell == the amount of unknowns
                if flag_around_cell(grid, i, j, image):  ## that means we can click the unknown cell
                    flagged = True

    return flagged

def click_solved_cell(grid):
    image = pyautogui.screenshot()  # capture one screenshot for performance

    for i in range(9):
        for j in range(9):
            val = grid[i][j]
            if val == '-' or val == 0:
                continue

            unknown_count, flag_count = check_around_cell(grid, i, j, image)

            if flag_count == val and unknown_count != 0:
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < columns:
                            if grid[ni][nj] == '-':  # unknown cell
                                x = startX + nj * 32
                                y = startY + ni * 32
                                pyautogui.leftClick(x, y)
                                time.sleep(0.05)
                                grid[ni][nj] = '0'  # mark clicked

def auto_flag_loop():
    global running

    plays = 0
    grid = define_map()

    while running:
        changed = flag_area_around_cell(grid)  ## loop through until there are no changes
        state, plays = win_lose(plays)

        if not changed:
            click_solved_cell(grid)
            print("No more flags")
            break

def main():
    global running
    state = False

    threading.Thread(target=watch_for_quit, daemon=True).start()  ## start another thread so we can force quit

    while running and not state:
        click(startX + 4 * 32, startY + 4 * 32)
        auto_flag_loop()

if __name__ == "__main__":
    main()
