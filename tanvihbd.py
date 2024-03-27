import pygame
import random
import copy
import sys
from collections import deque

# Define constants
pygame.init()  # Initializing pygame

display_h = pygame.display.Info().current_h  # system's height
BLOCK_SIZE = display_h // 30
SCREEN_HEIGHT = 25 * BLOCK_SIZE
SCREEN_WIDTH = SCREEN_HEIGHT + 10
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # initializes the game screen with given dimensions
pygame.display.set_caption("Tetris_group3")  # sets the title of the screen
bg = pygame.image.load('bg.jpg').convert()
screen.blit(bg, (0, 0))

time = 5000
timer_seconds = time  # the game is timed using this variable as a counter and gets over after these many seconds

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)


class Board:  # defining functions for the tetris game's grid

    def __init__(self, colour="Black"):
        self.colour = colour
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 20
        self.score = 0
        self.high_score = self.load_high_score() 
        self.linesCleared = 0  # to keep track of score
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

class Draw:
    def __init__(self):
        self.board = Board()
        self.height = self.board.GRID_HEIGHT 
        self.boardWidth = 10
        self.boardOffset = (BLOCK_SIZE // 5) # leaves some left margin before start of the grid
        self.boardOutline = (BLOCK_SIZE // 15) if (BLOCK_SIZE >= 15) else 1  # to see individual cells in board
        self.pieceOutline = (BLOCK_SIZE // 15) if (BLOCK_SIZE >= 15) else 1  # to see tetromino piece in board
        self.boardRect = pygame.Rect(self.boardOffset * BLOCK_SIZE, self.boardOffset * BLOCK_SIZE,
                                      (self.boardWidth * BLOCK_SIZE) + self.boardOutline,
                                      self.board.GRID_HEIGHT - self.boardOffset)
        self.fontColour = (255, 0, 50)  # font colour
        self.fontColour1="orange"
    def draw_score(self, score, fontColour, boardOffset, height):
        fontSize = int(1.5 * BLOCK_SIZE)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
        score_text = gameFont.render("Score: " + str(score), True, self.fontColour1)
        screen.blit(score_text, ((boardOffset + 11) * BLOCK_SIZE, (height / 2 - 2) * BLOCK_SIZE))

    def draw_height(self, height, fontColour, boardOffset, height1):
        fontSize = int(1.5 * BLOCK_SIZE)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
        height_text = gameFont.render("Max Height: " + str(height), True, self.fontColour1)
        screen.blit(height_text, ((boardOffset + 11) * BLOCK_SIZE, (height1 / 2 - 4) * BLOCK_SIZE))

    def drawHoles(self, num_holes, fontColour, boardOffset, height):
        fontSize = int(1.5 * BLOCK_SIZE)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
        holeText = gameFont.render("Holes:"+ str(num_holes), True, self.fontColour1)
        pauseYpos=int(self.height * 0.2)+14
        screen.blit(holeText, ((self.boardOffset + 11) * BLOCK_SIZE, (pauseYpos + 2) * BLOCK_SIZE))
       # holeNum = gameFont.render(str(num_holes), True, fontColour)
        #screen.blit(holeNum, ((boardOffset + 15) * BLOCK_SIZE, (height / 2 - 6) * BLOCK_SIZE))
        
    def draw_main_screen(self):
        self.draw_text_with_highlight("WELCOME TO TETRIS!", (self.boardWidth // 2 - 1.5) * BLOCK_SIZE,
                                    ((self.board.GRID_HEIGHT / 2) - 8) * BLOCK_SIZE,
                                    highlight_color=(20, 0, 200))

        self.draw_text_with_highlight("PRESS  A  :  AI MODE", (self.boardWidth // 2 - 1) * BLOCK_SIZE,
                                    ((self.board.GRID_HEIGHT / 2) - 5) * BLOCK_SIZE,
                                    highlight_color=(20, 200, 20))

        self.draw_text_with_highlight("PRESS  R  : RANDOM BLOCK", (self.boardWidth // 2 - 1) * BLOCK_SIZE,
                                    ((self.board.GRID_HEIGHT / 2) -1) * BLOCK_SIZE,
                                    highlight_color=(100, 190, 200))

        self.draw_text_with_highlight("PRESS  I  :  AI GENERATED BLOCK", (self.boardWidth // 2 - 1) * BLOCK_SIZE,
                                    ((self.board.GRID_HEIGHT / 2) + 5) * BLOCK_SIZE,
                                    highlight_color=(200, 200, 200))

        self.draw_text_with_highlight("PRESS  J  :  AI VS AI", (self.boardWidth // 2 - 1) * BLOCK_SIZE,
                                    ((self.board.GRID_HEIGHT / 2) + 8) * BLOCK_SIZE,
                                    highlight_color=(200, 200, 200))

    def drawGameOver(self):
        self.draw_text_with_highlight("GAME OVER", BLOCK_SIZE * (self.boardWidth // 2 + 2),
                                    ((self.board.GRID_HEIGHT // 2) - 2) * BLOCK_SIZE)  # Update here
 


    def drawPauseScreen(self):
        self.draw_text_with_highlight("Game Menu!", (self.boardWidth // 2 + self.boardOffset - 1) * BLOCK_SIZE,
                                      3 * BLOCK_SIZE, highlight_color=(80, 190, 200))
        self.draw_text_with_highlight("N:                        New Game", (self.boardWidth // 2) * BLOCK_SIZE,
                                      7 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("P:                        Pause/Unpause", (self.boardWidth // 2) * BLOCK_SIZE,
                                      9 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("Left Arrow:         Move Left", (self.boardWidth // 2) * BLOCK_SIZE,
                                      11 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("Right Arrow:      Move Right", (self.boardWidth // 2) * BLOCK_SIZE,
                                      13 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("Up Arrow:          Rotate", (self.boardWidth // 2) * BLOCK_SIZE,
                                      15 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("Down Arrow:          Move down", (self.boardWidth // 2) * BLOCK_SIZE,
                                      17 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("Space:               Hard Drop", (self.boardWidth // 2) * BLOCK_SIZE,
                                      19 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))

    def drawBoard(self, board):
        pygame.draw.rect(screen, board.colour, self.boardRect)
        for x in range(self.boardOffset, (self.boardWidth + self.boardOffset)):
            for y in range(self.boardOffset, self.height + self.boardOffset):
                cell = pygame.Rect(x * BLOCK_SIZE + self.boardOutline,
                                   y * BLOCK_SIZE + self.boardOutline,
                                   BLOCK_SIZE - self.boardOutline, BLOCK_SIZE - self.boardOutline)
                pygame.draw.rect(screen, "White", cell)

    def drawStats(self, board, timer_seconds):
        fontSize = int(1.5 * BLOCK_SIZE)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
        timeText = gameFont.render("Time remaining", True, self.fontColour1)
        lineNum = gameFont.render(str(board.linesCleared), True, self.fontColour1)
        lineText = gameFont.render("Lines cleared", True, self.fontColour1)
        pauseText = gameFont.render("Press P to pause", True, self.fontColour1)
        nextYPos = int(self.height * 0.2)
        timeYPos = nextYPos + 6
        lineYPos = timeYPos + 4
        pauseYpos = lineYPos + 4
        screen.blit(timeText, ((self.boardOffset + 11) * BLOCK_SIZE, (timeYPos) * BLOCK_SIZE))
        screen.blit(lineText, ((self.boardOffset + 11) * BLOCK_SIZE, lineYPos * BLOCK_SIZE))
        screen.blit(lineNum, ((self.boardOffset+15)*BLOCK_SIZE, (lineYPos+1.5)*BLOCK_SIZE))
        screen.blit(pauseText, ((self.boardOffset + 11) * BLOCK_SIZE, pauseYpos * BLOCK_SIZE))
        score_text = gameFont.render("Score: {}".format(board.score), True, self.fontColour1)
        high_score_text = gameFont.render("High Score: {}".format(board.high_score), True, self.fontColour1)
        #screen.blit(score_text, ((self.boardOffset + 11) * BLOCK_SIZE, (pauseYpos + 2) * BLOCK_SIZE))
        screen.blit(high_score_text, ((self.boardOffset + 11) * BLOCK_SIZE, (pauseYpos + 4) * BLOCK_SIZE))
        

        time_surface = gameFont.render(str(timer_seconds), True, self.fontColour1)
        screen.blit(time_surface, ((self.boardOffset + 15) * BLOCK_SIZE, (timeYPos + 1.5) * BLOCK_SIZE))

    def draw_text_with_highlight(self, text, x, y, fontSize=int(2 * BLOCK_SIZE), highlight_color=(250, 200, 0)):
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
        text_surface = gameFont.render(text, True, self.fontColour)
        rect = text_surface.get_rect()
        rect.topleft = (x, y)
        pygame.draw.rect(screen, highlight_color, rect)
        screen.blit(text_surface, rect.topleft)

    def getScaledCoords(self, vertexCoords):
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + self.boardOffset) * BLOCK_SIZE
            coord[1] = (coord[1] + self.boardOffset) * BLOCK_SIZE
        return copyCoords

    def getScaledCoords1(self, vertexCoords):
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + self.boardWidth + self.boardOffset - 1) * BLOCK_SIZE
            coord[1] = (coord[1] + self.boardOffset + 2) * BLOCK_SIZE
        return copyCoords


class Tetromino:
    SHAPE_COLORS = [
    (255, 0, 0),     # Red (for I)
    (255, 165, 0),   # Orange (for T)
    (255, 255, 0),   # Yellow (for L)
    (0, 128, 0),     # Green (for J)
    (0, 0, 255),     # Blue (for S)
    (255, 105, 180), # Pink (for O)
    (128, 0, 128),   # Purple (for Z)
    #(0, 255, 255),   # Cyan (for Snake)
    #(255, 192, 203), # Light Pink (for Difficult Tetromino 1)
    #(70, 130, 180),  # Steel Blue (for Difficult Tetromino 2)
    #(154, 205, 50),  # Yellow Green (for Difficult Tetromino 3)
    #(255, 20, 147)   # Deep Pink (for Difficult Tetromino 4)
]

    SHAPES = [
    [[1, 1, 1, 1]],  # I - Red
    [[2, 2, 2], [0, 2, 0]],  # T - Orange
    [[3, 3, 3], [3, 0, 0]],  # L - Yellow
    [[4, 4, 4], [0, 0, 4]],  # J - Green
    [[0, 5, 5], [5, 5, 0]],  # S - Blue
    [[6, 6], [6, 6]],  # O - Pink
    [[7, 7, 0], [0, 7, 7]],  # Z - Purple
    #[[0, 0, 8], [8, 8, 8]],  # Snake - Cyan
    #[[9, 0, 0], [9, 9, 9]],  # Difficult Tetromino 1 - Light Green
    #[[0, 0, 10], [10, 10, 10]],  # Difficult Tetromino 2 - Light Blue
    #[[11, 11], [0, 11], [0, 11]],  # Difficult Tetromino 3 - Light Pink
    #[[0, 12, 0], [12, 12, 12], [0, 12, 0]],  # Difficult Tetromino 4 - Light Purple
    ]
    @staticmethod
    def rotate(piece, rotation):
        rotated_piece = piece
        for _ in range(rotation):
            rotated_piece = [list(row) for row in zip(*rotated_piece[::-1])]
        return rotated_piece


class Tetris:
    def __init__(self):
        self.board = Board()  # Instantiate Board object
        self.drawer = Draw()
        self.clock = pygame.time.Clock()
        self.grid = [[0] * self.board.GRID_WIDTH for _ in range(self.board.GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.piece_x = self.board.GRID_WIDTH // 2 - len(self.current_piece[0]) // 2#offset for drawing the piece
        self.piece_y = 0
        self.sum1=0
        self.last_type = None
    def poll_attacker_ai(self, piece_x_copy, piece_y_copy):
        # AI attacker logic
        # Calculate the impact of each possible next piece on the player's score
        # Choose the piece that decreases the player's score the most
        
        # Get available types, excluding the last used piece
        available_types = list(self.get_available_types().keys())
        current_piece = self.current_piece
        if self.last_type is not None:
        # Check if any rotation of the last piece exists in available types
            last_piece_rotations = [Tetromino.rotate(self.current_piece, i) for i in range(5)]
            for rotation in last_piece_rotations:
                if rotation in Tetromino.SHAPES:
                    current_piece = rotation
                    available_types.remove(Tetromino.SHAPES.index(current_piece))
                    break
        scores = self.score_types(available_types, piece_x_copy, piece_y_copy)
        
        worst_score = float('inf')  # Initialize worst score to positive infinity
        worst_types = []
        
        for piece_type, score in scores.items():
            if score <= worst_score:  # Choose the piece that worsens the player's score the most
                worst_score = score
                worst_types.append(piece_type)
        
        piece_type = random.choice(worst_types)
        self.sum1= self.sum1 +  worst_score
        
        #print(self.sum1, "...........................")
        self.last_type = Tetromino.SHAPES.index(current_piece)
        self.next_piece = Tetromino.SHAPES[piece_type]
    def get_available_types(self):
        """
        Returns a dictionary of available types of tetrominoes that can be used in the game.
        The keys are the types (0-indexed) and the values could be the counts of each type.
        """
        return {i: 1 for i in range(len(Tetromino.SHAPES))}  # In this example, each type appears only once.

    def find_best_position_rotation(self, pit, current_piece):
        """
        Finds the best position and rotation for the current tetromino, considering the current state of the game board.
        This function should implement the logic to evaluate potential positions and rotations.
        """
        # Placeholder implementation, always returns the same position and rotation.
        return {"x": 0, "rotation": 0}
    def score_types(self, available_types, piece_x_copy, piece_y_copy):
        scores = {}
        #print(self.current_piece)
        
        for type_ in available_types:
            temp_board = copy.deepcopy(self.grid)
            temp_piece = Tetromino.SHAPES[type_]
            
            # Initialize worst score to positive infinity
            worst_score = float('-inf')
            self.drop_piece_hard1(self.current_piece, piece_x_copy, piece_y_copy, temp_board)
            # Iterate over all possible rotations of the current piece
            for rotation in range(4):
                rotated_piece = temp_piece
                for _ in range(rotation):
                    rotated_piece = Tetromino.rotate(rotated_piece, 1)
                    
                # Find the best position and rotation to place the rotated piece on the board
                best_position_rotation = self.find_best_position_rotation(temp_board, rotated_piece)
                best_position = best_position_rotation["x"]
                
                # Simulate dropping the rotated piece onto the temporary board
                self.drop_piece_hard1(rotated_piece, piece_x_copy, piece_y_copy, temp_board)
                
                # Calculate various metrics after rotation
                max_height = sum(1 for row in temp_board if any(row))
                #print(temp_piece, "++++++++++++++++++++")
                #print(max_height,"-----------")
                #print(temp_board)
                num_holes_before = self.count_holes_in_range(max_height, self.grid)
                num_holes_after = self.count_holes_in_range(max_height, temp_board)
                holes_difference = num_holes_after - num_holes_before
                #print(holes_difference, "\\\\\\\\\\\\\\\\\\\\\\")
                lines_cleared = self.lines_cleared(temp_board)
                #print(temp_piece, holes_difference, "##########################")
                
                pieces_to_clear_lines = self.pieces_to_clear_lines(temp_board)
                #print(pieces_to_clear_lines, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")
                
                # Assign scores based on multiple factors after rotation
                # Adjust weights to make the choice even worse for the player
                score = holes_difference * 10 - lines_cleared * 2000 - pieces_to_clear_lines * 50
                if score > worst_score:
                    worst_score = score
            
            scores[type_] = worst_score
        #print(scores)
        return scores

    def lines_cleared(self, board):
        lines = 0
        for row in board:
            if all(row):
                lines += 1
        return lines

    def pieces_to_clear_lines(self, board):
        # Simulate clearing lines and count the number of pieces required
        temp_board = [row[:] for row in board]
        lines_to_clear = self.lines_cleared(temp_board)
        pieces_required = 0
        while lines_to_clear > 0:
            # Drop pieces to clear lines
            for row in reversed(range(len(temp_board))):
                if all(temp_board[row]):
                    del temp_board[row]
                    temp_board.insert(0, [0] * len(temp_board[0]))
                    pieces_required += 1
                    lines_to_clear -= 1
                    break
        return pieces_required
    def draw_piece_on_board(self, piece, temp_board, offset_x, offset_y):
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x]:
                    color = Tetromino.SHAPE_COLORS[piece[y][x] - 1]
                    # Adjust the coordinates to draw on the board
                    board_x = x + offset_x
                    board_y = y + offset_y
                    if 0 <= board_x < len(temp_board[0]) and 0 <= board_y < len(temp_board):
                        # Draw the piece on the board
                        pygame.draw.rect(screen, color,
                                        (board_x * BLOCK_SIZE, board_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(screen, GRAY,
                                        (board_x * BLOCK_SIZE, board_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    
    def new_piece(self):
        next_piece = random.choice(Tetromino.SHAPES)
        self.next_piece = next_piece  # Update next piece
        return next_piece
    def draw_grid(self):
        screen.fill(BLACK)
        for y1 in range(self.drawer.boardOffset-2,self.drawer.boardOffset-2+self.board.GRID_HEIGHT):
            y=y1-self.drawer.boardOffset+2
            for x1 in range(self.drawer.boardOffset-2,self.drawer.boardOffset-2+self.board.GRID_WIDTH):
                x=x1-self.drawer.boardOffset+2
                color = WHITE if self.grid[y][x] == 0 else Tetromino.SHAPE_COLORS[self.grid[y][x] - 1]
                pygame.draw.rect(screen, color, (x1 * BLOCK_SIZE, y1 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, GRAY, (x1 * BLOCK_SIZE, y1 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
                
    def draw_piece(self, piece, offset_x, offset_y):
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x]:
                    color = Tetromino.SHAPE_COLORS[piece[y][x] - 1]
                    pygame.draw.rect(screen, color,
                                     ((x + offset_x+self.drawer.boardOffset-2) * BLOCK_SIZE, (y +self.drawer.boardOffset-2+ offset_y) * BLOCK_SIZE, BLOCK_SIZE,
                                      BLOCK_SIZE))
                    pygame.draw.rect(screen, GRAY,
                                     ((x + offset_x+self.drawer.boardOffset-2) * BLOCK_SIZE, (y +self.drawer.boardOffset-2+ offset_y) * BLOCK_SIZE, BLOCK_SIZE,
                                      BLOCK_SIZE), 1)

    def drop_piece_hard(self):
        while not self.check_collision(self.current_piece, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        self.merge_piece()
        self.current_piece = self.next_piece  # Set current piece to next piece
        self.next_piece = self.new_piece()  # Generate new random piece for next piece    
        self.piece_x = self.board.GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        self.score +=20
        if self.check_collision(self.current_piece, self.piece_x, self.piece_y):
            self.game_over = True
            
    def drop_piece_hard1(self,current_piece,piece_x,piece_y,grid_copy):
        while not self.check_collision(current_piece, piece_x, piece_y + 1,grid=grid_copy):
            piece_y += 1
        self.merge_piece(grid_copy,current_piece,piece_y,piece_x)
        piece_x = self.board.GRID_WIDTH // 2 - len(current_piece[0]) // 2
        piece_y = 0
        self.score +=20
        #if self.check_collision(current_piece, piece_x, piece_y,):
         #   self.game_over = True

    def move_piece_down(self):
        if not self.check_collision(self.current_piece, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        else:
            self.merge_piece()
            self.current_piece = self.next_piece  # Set current piece to next piece
            self.next_piece = self.new_piece()  # Generate new random piece for next piece
            self.piece_x = self.board.GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
            self.piece_y = 0
            self.score +=20
            if self.check_collision(self.current_piece, self.piece_x, self.piece_y):
                self.game_over = True

    def move_piece_left(self, grid=None, current_piece=None, piece_x=None,piece_y=None):
        flag_x=0
        if grid is None:
            grid = self.grid
        if current_piece is None:
            current_piece = self.current_piece
        if piece_x is None:
            piece_x = self.piece_x
            flag_x=1
        if piece_y == None:
            piece_y = self.piece_y
        if not self.check_collision(current_piece, piece_x - 1, piece_y,grid):
            piece_x -= 1
        return piece_x

    def move_piece_right(self,grid=None, current_piece=None, piece_x=None,piece_y=None):
        flag_x=0
        if grid is None:
            grid = self.grid
        if current_piece is None:
            current_piece = self.current_piece
        if piece_x is None:
            piece_x = self.piece_x
            flag_x=1
        if piece_y == None:
            piece_y = self.piece_y
        if not self.check_collision(current_piece, piece_x + 1, piece_y,grid):
            piece_x += 1
        return piece_x

    def rotate_piece(self,grid=None, current_piece=None, piece_x=None,piece_y=None):
        flag_c=0
        if grid is None:
            grid = self.grid
        if current_piece is None:
            current_piece = self.current_piece
            flag_c=1
        if piece_x is None:
            piece_x = self.piece_x
        if piece_y == None:
            piece_y = self.piece_y
        rotated_piece = list(zip(*current_piece[::-1]))
        if not self.check_collision(rotated_piece, piece_x, piece_y,grid):
            current_piece = rotated_piece
        return current_piece
    def is_valid_position(self, piece, x, y, grid):
            """
            Check if the piece can be placed at the given position on the grid.
            """
            piece_height = len(piece)
            piece_width = len(piece[0])
            for i in range(piece_height):
                for j in range(piece_width):
                    if piece[i][j] and (x + j < 0 or x + j >= len(grid[0]) or y + i >= len(grid) or grid[y + i][x + j]):
                        return False
            return True
    def check_collision(self, piece, offset_x, offset_y,grid=None):
        if grid==None:
            grid=self.grid
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x] and (
                        y + offset_y < 0 or y + offset_y >= self.board.GRID_HEIGHT or
                        x + offset_x < 0 or x + offset_x >= self.board.GRID_WIDTH or
                        grid[y + offset_y][x + offset_x] != 0
                ):
                    return True
        return False

    def merge_piece(self, grid=None, current_piece=None, piece_y=None, piece_x=None):
        if grid is None:
            grid = self.grid
        if current_piece is None:
            current_piece = self.current_piece
        if piece_x is None:
            piece_x = self.piece_x
        if piece_y is None:
            piece_y = self.piece_y
        
        piece_height = len(current_piece)
        piece_width = len(current_piece[0])

        for y in range(piece_height):
            for x in range(piece_width):
                if current_piece[y][x]:
                    grid_y = y + piece_y
                    grid_x = x + piece_x
                    # Check if the position is valid
                    #print(current_piece,x + piece_x, x, piece_x, y + piece_y, y, piece_y)
                    if 0 <= grid_y < len(grid) and 0 <= grid_x < len(grid[0]):
                        grid[grid_y][grid_x] = current_piece[y][x]

    def get_column_height(self, grid, column_index):
        """
        Calculate the height of a specific column in the grid.
        """
        height = len(grid)  # Start from the top row
        if column_index < 0 or column_index >= len(grid[0]):  # Check if column_index is out of range
            return 0
        for row in range(len(grid)):
            if grid[row][column_index]:
                return height - row
        return 0

    def clear_lines(self,grid=None):
        lines_cleared = 0
        for y in range(self.board.GRID_HEIGHT):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * self.board.GRID_WIDTH)
                lines_cleared += 1
        self.score += lines_cleared * 100
        self.board.linesCleared += lines_cleared 
        self.board.high_score = max(self.board.high_score, self.score)  # Update high score
        self.board.save_high_score()  # Save high score to file
        return lines_cleared

          
    def max_height(self, piece, offset_x, offset_y):
        #for x in range(len(piece[0])):
        column_heights = [0] * self.board.GRID_WIDTH
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x]:
                    column_heights[offset_x + x] = max(column_heights[offset_x + x], self.board.GRID_HEIGHT - (offset_y + y))
        #self.height = max(column_heights)
       
        filled_rows=sum(1 for row in self.grid if any(row))+sum(1 for row in piece if any(piece))
        return filled_rows
        
    def count_holes_in_range(self, max_height=None,grid=None):
        num_holes = 0
        if grid == None:
            grid=self.grid
        if max_height==None:
            max_height=sum(1  for row in grid if any(row))
            #print("max hi",max_height)
        for x in range(self.board.GRID_WIDTH):  # Iterate over each column
            hole_found = False  # Flag to indicate if a hole has been found in this column
            for y in range(self.board.GRID_HEIGHT-max_height, self.board.GRID_HEIGHT):  # Start from the top of the filled grid
                if grid[y][x] != 0:  # If we encounter a filled cell
                    hole_found = True  # Update flag to indicate that a filled cell has been found
                elif hole_found:  # If a filled cell has been found and we encounter an empty cell
                    num_holes += 1  # Count it as a hole
        return num_holes
    
    def get_best_move(self, grid_copy, current_piece, piece_x, piece_y, max_height):
        possible_moves = ["LEFT", "RIGHT", "ROTATE"]
        best_move = None
        best_holes = float('inf')  # Initialize with infinity to ensure any found holes are better
        original_grid = copy.deepcopy(grid_copy)
        min_max_height = float('inf')
        column_height = self.get_column_height(grid_copy, piece_y)
        
        for move in possible_moves:
            if move == "ROTATE":
                # Iterate over possible rotations
                for rotation in range(4):  # Assuming 4 possible rotations
                    rotated_piece = self.rotate_piece(grid_copy, current_piece, piece_x, piece_y)
                    rotated_piece_copy = rotated_piece.copy()
                    
                    # Check if the rotation is valid
                    if self.is_valid_position(rotated_piece_copy, piece_x, piece_y, grid_copy):
                        # Drop the rotated piece
                        self.drop_piece_hard1(rotated_piece_copy, piece_x, piece_y, grid_copy)
                        
                        # Calculate the height after dropping the piece
                        max_height = sum(1 for row in grid_copy if any(row))
                        
                        # Calculate the number of holes in the grid
                        new_holes = self.count_holes_in_range(max_height, grid=grid_copy)
                        
                        # Check if lines are cleared
                        lines_cleared = self.board.linesCleared - a
                        if lines_cleared > 0:
                            return move  # Prioritize clearing lines
                        
                        # Update best move based on holes and height
                        if new_holes < best_holes or (new_holes == best_holes and column_height < min_max_height):
                            best_holes = new_holes
                            min_max_height = column_height
                            best_move = move
                        
                        # Restore the grid to its original state
                        grid_copy = copy.deepcopy(original_grid)
                    
                    # Rotate the piece for the next iteration
                    current_piece = rotated_piece
                    
            elif move in ["LEFT", "RIGHT"]:
                # Calculate the height after moving the piece multiple steps
                new_piece_x = piece_x
                a = self.clear_lines(grid_copy) 
                #print(a) # Store initial lines cleared count
                while True:
                    # Move the piece
                    new_piece_x = (self.move_piece_left(grid_copy, current_piece, new_piece_x, piece_y)
                                if move == "LEFT" else self.move_piece_right(grid_copy, current_piece, new_piece_x, piece_y))

                    # Check if the new position is within the grid boundaries
                    if new_piece_x < 0 or new_piece_x >= len(grid_copy[0]):
                        break

                    # Drop the piece
                    self.drop_piece_hard1(current_piece, new_piece_x, piece_y, grid_copy)
                    lines_cleared = self.clear_lines(grid_copy) - a
                    if lines_cleared > 0:
                        return move  # Prioritize clearing lines

                    max_height = sum(1 for row in grid_copy if any(row))
                    new_holes = self.count_holes_in_range(max_height, grid=grid_copy)
                    if new_holes==best_holes:
                        if column_height < min_max_height:
                            best_holes = new_holes
                            min_max_height = column_height
                            best_move = move

                    # Update best move based on holes and height
                    if new_holes < best_holes: 
                        best_holes = new_holes
                        best_move = move

                    # Restore the grid to its original state
                    grid_copy = copy.deepcopy(original_grid)

                    # Stop when reached grid boundary or found a lower height
                    if new_piece_x == piece_x:
                        break

                    # Update the current piece position
                    piece_x = new_piece_x

        return best_move

    def runAIBlock(self,flag_new):
        global timer_seconds
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.piece_x=self.move_piece_left()
                        max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                    elif event.key == pygame.K_RIGHT:
                        self.piece_x=self.move_piece_right()
                        max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                    elif event.key == pygame.K_DOWN:
                        self.move_piece_down()
                        max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                    elif event.key == pygame.K_UP:
                        self.current_piece=self.rotate_piece()
                    elif event.key == pygame.K_SPACE:  # Added for drop hard feature
                        self.drop_piece_hard()
                        
                    elif event.key == pygame.K_p:  # Pause/unpause when P key is pressed
                        self.paused = not self.paused
                        while self.paused:
                            screen.blit(bg, (0, 0))
                            drawer.drawPauseScreen()
                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_p:  # Pause/unpause when P key is pressed
                                        self.paused = not self.paused
                                    if event.key == pygame.K_n:
                                        flag_new=True#for new game
                                        return flag_new
                                    
            piece_x_copy=copy.deepcopy(self.piece_x)
                
            piece_y_copy=copy.deepcopy(self.piece_y)
            if not self.paused:  # Only update the game if not paused
                self.poll_attacker_ai(piece_x_copy, piece_y_copy)
                self.move_piece_down()
                self.clear_lines()
                self.clock.tick(5)  # Adjust game speed
                if timer_seconds == 0:
                    self.game_over = True
                else:
                    timer_seconds -= 1
            self.draw_grid()
            fontSize = int(1.5 * BLOCK_SIZE)
            nextYPos = int(self.drawer.height * 0.2)
            gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
            nextText = gameFont.render("Next piece", True, self.drawer.fontColour1)
            self.draw_piece(self.next_piece, self.board.GRID_WIDTH +5, 3)  # Draw next piece
            screen.blit(nextText, ((self.drawer.boardOffset + 12) *BLOCK_SIZE, (nextYPos-1) * BLOCK_SIZE))
            self.draw_piece(self.current_piece, self.piece_x, self.piece_y)# Draw current piece
            self.drawer.drawStats(self.board, timer_seconds)
            self.drawer.draw_score(self.score, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            #filled_rows = sum(1 for row in self.grid if any(row))
            #self.drawer.draw_height(filled_rows, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            #max_height_range = (0, filled_rows)
            #num_holes = self.count_holes_in_range(filled_rows)
            #self.drawer.drawHoles(num_holes, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            filled_rows = sum(1 for row in self.grid if any(row))
            #self.drawer.draw_height(filled_rows, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            #max_height_range = (0, filled_rows)
            num_holes = self.count_holes_in_range(filled_rows)
            self.drawer.drawHoles(num_holes, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            print(num_holes,"qgra")
                
            pygame.display.update()
            
    def run(self,flag_new):
        global timer_seconds
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.piece_x=self.move_piece_left()
                        max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                    elif event.key == pygame.K_RIGHT:
                        self.piece_x=self.move_piece_right()
                        max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                    elif event.key == pygame.K_DOWN:
                        self.move_piece_down()
                        max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                    elif event.key == pygame.K_UP:
                        self.current_piece=self.rotate_piece()
                    elif event.key == pygame.K_SPACE:  # Added for drop hard feature
                        self.drop_piece_hard()
                        
                    elif event.key == pygame.K_p:  # Pause/unpause when P key is pressed
                        self.paused = not self.paused
                        while self.paused:
                            screen.blit(bg, (0, 0))
                            drawer.drawPauseScreen()
                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_p:  # Pause/unpause when P key is pressed
                                        self.paused = not self.paused
                                    if event.key == pygame.K_n:
                                        flag_new=True#for new game
                                        return flag_new
            if not self.paused:  # Only update the game if not paused
                self.move_piece_down()
                self.clear_lines()
                self.clock.tick(5)  # Adjust game speed
                if timer_seconds == 0:
                    self.game_over = True
                else:
                    timer_seconds -= 1
            self.draw_grid()
            fontSize = int(1.5 * BLOCK_SIZE)
            nextYPos = int(self.drawer.height * 0.2)
            gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
            nextText = gameFont.render("Next piece", True, self.drawer.fontColour1)
            self.draw_piece(self.next_piece, self.board.GRID_WIDTH +5, 3)  # Draw next piece
            screen.blit(nextText, ((self.drawer.boardOffset + 12) *BLOCK_SIZE, (nextYPos-1) * BLOCK_SIZE))
            self.draw_piece(self.current_piece, self.piece_x, self.piece_y)# Draw current piece
            self.drawer.drawStats(self.board, timer_seconds)
            self.drawer.draw_score(self.score, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            filled_rows = sum(1 for row in self.grid if any(row))
            #self.drawer.draw_height(filled_rows, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            #max_height_range = (0, filled_rows)
            num_holes = self.count_holes_in_range(filled_rows)
            print(num_holes)
            self.drawer.drawHoles(num_holes, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            pygame.display.update()

    def runAI(self,flag_new):
            
            global timer_seconds
            while not self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:                        
                        if event.key == pygame.K_p:  # Pause/unpause when P key is pressed
                            self.paused = not self.paused
                            while self.paused:
                                screen.blit(bg, (0, 0))
                                drawer.drawPauseScreen()
                                pygame.display.update()
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    elif event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_p:  # Pause/unpause when P key is pressed
                                            self.paused = not self.paused
                                        if event.key == pygame.K_n:
                                            flag_new=True#for new game
                                            return flag_new
                                    
                if not self.paused:  # Only update the game if not paused
                    
                    self.move_piece_down()
                    self.clear_lines()
                    self.clock.tick(4)  # Adjust game speed
                    if timer_seconds == 0:
                        self.game_over = True
                    else:
                        timer_seconds -= 1
                
                self.draw_grid()
                
                fontSize = int(1.5 * BLOCK_SIZE)
                nextYPos = int(self.drawer.height * 0.2)
                gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
                nextText = gameFont.render("Next piece", True, self.drawer.fontColour1)
                self.draw_piece(self.next_piece, self.board.GRID_WIDTH +4, 1)  # Draw next piece
                screen.blit(nextText, ((self.drawer.boardOffset + 12) *BLOCK_SIZE, (nextYPos-3) * BLOCK_SIZE))
                
                self.draw_piece(self.current_piece, self.piece_x, self.piece_y)# Draw current piece
                self.drawer.drawStats(self.board, timer_seconds)
                self.drawer.draw_score(self.score, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
                filled_rows = sum(1 for row in self.grid if any(row))
                self.drawer.draw_height(filled_rows, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
                max_height_range = (0, filled_rows)
                num_holes = self.count_holes_in_range(filled_rows)
                
                self.drawer.drawHoles(num_holes, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
                pygame.display.update()
                
                grid_copy=copy.deepcopy(self.grid)
                #print(grid_copy)
                current_piece_copy=copy.deepcopy(self.current_piece)
                piece_x_copy=copy.deepcopy(self.piece_x)
                
                piece_y_copy=copy.deepcopy(self.piece_y)
                #print(piece_x_copy)
                max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                #get_best_move(self, grid_copy, current_piece, piece_x, piece_y, max_height)
                move= self.get_best_move(grid_copy,current_piece_copy,piece_x_copy,piece_y_copy,max_height)            
                if move=="LEFT":
                    self.piece_x=self.move_piece_left()
                if move=="RIGHT":
                    self.piece_x=self.move_piece_right()
                if move=="ROTATE":
                    self.current_piece=self.rotate_piece()
    def runAIvsAI(self,flag_new):
            global timer_seconds
            while not self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:                      
                        if event.key == pygame.K_p:  # Pause/unpause when P key is pressed
                            self.paused = not self.paused
                            while self.paused:
                                screen.blit(bg, (0, 0))
                                drawer.drawPauseScreen()
                                pygame.display.update()
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    elif event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_p:  # Pause/unpause when P key is pressed
                                            self.paused = not self.paused
                                        if event.key == pygame.K_n:
                                            flag_new=True#for new game
                                            return flag_new
                                        
                piece_x_copy=copy.deepcopy(self.piece_x)
                    
                piece_y_copy=copy.deepcopy(self.piece_y)
                if not self.paused:  # Only update the game if not paused
                    self.poll_attacker_ai(piece_x_copy, piece_y_copy)
                    self.move_piece_down()
                    self.clear_lines()
                    self.clock.tick(10)  # Adjust game speed
                    if timer_seconds == 0:
                        self.game_over = True
                    else:
                        timer_seconds -= 1
                self.draw_grid()
                fontSize = int(1.5 * BLOCK_SIZE)
                nextYPos = int(self.drawer.height * 0.2)
                gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
                nextText = gameFont.render("Next piece", True, self.drawer.fontColour1)
                self.draw_piece(self.next_piece, self.board.GRID_WIDTH +5, 3)  # Draw next piece
                screen.blit(nextText, ((self.drawer.boardOffset + 12) *BLOCK_SIZE, (nextYPos-1) * BLOCK_SIZE))
                
                self.draw_piece(self.current_piece, self.piece_x, self.piece_y)# Draw current piece
                self.drawer.drawStats(self.board, timer_seconds)
                self.drawer.draw_score(self.score, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
                filled_rows = sum(1 for row in self.grid if any(row))
                self.drawer.draw_height(filled_rows, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
                max_height_range = (0, filled_rows)
                num_holes = self.count_holes_in_range(filled_rows)
                
                self.drawer.drawHoles(num_holes, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
                pygame.display.update()
                
                grid_copy=copy.deepcopy(self.grid)
                #print(grid_copy)
                current_piece_copy=copy.deepcopy(self.current_piece)
                piece_x_copy=copy.deepcopy(self.piece_x)
                
                piece_y_copy=copy.deepcopy(self.piece_y)
                #print(piece_x_copy)
                max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                #get_best_move(self, grid_copy, current_piece, piece_x, piece_y, max_height)
                move= self.get_best_move(grid_copy,current_piece_copy,piece_x_copy,piece_y_copy,max_height)            
                if move=="LEFT":
                    self.piece_x=self.move_piece_left()
                if move=="RIGHT":
                    self.piece_x=self.move_piece_right()
                if move=="ROTATE":
                    self.current_piece=self.rotate_piece()
                
    ##                def get_best_move_cleared(self,grid_copy,current_piece,piece_x,piece_y,max_height=None):
    ##                    for move in ["LEFT", 'RIGHT','ROTATE']:
    ##                        score_before=0
    ##                        for row in grid_copy:
    ##                            score_row=sum(row)
    ##                            if score_row>score_before:
    ##                                score_before=score_row
    ##                                
    ##                        final_move=None
    ##                        if move == "LEFT":
    ##                            piece_x = self.move_piece_left(grid_copy,current_piece,piece_x,piece_y)  # Move one step to the left
    ##                        elif move == "RIGHT":
    ##                            piece_x = self.move_piece_right(grid_copy,current_piece,piece_x,piece_y)  # Move one step to the right
    ##                        elif move == "ROTATE":
    ##                            # Update current_piece after rotation
    ##                            current_piece = self.rotate_piece(grid_copy, current_piece, piece_x, piece_y)
    ##                        while !check_collision(self,current_piece,piece_x,piece_y,grid_copy):
    ##                            drop current piece on grid
    ##                            score_row_final=0#after piece is dropped
    ##                            for row in grid_copy:
    ##                                score_row=sum(row)
    ##                                if score_row>score_row_final:
    ##                                    score_row_final=score_row
    ##                                
    ##                            if score_row_final>score_before:
    ##                                final_move=move
                                    
                        
    ##                
    ##                grid_copy=copy.copy(self.grid)
    ##                current_piece_copy=copy.copy(self.current_piece)
    ##                piece_x_copy=copy.copy(self.piece_x)
                    #print(piece)
                    #print(self.current_piece,self.grid)
                
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris_group3")
    bg = pygame.image.load('bg.jpg').convert()

    game = Tetris()
    drawer = Draw()
    current_screen = "main"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if current_screen == "main":
                    if event.key == pygame.K_r:
                        current_screen = "tetris"
                        flag_new=False#human
                        flag_new=game.run(flag_new)
                        if flag_new==True:
                            game = Tetris()  # Reset the game
                            current_screen = "main"
                    elif event.key == pygame.K_a:
                        current_screen = "tetris"
                        flag_new=False
                        flag_new=game.runAI(flag_new)
                        if flag_new==True:
                            game = Tetris()  # Reset the game
                            current_screen = "main"
                    elif event.key == pygame.K_i:
                        current_screen = "tetris"
                        flag_new=False
                        flag_new=game.runAIBlock(flag_new)
                        if flag_new==True:
                            game = Tetris()  # Reset the game
                            current_screen = "main"
                    elif event.key == pygame.K_j:
                        current_screen = "tetris"
                        flag_new=False
                        flag_new=game.runAIvsAI(flag_new)
                        if flag_new==True:
                            game = Tetris()  # Reset the game
                            current_screen = "main"
                elif current_screen == "tetris":
                    if game.game_over and event.key == pygame.K_n:  # Restart the game if 'N' is pressed
                        print("Restarting the game...")
                        game = Tetris()  # Reset the game
                        current_screen = "main"
                elif current_screen == "game_over_screen":
                    if event.key == pygame.K_n:  # Restart the game if 'N' is pressed
                        print("Restarting the game...")
                        game = Tetris()  # Reset the game
                        current_screen = "main"

        if current_screen == "main":
                screen.blit(bg, (0, 0))  # Blit the background image onto the screen
                drawer.draw_main_screen()
                pygame.display.update()
                timer_seconds = time
        if current_screen == "paused":
            screen.blit(bg, (0, 0))
            drawer.drawPauseScreen()
            pygame.display.update()
        elif current_screen == "tetris":
            if game.game_over:  # If the game is over, switch to the game over screen
                current_screen = "game_over_screen"
            else:
                screen.blit(bg, (0, 0))  # Blit the background image onto the screen
                #drawer.drawBoard(game.board)
                #game.draw_grid()
                game.draw_piece(game.current_piece, game.piece_x, game.piece_y)
                drawer.drawStats(game.board, timer_seconds)
                pygame.display.update()
        if current_screen == "game_over_screen":
                screen.blit(bg, (0, 0))
                drawer.drawGameOver()
                drawer.draw_text_with_highlight("Score: " + str(game.score), BLOCK_SIZE * (game.board.GRID_WIDTH // 2+4),
                                (game.board.GRID_HEIGHT // 2 +2 ) * BLOCK_SIZE)
                drawer.draw_text_with_highlight("High Score: {}".format(game.board.high_score), BLOCK_SIZE * (game.board.GRID_WIDTH // 2 +2),
                                                (game.board.GRID_HEIGHT // 2 + 5) * BLOCK_SIZE)  # Adjusted position for high score
                drawer.draw_text_with_highlight("PRESS N to play again", BLOCK_SIZE * (game.board.GRID_WIDTH // 2 -1),
                                                (game.board.GRID_HEIGHT // 2 + 8) * BLOCK_SIZE)  # Adjusted position for play again
                pygame.display.update()
                timer_seconds = time
