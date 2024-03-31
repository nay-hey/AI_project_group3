# AI_project_group3
Tetris Gameplay - Score Optimization

Introduction
This is a simple implementation of the classic game Tetris in Python using the Pygame library. Additionally, a basic AI has been included to play the game automatically. Tetris is a tile-matching puzzle game where players manipulate geometric shapes, called tetrominoes, as they fall from the top of the game board to build horizontal lines without any gaps.

Play rules
Just like classical Tetris Game. You use up key to rotate a shape, left key to move left and right key to move right. Also you can use space key to drop down current shape immediately. If you want a pause, just press P key. The right panel shows the next shape.

AI Gameplay
The included simple AI is programmed to move the tetromino to the left until it encounters an obstacle, then it rotates the tetromino. If there's still an obstruction, it moves the tetromino to the right. This process repeats during the AI's gameplay.

Tetris Class Functions:
Here's a breakdown of the functionality of the provided `Tetris` class and its methods:

1. **__init__**: Initializes the game by instantiating objects for the game board, drawing, and clock. It also sets up variables for the game state such as the current and next pieces, score, and game over flag.

2. **poll_attacker_ai**: Implements the AI logic for the attacker. It evaluates potential moves by considering available piece types and their impact on the player's score. Then it selects the piece that decreases the player's score the most.

3. **get_available_types**: Returns a dictionary of available types of tetrominoes that can be used in the game.

4. **find_best_position_rotation**: Finds the best position and rotation for the current tetromino, considering the current state of the game board.

5. **score_types**: Scores each possible move or configuration of a tetromino based on certain criteria, such as the number of holes created.

6. **draw_piece_on_board**: Draws a tetromino piece on the game board.

7. **new_piece**: Generates a new random tetromino piece.

8. **draw_grid**: Draws the game grid on the screen.

9. **draw_piece**: Draws a tetromino piece on the screen.

10. **drop_piece_hard**: Drops the current piece down to the lowest possible position and merges it with the existing grid.

11. **move_piece_down**: Moves the current piece down by one position.

12. **move_piece_left**: Moves the current piece left by one position.

13. **move_piece_right**: Moves the current piece right by one position.

14. **rotate_piece**: Rotates the current piece clockwise.

15. **is_valid_position**: Checks if a piece can be placed at a given position on the grid.

16. **check_collision**: Checks for collisions between a piece and the grid or other pieces.

17. **merge_piece**: Merges a piece with the existing grid when it cannot move further down.

18. **get_column_height**: Calculates the height of a specific column in the grid.

19. **clear_lines**: Clears completed lines from the grid and updates the score.

20. **max_height**: Calculates the maximum height reached by the current piece.

21. **count_holes_in_range**: Counts the number of holes in the grid within a specific height range.

22. **calculate_score**: Calculates a score based on factors such as holes and maximum height.

23. **get_best_move**: Determines the best move for the AI player based on the current game state.

24. **runAIBlock**: Runs the AI-controlled gameplay loop, handling user inputs and AI actions.


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
