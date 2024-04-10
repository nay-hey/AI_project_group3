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

### CLASS PIECES :

1. ### `calc_skirt()` function :
This function calculates the skirt of a Tetromino piece, which represents the lowest height at each column of the piece.
- It iterates over each column of the piece.
- For each column, it finds the lowest block and records its height.
- The function returns a list containing the minimum height for each column.

2. ### `get_next_rotation()` function:
This function rotates a Tetromino piece clockwise by 90 degrees and returns the rotated piece
- Calculates the width of the piece.
- Applies a clockwise rotation to the piece's coordinates.
- Adjusts the coordinates to stay within the board boundaries.
- Returns a new Piece object representing the rotated piece.

### CLASS GREEDY_AI :

1. ### `get_best_move(self, board, piece, depth=1)`:

- **Performs a heuristic search of depth 1**: 
    - This means that the AI considers only one level of moves ahead. It evaluates the current state of the board and the available pieces to determine the best move for the current turn.

- **Generates all possible placements with the current piece**:
    - The AI iterates over all possible horizontal positions and rotations of the current piece on the board. For each position, it evaluates the cost associated with placing the piece there.

- **Chooses the placement that minimizes the cost function**:
    - After generating all possible placements, the AI calculates the cost associated with each placement using the `cost()` function. It then selects the placement with the lowest cost as the best move.

2. ### `cost(self, board, x, y, piece)`:

- **Calculates the cost of a specific placement of a piece on the board**:
    - This function evaluates the desirability of placing a piece at a particular position on the board.

- **The cost function is defined as the sum of**:
    - **Number of holes in the board**: Holes are empty spaces in the board that are covered by blocks above. More holes generally indicate a higher cost.
    - **Maximum height of the board**: The maximum height of the board after placing the piece. Higher heights usually increase the cost.
    - **Number of cleared lines**: The AI rewards clearing lines as it reduces the board's congestion and provides more room for future placements.
    - **Aggregate height of the columns**: This measures the sum of heights of all columns in the board. Higher aggregate heights contribute to a higher cost.
    - **Bumpiness of the board (variation in column heights)**: Bumpiness quantifies the unevenness of the column heights. Higher bumpiness adds to the cost as it makes the board harder to manage.

### CLASS BOARD :

1. ### `load_high_score(self)`:

- **Function**:
    - Loads the high score from a file named "high_score.txt".

- **Explanation**:
    - Tries to open the "high_score.txt" file in read mode.
    - Reads the content of the file and converts it to an integer, representing the high score.
    - If the file doesn't exist or cannot be opened, it returns a default value of 0.

2. ### `save_high_score(self)`:

- **Function**:
    - Saves the current high score to a file named "high_score.txt".

- **Explanation**:
    - Opens the "high_score.txt" file in write mode.
    - Writes the current high score (stored in the `self.high_score` attribute) to the file as a string.
    - Overwrites the existing content of the file with the new high score.
 
### CLASS DRAW :

###  `draw_score()`: Draws the player's score on the screen.

###  `draw_height()`: Draws the maximum height reached on the screen.

###  `drawHoles()`: Draws the number of holes present on the screen.

###  `draw_main_screen()`: Draws the main menu screen with various options for the player.

These functions handle the visualization of important game information and the main menu interface, providing essential feedback to the player and allowing them to interact with the game.

Here's a concise explanation for the `drawGameOver()` and `drawPauseScreen()` methods suitable for a README file:

### `drawGameOver(self)`:

- **Function**:
    - Draws the "Game Over" message on the screen when the game ends.

- **Explanation**:
    - Uses the provided font file to render the text "GAME OVER" in a large font size.
    - Places the text at the center of the screen to notify the player about the game's end.

### `drawPauseScreen(self)`:

- **Function**:
    - Draws the pause menu screen with various instructions for the player.

- **Explanation**:
    - Renders different text lines for menu options such as "New Game," "Pause/Unpause," etc., using the provided font file.
    - Each option is highlighted with a different color to improve readability.
    - The text is positioned at specific coordinates on the screen to create a visually organized menu interface.

### CLASS TETROMINO :
Here's a brief explanation of the `Tetromino` class in two bullet points:

- **Shapes**: 
  - Defines the shapes of all Tetromino pieces using a nested list structure, where each sublist represents a shape with numerical values indicating the presence of blocks. 
  - Each shape is represented by a unique combination of numbers, and the numbers are mapped to block images using the `BLOCK_IMAGES` dictionary.

- **Block Images**: 
  - Maps numerical block values to corresponding image filenames, allowing the graphical representation of Tetromino pieces.
  - Provides a convenient way to associate visual representations with the numerical values used to define Tetromino shapes.
 
### CLASS TETRIS : 

- **new_piece(self)**: Randomly selects a Tetromino shape from predefined shapes and sets it as the next piece to be used in the game.
- Here are concise explanations of the functions using game terminology, suitable for a README file:

- **drop_piece_hard(self)**:
  - Drops the current piece directly to the lowest possible position in the grid, merging it with existing blocks.
  - If the dropped piece causes a collision, it triggers game over.

- **drop_piece_hard1(self, current_piece, piece_x, piece_y, grid_copy)**:
  - Similar to `drop_piece_hard`, this function drops the given piece to the lowest possible position in the grid, without updating the game state. Instead, it operates on a copy of the grid.
  
- **move_piece_down(self)**:
  - Moves the current piece one step down in the grid.
  - If the piece cannot move down further due to a collision, it merges with existing blocks, and a new piece is generated.
  
- **move_piece_left(self, grid=None, current_piece=None, piece_x=None, piece_y=None)**:
  - Moves the current piece one step to the left in the grid if the move is valid.
  
- **move_piece_right(self, grid=None, current_piece=None, piece_x=None, piece_y=None)**:
  - Moves the current piece one step to the right in the grid if the move is valid.
  
- **rotate_piece(self, grid=None, current_piece=None, piece_x=None, piece_y=None)**:
  - Rotates the current piece clockwise if the rotation does not result in a collision.
  
- **is_valid_position(self, piece, x, y, grid)**:
  - Checks if a given piece can be placed at a specified position on the grid without causing any collisions or going out of bounds.

These functions handle the movement, rotation, and validation of Tetromino pieces within the game grid, ensuring smooth gameplay and enforcing game rules.
