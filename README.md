# 2048 Solver
2048 is a game in which a player must combine like-number blocks within a grid until they form a 2048 block. This game takes place within a square grid and has four directional controls: up, down, left, and right, which will move all blocks into the chosen direction.

Explanation of how to play: https://play2048.co/

The files in this repository attempt to achieve the 2048 block in a random 2048 game.

## The 2048 Game
The 2048 game is created by starting with an empty grid. Traditionally, this game has both a length and height of 4, allowing for 16 different blocks to be within the grid at a time. All files in this repository can have the width and height changed by manipulating the `GRID_LENGTH` constant. Upon a movement, the `move` function forces all blocks in the corresponding direction and a new block, with a 90% chance of having a value of 2 and a 10% chance of having a value of 4, is spawned in an empty cell using the `new_block` function. The game is won upon the achievement of the 2048 block. The game ends when there are no more valid moves.

![Screenshot 2024-09-19 185449](https://github.com/user-attachments/assets/7ab8d5c2-d261-4ae1-9dd6-5c2e5a4e52e8)

## Solver With Playing
The file under the name `solver-display.py` creates a playable 2048 experience and display of the solver using the pygame library. 

### Playable 2048
To make a directional move, a player can use 'a', 'w', 's', and 'd' to move left, up, down, and right respectively, or their corresponding arrow keys. Regardless of whether a 2048 block has been achieved, the player plays until the game ends. The colors used are based on the traditional 2048 block colors but can be easily changed by changing the `colors` dictionary.

### The Solver
To toggle the solver on and off, a player can press the 'p' key. Once toggled on, the solver uses the `ai_run` function to find optimal moves in the 2048 game. This evaluation is found by searching through the all possible moves throughout the next 3 turns. These future positions are evaluated by the `score` function which uses constant weights and specific rules in order to "score" each position. Using these positions, with scores decreasing as they lie further in the future, the four possible moves are compared to see which move is optimal and has a higher chance of yielding better results. This function will always work since it will not make a move that is not valid. This solver runs infinitely and will reset in any case of a game over.

## Solver With Only Results
The file under the name `solver-only-results.py` runs the solver without a pygame display. This file uses the same `ai_run` function as the display file does and uses the exact same method of solving as well. Although, this solver begins as soon as the program is run and upon finding a solution, the amount of time taken and highest block reached is printed.
