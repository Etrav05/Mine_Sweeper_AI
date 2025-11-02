# Mine Sweeper AI

A simple AI to beat the game of "Minesweeper"

## Description

TODO

## Getting Started

### Dependencies

TODO
* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

TODO
* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program


* Minesweeper tab is docked on the left side of your screen
* Game display is set to 200%
* Zoom in on the tab is set to 100%
```
code blocks for commands
```

## Help

TODO
Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Evan Travis
@Etrav05

## Version History


* 0.6.0
  * Refactored functions to now take a single screenshot and use "image.getpixel"
  * Refactored grid_definition function to now create the grid cell by cell (rather than an initial 9x9 to be filled)
  * Saves quite a lot of time, AI is now averaging ~7 seconds

* 0.5.0
  * Fixed flagging (again)
  * Added a function to click solved cells (value == amount of flags in the 3x3 area)
  * Redid the logic:
    * AI will now create a 2d array of the game board
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
