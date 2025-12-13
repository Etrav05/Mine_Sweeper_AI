# Minesweeper AI

A simple AI to play and learn the game of Minesweeper using Q-learning. The AI interacts with a [Web-based](https://minesweeperonline.com/#beginner-200) Minesweeper game, recognizing numbers, flags, and unknown tiles, and deciding actions to maximize its win rate.


## Description

This program automates Minesweeper gameplay by:
* Detecting cell states from a Minesweeper window using screen captures
* Using reinforcement learning (Q-learning) to decide whether to click, flag, or skip a cell
* Continuously improving its strategy over multiple games
* Providing a way to quit anytime by pressing 'q'


## Getting Started

### Dependencies

* Python 3.11+
* Windows 10 or higher
* Python libraries:

```
pip install pyautogui keyboard pywin32
```
* _Minesweeper game must be open on the left side of the screen, zoomed to 200%, and window zoom set to 100%_


### Installing

* Clone or download this repository
* Ensure the Minesweeper game is open and positioned correctly
* Open a terminal in the project directory
* Install dependencies:

```
pip install -r requirements.txt
```
* (or install manually with pip install pyautogui keyboard pywin32)


### Executing Program

1. Run the AI script:
  * python MineSweeping.py
2. The AI will start training and playing automatically
3. Press 'q' at any time to force quit the program
4. During the program, the AI will take actions such as clicking, flagging, and skipping cells, updating its Q-learning model in real-time.

* Notes:
  * Minesweeper window must be visible, set to 9x9 (beginner), and display --> zoom set to 200%
  * Initial coordinates in the script (startX, startY) are set for a standard Minesweeper layout. Adjust if your screen setup differs.


### Help
* If the AI clicks the wrong location, check your screen resolution and Minesweeper zoom (only works on beginner atm)
* Ensure Minesweeper tab is docked to the left of your screen and zoom settings match the script defaults
* For debugging:
  * TODO
* To reset the AI after a win/loss, it types "Etrav" automatically and clicks OK to restart (hopefully)


## Authors

Evan Travis: @Etrav05


## Version History

* 0.7.3
  * Created a discrete state check function
  * This function will reduce the number of states the AI can face, improving training time 


* 0.7.2
  * Refactored all functions to work with the update_Q function
  * Currently don't know if it's learning yet, but it's moving 


* 0.7.1
  * Added functions to:
    * Perform the selected action (random atm)
    * Check action for its reward value
    * Step function to actually call the above functions and move the game state forward
  * Started implementing a function to update the Q value of the AI. This is going to be the brain of the AI in which it will learn (given the reward values) what actions are good or bad


* 0.7.0
  * Started to refactor the program into a real AI
  * Reinforcement learning algorithm --> Q-learning
  * Added functions to:
    * Reset the game board
    * Find the game board's new state
    * Choose a random action (temp)
  * Started implementing a perform action function

* 0.6.1
  * 2 functions were still using pyautogui's click function, updated those
  * This was slowing the program down by so so much

https://github.com/user-attachments/assets/b5daddf4-4ace-4293-a5e5-4e65dfdba72a



* 0.6.0
  * Refactored functions to now take a single screenshot and use "image.getpixel"
  * Refactored grid_definition function to now create the grid cell by cell (rather than an initial 9x9 to be filled)
  * Saves quite a lot of time, program is now averaging ~7 seconds

* 0.5.0
  * Fixed flagging (again)
  * Added a function to click solved cells (value == amount of flags in the 3x3 area)
  * Redid the logic:
    * program will now create a 2d array of the game board
    * Check for flags
    * Click solved cells
    * Repeat
  * Slow at the moment (~12sec)

https://github.com/user-attachments/assets/00379284-0df8-45e1-99f2-68e79f9fc893

* 0.4.1
  * Flagging function now works properly

* 0.4.0
  * Renamed functions
  * Added a function to place flags around a cell
  * Started a function to click cells which are determined to be safe

* 0.3.2
  * Game board is now saved as a 2d array
  * Added a function to display this 2d array

* 0.3.1
  * Added a function to define the game board
  * Detects all block states: Unsolved, solved, 1, 2, 3, ..., 8
  * Bombs are ignored at the moment
  
* 0.2.1
   * Refactored the solution
   * Followed better modularity - created functions to be called in the main  

* 0.2
    * Added ability to randomly click tiles on a 9x9 board
    * Auto resets lost games
    * Took 4406 retries to beat its first game (with a score of 1sec)
    * <img width="330" height="125" alt="image" src="https://github.com/user-attachments/assets/48d57273-3f6c-4b0d-9586-e43a7491e1b1" />

* 0.1
    * Initial Release

## Acknowledgments


* https://www.youtube.com/watch?v=ehAStJmx_Fo 
* https://www.youtube.com/watch?v=YRAIUA-Oc1Y
* https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc#file-readme-template-md
