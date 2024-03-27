# AI_project_group3
Tetris Gameplay - Score Optimization

Introduction
This is a simple implementation of the classic game Tetris in Python using the Pygame library. Additionally, a basic AI has been included to play the game automatically. Tetris is a tile-matching puzzle game where players manipulate geometric shapes, called tetrominoes, as they fall from the top of the game board to build horizontal lines without any gaps.

Play rules
Just like classical Tetris Game. You use up key to rotate a shape, left key to move left and right key to move right. Also you can use space key to drop down current shape immediately. If you want a pause, just press P key. The right panel shows the next shape.

AI Gameplay
The included simple AI is programmed to move the tetromino to the left until it encounters an obstacle, then it rotates the tetromino. If there's still an obstruction, it moves the tetromino to the right. This process repeats during the AI's gameplay.

Tetris Class Functions:
init: Initializes the Tetris game, creating instances of the Board, Draw, and Clock objects. It also initializes the game grid, sets the current and next pieces, and sets initial game state variables.

poll_attacker_ai: This function is responsible for AI attacker logic. It evaluates potential moves by considering available piece types and their impact on the player's score. It then selects the piece that decreases the player's score the most, simulating the next move.



Board Class Functions:
init: Initializes the game board with default parameters such as width, height, score, high score, and lines cleared. It also loads the high score from a file if available.

load_high_score: Loads the high score from a file. If the file doesn't exist, it returns 0.

save_high_score: Saves the current high score to a file.


Draw Class Functions:
init: Initializes the drawing functionalities, setting parameters such as board dimensions, colors, and fonts.

draw_score: Draws the player's score on the screen.

draw_height: Draws the maximum height reached by the player's stack on the screen.

drawHoles: Draws the number of holes present in the player's stack on the screen.

draw_main_screen: Draws the main menu screen with options for the player to choose game modes.

drawGameOver: Draws the "Game Over" message on the screen when the game ends.

drawPauseScreen: Draws the pause menu screen with instructions for the player.

drawBoard: Draws the game board grid on the screen.

drawStats: Draws various game statistics such as lines cleared, time remaining, score, and high score on the screen.

draw_text_with_highlight: Draws text on the screen with highlighting effect.


