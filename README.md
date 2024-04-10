# AI_project_group3
Tetris Gameplay - Score Optimization

Introduction
This is a simple implementation of the classic game Tetris in Python using the Pygame library. Additionally, a basic AI has been included to play the game automatically. Tetris is a tile-matching puzzle game where players manipulate geometric shapes, called tetrominoes, as they fall from the top of the game board to build horizontal lines without any gaps.

Play rules
Just like classical Tetris Game. You use up key to rotate a shape, left key to move left and right key to move right. Also you can use space key to drop down current shape immediately. If you want a pause, just press P key. The right panel shows the next shape.

AI Gameplay
The included simple AI is programmed to move the tetromino to the left until it encounters an obstacle, then it rotates the tetromino. If there's still an obstruction, it moves the tetromino to the right. This process repeats during the AI's gameplay.


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

1. ### `load_high_score(self)` / `save_high_score(self)`:

- **Functionality**:
    - `load_high_score`: Loads the high score from a file named "high_score.txt".
    - `save_high_score`: Saves the current high score to the "high_score.txt" file.

- **Explanation**:
    - Both functions interact with the "high_score.txt" file to manage the high score.
    - `load_high_score` attempts to read the high score from the file. If the file doesn't exist or cannot be opened, it returns a default value of 0.
    - `save_high_score` writes the current high score (stored in `self.high_score`) to the "high_score.txt" file, updating it with the new value.
 
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

- **drop_piece_hard(self)**:
  - Drops the current piece directly to the lowest possible position in the grid, merging it with existing blocks.
  - If the dropped piece causes a collision, it triggers game over.

- **drop_piece_hard1(self, current_piece, piece_x, piece_y, grid_copy)**:
  - Similar to `drop_piece_hard`, this function drops the given piece to the lowest possible position in the grid, without updating the game state. Instead, it operates on a copy of the grid.
  
- **move_piece_down**:
  - Moves the current piece one step down in the grid.
  - If the piece cannot move down further due to a collision, it merges with existing blocks, and a new piece is generated.
  
- **move_piece_left** / **move_piece_right**:
  - These functions move the current piece one step to the left/right in the grid if the move is valid.
  
- **rotate_piece(self, grid=None, current_piece=None, piece_x=None, piece_y=None)**:
  - Rotates the current piece clockwise if the rotation does not result in a collision.
  
- **is_valid_position(self, piece, x, y, grid)**:
  - Checks if a given piece can be placed at a specified position on the grid without causing any collisions or going out of bounds.

- **check_collision(self, piece, offset_x, offset_y, grid=None)**:
  - Checks if there is a collision between the given piece and the grid at the specified offset position.
    
- **merge_piece(self, grid=None, current_piece=None, piece_y=None, piece_x=None)**:
  - Merges the current piece into the grid at the specified position.
   
- **clear_lines(self, grid=None)**:
  - Clears any complete lines in the grid and updates the score accordingly.
    
- **max_height(self, piece, offset_x, offset_y)**:
  - Computes the maximum height of a piece placed at the specified offset on the grid.

- **count_holes_in_range(self, max_height=None, grid=None)**:
  - Counts the number of holes in the grid within the specified height range.
    
- **get_clear_lines(self, grid_copy)**:
  - Determines the number of complete lines in a copy of the grid.
 
### These functions are related to the AI-controlled block generation in the game. Here's a brief explanation for each function:

- **poll_attacker_ai(self, piece_x_copy, piece_y_copy)**:
  - Selects the worst possible piece type for the AI attacker based on the current game state and player's grid.
  
- **get_available_types(self)**:
  - Returns a dictionary of available types of tetrominoes that can be used in the game. Each type appears only once in this implementation.
  
- **score_types(self, available_types, piece_x_copy, piece_y_copy)**:
  - Assigns scores to each available tetromino type based on various metrics such as hole difference, tallest column, and lines cleared after simulation.
  
- **find_best_position_rotation(self, pit, current_piece)**:
  - Finds the best position and rotation for the current tetromino considering the current state of the game board. Placeholder implementation, always returning the same position and rotation.
  
- **lines_cleared(self, board)**:
  - Counts the number of lines cleared in the given board configuration.
  
- **pieces_to_clear_lines(self, board)**:
  - Simulates clearing lines on the board and counts the number of pieces required to clear those lines.

These functions collectively contribute to the AI's decision-making process for generating and placing blocks strategically to maximize its effectiveness in the game.
