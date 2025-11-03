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

def check_cell_state(x, y, image):
    num = 0

    if image.getpixel((x + flagX, y + flagY)) == (255, 0, 0):
        return 'f'

    if image.getpixel((x, y)) == (255, 255, 255):
        return '-'

    match image.getpixel((x + numColX, y + numColY)):
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

def define_map(image):
    grid = []

    for i in range(rows):
        row = []
        y = startY + i * change
        for j in range(columns):
            x = startX + j * change
            cell_state = check_cell_state(x, y, image)
            row.append(cell_state)
        grid.append(row)

    return grid

def display_map(grid):
    for i in range(9):
        for j in range(9):
            print(f"{grid[i][j]}  ", end="")
        print()  ## new line

def check_around_cell(i, j, image):
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

    return flag_count, unknown_count

ok_buttonX = 560
ok_buttonY = 240

## Functions to make this program a Reinforcement Learning AI --> Q-learning

## Q-learning variables
Q_dictionary = {}  ## Quality dictionary --> (state, action), value

## All caps, so we can use them everywhere (hyperparameters)
ALPHA = 0.5    ## learning rate
GAMMA = 0.9    ## reward loss
EPSILON = 0.1  ## exploration probability

actions = ["click", "flag", "skip"]

def get_all_unknowns(grid):
    return [(i, j) for i in range(rows) for j in range(columns) if grid[i][j] == '-']

def get_cell_info(cell_i, cell_j, grid, image):
    cell_value = grid[cell_i][cell_j] if grid[cell_i][cell_j] != '-' else 0

    flags, unknowns = check_around_cell(cell_i, cell_j, image)
    return cell_value, flags, unknowns

def get_state(cell_value, flags_around, unknowns_around):
    return (cell_value, flags_around, unknowns_around)

def pick_random_unknown(unknown_cells):
    if not unknown_cells:
        return None, None
    cell = random.choice(unknown_cells)
    unknown_cells.remove(cell)
    return cell


def reset():
    keyboard.write("Etrav")  # type name for wins
    click(ok_buttonX, ok_buttonY)
    click(winFaceX, winFaceY)
    click(400, 400)  # center of the board

    image = pyautogui.screenshot()
    grid = define_map(image)
    unknown_cells = get_all_unknowns(grid)

    first_cell = pick_random_unknown(unknown_cells)
    if first_cell:
        cell_i, cell_j = first_cell
        cell_value, flags, unknowns_around = get_cell_info(cell_i, cell_j, grid, image)
        state = get_state(cell_value, flags, unknowns_around)
    else:
        cell_i = cell_j = None
        state = None

    return grid, unknown_cells, cell_i, cell_j, state

def new_state_finder(image, grid, unknown_cells):
    i, j, cell_value = pick_random_unknown(unknown_cells)

    if i is None:
        return None, None, None, None, None, grid

    flags, unknowns = check_around_cell(i, j, image)

    return cell_value, i, j, flags, unknown_cells, grid

def choose_action(state):
    if state not in Q_dictionary:  ## If we come up to a new action, add it
        Q_dictionary[state] = {a: 0.0 for a in actions}

    if random.random() < EPSILON:  ## Choose a random action sometimes
        return random.choice(actions)
    else:  ## Else just go with the action that has had the best return (reward)
        return max(Q_dictionary[state], key=Q_dictionary[state].get)

def perform_action(action, cell_i, cell_j):
    match action:
        case "click":
            click(startX + cell_i * 32, startY + cell_j * 32)
        case "flag":
            right_click(startX + cell_i * 32, startY + cell_j * 32)
        case "skip":
            return 0

def reward_check(cell_i, cell_j, image):
    done = False

    if image.getpixel((startX + cell_i * 32, startY + cell_j * 32)) == (255, 0, 0):
        return -10, True  ## hit a bomb and failed

    if image.getpixel((winFaceX, winFaceY)) == (0, 0, 0):
        return 50, True  ## Finished the board and won

    num = check_cell_state(cell_i, cell_j, image)
    if 0 < num < 9:  ## Hit a number
        reward = 1
    else:
        reward = 0  ## Skipped

    return reward, done

def step(action, cell_i, cell_j, grid, unknown_cells):
    perform_action(action, cell_i, cell_j)
    image = pyautogui.screenshot()

    reward, done = reward_check(cell_i, cell_j, image)

    grid[cell_i][cell_j] = check_cell_state(cell_i, cell_j, image) or 0  ## update grid cell

    next_cell = pick_random_unknown(unknown_cells)
    if next_cell:
        ni, nj = next_cell
        cell_value, flags, unknowns = get_cell_info(ni, nj, grid, image)
        next_state = get_state(cell_value, flags, unknowns)
        return reward, next_state, done, ni, nj
    else:
        return reward, None, done, None, None

def update_Q(state, action, reward, next_state):
    if next_state not in Q_dictionary:
        Q_dictionary[next_state] = {a: 0.0 for a in actions}

    max_next = max(Q_dictionary[next_state].values())

    ## Q-learning function :)
    Q_dictionary[state][action] += ALPHA * (reward + GAMMA * max_next - Q_dictionary[state][action])


def main():
    global running
    threading.Thread(target=watch_for_quit, daemon=True).start()  ## start another thread so we can force quit

    for training in range(500):
        state_grid = define_map(pyautogui.screenshot())
        unknown_cells = get_all_unknowns(state_grid)

        cell = pick_random_unknown(unknown_cells)
        if not cell:
            continue
        cell_i, cell_j = cell
        cell_value, flags, unknowns = get_cell_info(cell_i, cell_j, state_grid, pyautogui.screenshot())
        current_state = get_state(cell_value, flags, unknowns)

        grid, unknown_cells, cell_i, cell_j, current_state = reset()
        done = False

        while running and not done and unknown_cells:
            action = choose_action(current_state)
            reward, next_state, done, next_i, next_j = step(action, cell_i, cell_j, grid, unknown_cells)

            if next_state:
                update_Q(current_state, action, reward, next_state)
                current_state = next_state
                cell_i, cell_j = next_i, next_j
            else:
                update_Q(current_state, action, reward, current_state)
                done = True

if __name__ == "__main__":
    main()
