
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

time = 300
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
                                      ((self.board.GRID_HEIGHT / 2) - 5) * BLOCK_SIZE,
                                      highlight_color=(20, 0, 200))
        self.draw_text_with_highlight("PRESS  A  :  AI MODE", (self.boardWidth // 2 - 1) * BLOCK_SIZE,
                                      (self.board.GRID_HEIGHT / 2) * BLOCK_SIZE, highlight_color=(20, 200, 20))
        self.draw_text_with_highlight("PRESS  H  :  HUMAN", (self.boardWidth // 2 - 0.7) * BLOCK_SIZE,
                                      ((self.board.GRID_HEIGHT / 2) + self.boardOffset + 1) * BLOCK_SIZE,
                                      highlight_color=(100, 190, 200))


    def drawGameOver(self):
        self.draw_text_with_highlight("GAME OVER", BLOCK_SIZE * (self.boardWidth // 2 + 2),
                                      (self.board.GRID_HEIGHT // 2 - 2) * BLOCK_SIZE)  # Update here
 


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
        (255, 0, 0),
        (255, 163, 47),
        (255, 236, 33),
        (147, 240, 59),
        (55, 138, 255),
        (255, 119, 253),
        (149, 82, 234)
    ]

    SHAPES = [
        [[1, 1, 1, 1]],  # I - Red
        [[2, 2, 2], [0, 2, 0]],  # T - Orange
        [[3, 3, 3], [3, 0, 0]],  # L - Yellow
        [[4, 4, 4], [0, 0, 4]],  # J - Green
        [[0, 5, 5], [5, 5, 0]],  # S - Blue
        [[6, 6], [6, 6]],  # O - Pink
        [[7, 7, 0], [0, 7, 7]]  # Z - Purple
    ]


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

    def move_piece_left(self):
        if not self.check_collision(self.current_piece, self.piece_x - 1, self.piece_y):
            self.piece_x -= 1

    def move_piece_right(self):
        if not self.check_collision(self.current_piece, self.piece_x + 1, self.piece_y):
            self.piece_x += 1

    def rotate_piece(self):
        rotated_piece = list(zip(*self.current_piece[::-1]))
        if not self.check_collision(rotated_piece, self.piece_x, self.piece_y):
            self.current_piece = rotated_piece

    def check_collision(self, piece, offset_x, offset_y):
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x] and (
                        y + offset_y < 0 or y + offset_y >= self.board.GRID_HEIGHT or
                        x + offset_x < 0 or x + offset_x >= self.board.GRID_WIDTH or
                        self.grid[y + offset_y][x + offset_x] != 0
                ):
                    return True
        return False

    def merge_piece(self):
        for y in range(len(self.current_piece)):
                for x in range(len(self.current_piece[y])):
                    if self.current_piece[y][x]:
                        self.grid[y + self.piece_y][x + self.piece_x] = self.current_piece[y][x]
                    else:
                        self.grid[y][x] = 0


    def clear_lines(self):
        lines_cleared = 0
        for y in range(self.board.GRID_HEIGHT):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * self.board.GRID_WIDTH)
                lines_cleared += 1
        self.score += lines_cleared * 100
        self.board.linesCleared += lines_cleared 
        self.board.high_score = max(self.board.high_score, self.board.score)  # Update high score
        self.board.save_high_score()  # Save high score to file

    def max_height(self, piece, offset_x, offset_y):
        #for x in range(len(piece[0])):
        column_heights = [0] * self.board.GRID_WIDTH
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x]:
                    column_heights[offset_x + x] = max(column_heights[offset_x + x], self.board.GRID_HEIGHT - (offset_y + y))
        self.height = max(column_heights)
        return max(column_heights)
        #if column_height >= self.height:
          #  self.height = column_height
            #self.height = offset_y + y
        
    def count_holes_in_range(self, max_height):
        num_holes = 0
        for x in range(self.board.GRID_WIDTH):  # Iterate over each column
            hole_found = False  # Flag to indicate if a hole has been found in this column
            for y in range(self.board.GRID_HEIGHT-max_height, self.board.GRID_HEIGHT):  # Start from the top of the grid
                if self.grid[y][x] != 0:  # If we encounter a filled cell
                    hole_found = True  # Update flag to indicate that a filled cell has been found
                elif hole_found:  # If a filled cell has been found and we encounter an empty cell
                    num_holes += 1  # Count it as a hole
        return num_holes
    
    def run(self,flag_new):
        global timer_seconds
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece_left()
                        max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece_right()
                        max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                    elif event.key == pygame.K_DOWN:
                        self.move_piece_down()
                        max_height=self.max_height(self.current_piece, self.piece_x, self.piece_y)
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
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
                                        flag_new=True
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
                    if event.key == pygame.K_h:
                        current_screen = "tetris"
                        flag_new=False#human
                        flag_new=game.run(flag_new)
                        if flag_new==True:
                            game = Tetris()  # Reset the game
                            current_screen = "main"
                    elif event.key == pygame.K_a:
                        current_screen = "tetris"
                        flag_new=False
                        flag_new=game.run(flag_new)
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

    
    

    
    

'''
import copy, random #for generating blocks
import sys #needed to quit the pygame
import pygame
from enum import *

pygame.init()#initialising pygame

display_h = pygame.display.Info().current_h #system's height
pygame.display.set_caption("Tetris_group3")#sets the title of the screen
blockSize = display_h // 30 #1/30 of that height is a block, so that a 20 by 10 blocks tetris grid is visible in 2/3 rd by 1/3rd of the dispay screen
height = 25* blockSize
width=height+10
screen = pygame.display.set_mode((width, height))#initializes the game screen with given dimensions
bg = pygame.image.load('bg.jpg').convert()
screen.blit(bg,(0,0))
clock = pygame.time.Clock()#we need this to time the game and control frame rate (how fast the game progresses)

time=10
timer_seconds=time #the game is timed using this variable as a counter and  gets over after these many seconds

class Board :#defining functions for the tetris game's grid

    def __init__(self, colour = "Black"):
        self.colour = colour
        self.width = 10
        self.height = 20
        self.linesCleared = 0 #to keep track of score
        self.emptyGrid() #creating a 2D list to represent the grid.
        self.pieceList = [] #creating an array containing the tetromino pieces. Each tetromino is specified by the coordinates of its color.
        self.nextPiece=self.generatePiece() #the next piece that will come into play
        self.holeCount = None
        self.startInterval = 1000
        self.level = 1
        
    def emptyGrid(self):
        self.grid = []#creating a 2D list to represent the grid. 
        self.emptyRow = []
        for x in range(self.width):
            self.emptyRow.append(0)
        for rowCount in range(self.height):
            self.grid.append(copy.copy(self.emptyRow))

    def centrePiece(self, tetromino):#this moves the given tetromino form its default position at top left corner, to middle of top row which is where the pieces shouuld appear from initially.
        for coord in tetromino.vertexCoords:#iterating over the list of all vertex coordinates which are used to draw the piece.
            coord[0] += (self.width/2)-2  #for x coordinate of each vertex it is shifted to the middle of the grid
        tetromino.centre[0] += (self.width/2)-2 #tetromino.centre[0] is the x coordinate of the centre of tetromino and it is shifted by as much as the vertex is shifted to maintain shape of block
        for coord in tetromino.blockCoords:#done for the block coordinates
            coord[0] += (self.width/2)-2
        
    def generatePiece(self):
        if (len(self.pieceList) == 0):
            self.pieceList = list(Tetromino.Shapes.keys())
            random.shuffle(self.pieceList)
        tetromino = Tetromino(self.pieceList.pop())#returns a tetromino which is a 2d array of vertex coords, block coords and centre
        self.centrePiece(tetromino)
        return (tetromino)
    
    def isOutOfBounds(self, tetromino):
        minX = tetromino.getMinXCoord()
        maxX = tetromino.getMaxXCoord()
        minY = tetromino.getMinYCoord()
        maxY = tetromino.getMaxYCoord()
        if (minX < 0) or (minY < 0) or (maxX > self.width) or (maxY > self.height):
            return True
        else:
            return False

    def moveOrLockPiece(self, tetromino, direction, count = 1):
        x = direction.value[0]
        y = direction.value[1]
        for i in range(count):
            tetromino.incrementCoords(x, y)
            if (self.isOutOfBounds(tetromino) or self.isGridBlocked(tetromino)):
                tetromino.incrementCoords(-x,-y)
                if (y > 0):
                    self.lockPieceOnGrid(tetromino)
                    clearedRowCount = self.clearFullRows()
                    self.updateScores(clearedRowCount)
                    return True
        return False
    def updateScores(self, clearedRowCount):
        self.linesCleared += clearedRowCount

    def getDropInterval(self):
        scale = pow(0.8, self.level)
        dropInterval = int(self.startInterval * scale)
        return dropInterval

    def isGridBlocked(self, tetromino):
        for coord in tetromino.blockCoords:
            y = int(coord[1])
            x = int(coord[0])
            if self.grid[y][x] != 0:
                return True
        return False

    def lockPieceOnGrid(self, tetromino):
        for coord in tetromino.blockCoords:
            y = int(coord[1])
            x = int(coord[0])
            self.grid[y][x] = copy.copy(tetromino.colour)
    
    def clearFullRows(self):
        fullRowCount = 0
        y = self.height - 1
        while (y > 0):
            emptyBlocks = 0
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    emptyBlocks +=1
            if emptyBlocks == self.width:
                return fullRowCount
            elif emptyBlocks == 0:
                fullRowCount += 1
                self.grid[y] = copy.copy(self.emptyRow)
                for i in range (y, 1, -1):
                    self.grid[i] = copy.deepcopy(self.grid[i-1])
                y += 1
            y-=1
        return fullRowCount
         
    def rotatePiece(self, tetromino, rotation = None, count = 1):
        for i in range(count):
            tetromino.rotateCoords(rotation)
            if (self.isOutOfBounds(tetromino) or self.isGridBlocked(tetromino)):
                tetromino.rotateCoords(-rotation)
                break

    def newPieceOrGameOver(self, tetromino,tetrominonext):
        if (tetromino.xOffset == 0) and (tetromino.yOffset == 0):
            return None
        else:
            tetromino = tetrominonext
            return tetromino
    
    def dropAndLockPiece(self, tetromino):
        isLocked = False
        while (not isLocked):
            isLocked = self.moveOrLockPiece(tetromino,Direction.DOWN)

    def dropPieceWithoutLock(self, tetromino):
            while not ((self.isOutOfBounds(tetromino) or self.isGridBlocked(tetromino))):
                tetromino.incrementCoords(0, 1)
            tetromino.incrementCoords(0, -1)
    
    def moveLeftAndLockPiece(self, tetromino, count):
        self.moveOrLockPiece(tetromino, Direction.LEFT, count)
        self.dropAndLockPiece(tetromino)

class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
            
class Draw:
    

    def __init__(self):
        self.height=20
        self.boardWidth = 10 
        self.boardOffset = 4#leaves some left margin before start of the grid
        self.boardOutline = (blockSize // 15) if (blockSize >= 15) else 1#to see individual cells in board
        self.pieceOutline = (blockSize // 15) if (blockSize >= 15) else 1#to see tetromino piece in board
        self.boardRect = pygame.Rect(self.boardOffset*blockSize, self.boardOffset*blockSize, (self.boardWidth*blockSize
                                                                     ) + self.boardOutline, height-self.boardOffset)
        #pygame.Rect(x,y,w,h) creates a rectangle object of width w and height h whose top left corner is at position x,y 
        self.fontColour = (255, 0, 50) #font colour

    def drawBackground(self, board):
        self.drawBoard(board)

    def drawBoard(self, board):

        pygame.draw.rect(screen, board.colour, self.boardRect)        #pygame.draw.rect(surface, color of rect, pygame.rect,default=fill whole else specify width of border) draws the rect of specified color
        for x in range(self.boardOffset, (self.boardWidth + self.boardOffset)):#coordinates along width of grid
            for y in range(self.boardOffset, self.height+ self.boardOffset):#coordinates along height of grid
                cell = pygame.Rect(x*blockSize + self.boardOutline,
                                   y*blockSize + self.boardOutline,
                                   blockSize - self.boardOutline, blockSize - self.boardOutline)
                #adds margins to x and y coordinates and subtract margins from width and height coordinates to accomodate borders of each individual cell 
                pygame.draw.rect(screen, "White", cell)#draws each of the cells in the board grid

    def getScaledCoords(self, vertexCoords):#scaled coords of current tetromino at top centre of grid
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + self.boardOffset)*blockSize
            coord[1] = (coord[1]+self.boardOffset)*blockSize
        return copyCoords

    def getScaledCoords1(self, vertexCoords):#scaled coord of display for next tetromino at side of the grid
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + self.boardWidth+self.boardOffset-1)*blockSize
            coord[1] = (coord[1]+self.boardOffset+2)*blockSize
        return copyCoords
    def drawTetromino1(self, tetromino):
        pygame.draw.polygon(screen, tetromino.colour, self.getScaledCoords1(tetromino.vertexCoords))
    def drawTetromino(self, tetromino):
        pygame.draw.polygon(screen, tetromino.colour, self.getScaledCoords(tetromino.vertexCoords))
        pygame.draw.polygon(screen, "Black", self.getScaledCoords(tetromino.vertexCoords), self.pieceOutline)#draws a black outline surrounding the tetromino piece

    def drawGridPieces(self, board):
        for y in range(int(board.height)):
            for x in range(int(board.width)):
                if board.grid[y][x] != 0:
                    pygame.draw.rect(screen, board.grid[y][x], ((x+self.boardOffset)*blockSize, y*blockSize, blockSize, blockSize))

    def updateDisplay(self, board, tetromino):
        self.board = board
        self.tetromino = tetromino
        pygame.display.update()
    
    def drawStats(self, board):
        fontSize = int(1.5*blockSize)# Determine font size
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize, bold=True)# Load game font
        nextText = gameFont.render("Next piece", True, self.fontColour)# Render text
        time = gameFont.render(str(timer_seconds), True, self.fontColour)
        timeText = gameFont.render("Time remaining", True, self.fontColour)
        lineNum = gameFont.render(str(board.linesCleared), True, self.fontColour)
        lineText = gameFont.render("Lines cleared", True, self.fontColour)
        pauseText=gameFont.render("Press P to pause", True, self.fontColour)
        nextYPos = int(board.height*0.2)
        timeYPos = nextYPos + 6
        lineYPos = timeYPos + 4
        pauseYpos = lineYPos + 4
        screen.blit(nextText, ((self.boardOffset+11)*blockSize, (nextYPos)*blockSize))# Blit text onto the screen
        screen.blit(time, ((self.boardOffset+15)*blockSize, (timeYPos+1.5)*blockSize))
        screen.blit(timeText, ((self.boardOffset+11)*blockSize, (timeYPos)*blockSize))
        screen.blit(lineText, ((self.boardOffset+11)*blockSize, lineYPos*blockSize))
        screen.blit(lineNum, ((self.boardOffset+15)*blockSize, (lineYPos+1.5)*blockSize))
        screen.blit(pauseText, ((self.boardOffset+11)*blockSize, pauseYpos*blockSize))
    def draw_text_with_highlight(self,text, x, y,fontSize = int(2 * blockSize),highlight_color = (250, 200, 0)):
        # Render the text
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize,bold=True)# Get a font object with the system's first available font at the specified size
        text_surface = gameFont.render(text, True, self.fontColour)# Render text using the font, antialiasing enabled, with specified font color

        # Create a rectangle with the same size as the text
        rect = text_surface.get_rect()
        rect.topleft = (x, y)
        # Draw the highlight rectangle
        pygame.draw.rect(screen, highlight_color, rect)

        # Draw the text on top of the highlight and blit the rendered text onto the screen at a specific position
        screen.blit(text_surface, rect.topleft)
    def drawGameOver(self, board):
        self.draw_text_with_highlight("GAME OVER", blockSize*(self.boardWidth/2+2), (board.height/2-1)*blockSize)
        self.draw_text_with_highlight("PRESS N", blockSize*(self.boardWidth/2+3), (board.height/2+2)*blockSize)
    def drawStartScreen(self, board):
        self.draw_text_with_highlight("WELCOME TO TETRIS!", (self.boardWidth//2-1.5)*blockSize, ((board.height/2)-5)*blockSize,highlight_color = (20, 0, 200))
        self.draw_text_with_highlight("PRESS  A  :  AI MODE", (self.boardWidth//2-1)*blockSize, (board.height/2)*blockSize,highlight_color = (20, 200, 20))
        self.draw_text_with_highlight("PRESS  H  :  HUMAN", (self.boardWidth//2-0.7)*blockSize, ((board.height/2)+self.boardOffset+1)*blockSize,highlight_color = (100, 190, 200))

    def drawPauseScreen(self):
        self.draw_text_with_highlight("Game Menu!", (self.boardWidth//2+self.boardOffset-1)*blockSize, 3*blockSize,highlight_color = (80, 190, 200))
        self.draw_text_with_highlight("N:                        New Game", (self.boardWidth//2)*blockSize, 7*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("P:                        Pause/Unpause", (self.boardWidth//2 )*blockSize, 9*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Left Arrow:         Move Left", (self.boardWidth//2 )*blockSize, 11*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Right Arrow:      Move Right", (self.boardWidth//2 )*blockSize, 13*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Up Arrow:          Rotate", (self.boardWidth//2 )*blockSize, 15*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Space:               Hard Drop", (self.boardWidth//2 )*blockSize, 17*blockSize,  int(1.5*blockSize))

    def refreshScreen(self, board, tetromino,tetrominonext):
        screen.fill("Black")#Clears screen by filling the screen with black color
        self.drawBoard(board)#creating the grid
        self.drawTetromino(tetromino)
        self.drawStats(board)
        self.drawTetromino1(tetrominonext)#draw next tetromino piece        
        pygame.display.update()
        
class Rotation(IntEnum):
    CLOCKWISE = 1
    
class Tetromino():
    # Dictionary mapping color names to RGB tuples
    Colours = {
        
        "red" : (255,0,0),         #RGB tuples represent colors using three values: red, green, and blue.  
        "orange" : (255,163,47),    #Each component can have a value between 0 and 255
        "yellow" : (255,236,33),     #0 represents no intensity of that color   
        "green" : (147,240,59),       #255 represents the maximum intensity.
        "blue" : (55,138,255),
        "pink" : (255,119,253),
        "purple" : (149,82,234)}

    Shapes = {
        #Every shape is 3 element list where the first element is list of vertices, 
        #2nd is a list of top left corner co-ordinates of constituent blocks and
        #3rd is the centre of rotation 
        "O" : [ [[0,0],[2,0],[2,2],[0,2]], [[0,0],[1,0],[0,1],[1,1]], [1,1] ],
        "I" : [ [[0,0],[4,0],[4,1],[0,1]], [[0,0],[1,0],[2,0],[3,0]], [2,1] ], 
        "S" : [ [[1,0],[3,0],[3,1],[2,1],[2,2],[0,2],[0,1],[1,1]], [[1,0],[2,0],[0,1],[1,1]], [1.5,1.5] ],
        "Z" : [ [[0,0],[2,0],[2,1],[3,1],[3,2],[1,2],[1,1],[0,1]], [[0,0],[1,0],[1,1],[2,1]], [1.5,1.5] ],
        "J" : [ [[0,0],[3,0],[3,2],[2,2],[2,1],[0,1]], [[0,0],[1,0],[2,0],[2,1]], [1.5,0.5] ],
        "L" : [ [[0,0],[3,0],[3,1],[1,1],[1,2],[0,2]], [[0,0],[1,0],[2,0],[0,1]], [1.5,0.5] ],
        "T" : [ [[0,0],[3,0],[3,1],[2,1],[2,2],[1,2],[1,1],[0,1]], [[0,0],[1,0],[2,0],[1,1]], [1.5,0.5] ]
    }
    SHAPE_COLORS = [
        (255, 0, 0),
        (255, 163, 47),
        (255, 236, 33),
        (147, 240, 59),
        (55, 138, 255),
        (255, 119, 253),
        (149, 82, 234)
    ]

    SHAPES = [
        [[1, 1, 1, 1]],  # I - Red
        [[2, 2, 2], [0, 2, 0]],  # T - Orange
        [[3, 3, 3], [3, 0, 0]],  # L - Yellow
        [[4, 4, 4], [0, 0, 4]],  # J - Green
        [[0, 5, 5], [5, 5, 0]],  # S - Blue
        [[6, 6], [6, 6]],  # O - Pink
        [[7, 7, 0], [0, 7, 7]]  # Z - Purple
    ]

    def __init__(self, shape = None):
        self.rotations = 0
        self.xOffset = 0
        self.yOffset = 0
        if self.Shapes.get(shape) is not None:
            self.shape = shape
        else:
            self.shape = random.choice(list(self.Shapes.keys()))
        self.vertexCoords = copy.deepcopy(self.Shapes[self.shape][0])#for more meaningful variables
        #and if we dont make deepcopy then vertex will keep shifting for every new game!
        self.blockCoords = self.Shapes[self.shape][1]
        self.centre = self.Shapes[self.shape][2]        
        self.colour = random.choice(list(self.Colours.values()))

    def getMinXCoord(self):
        x = 38400
        for coord in self.vertexCoords:
            if coord[0] < x:
                x = coord[0]
        return x
    
    def getMaxXCoord(self):
        x = 0
        for coord in self.vertexCoords:
            if coord[0] > x:
                x = coord[0]
        return x
    
    def getMinYCoord(self):
        y = 21600
        for coord in self.vertexCoords:
            if coord[1] < y:
                y = coord[1]
        return y

    def getMaxYCoord(self):
        y = 0
        for coord in self.vertexCoords:
            if coord[1] > y:
                y = coord[1]
        return y
    def incrementCoords(self, x = 0 , y = 0):
        self.xOffset += x
        self.yOffset += y
        self.centre[0] += x
        self.centre[1] += y
        for coord in self.vertexCoords:
            coord[0] += x
            coord[1] += y
        for coord in self.blockCoords:
            coord[0] += x
            coord[1] += y

    def rotateCoords(self, rotation = 0):
        if rotation != 0:
            self.rotations += rotation
            direction = rotation / abs(rotation)
            for i in range(abs(rotation)):
                for coord in self.vertexCoords:
                    x = coord[0] - self.centre[0]
                    y = coord[1] - self.centre[1]
                    coord[1] = self.centre[1] + (direction * x)
                    coord[0] = self.centre[0] - (direction * y)
                for coord in self.blockCoords:
                    x = coord[0] - self.centre[0]
                    y = coord[1] - self.centre[1]
                    coord[1] = self.centre[1] + (direction * x)
                    coord[0] = self.centre[0] - (direction * y)
                    #This line is needed to adjust so the block coord is always top left coord of "block"
                    coord[int((1 - direction)/2)] += -1

        
newGame = True
gameOver = False
paused = False
locked = False
draw = Draw()

def gameQuit(parameter=None):
    if event.type == pygame.QUIT: # If the user quits the game
        parameter = False # Exit the parameter's loop
        pygame.quit() # Quit pygame
        sys.exit() # Exit the script
                

while True:
    
    #reset game and timer
    if newGame:
        board = Board() # Create a new instance of the Board class
        tetromino = board.generatePiece() # Generate a new tetromino piece
        tetrominonext=board.generatePiece() # Generate the next tetromino piece
        screen.blit(bg,(0,0))#refresh the background image
        draw.drawStartScreen(board) # Draw the start screen
        timer_seconds=time # Set the timer_seconds variable to initial value of time
        timeCount = 0

    #newGame screen loop
        while newGame:
            pygame.display.update() # Update the display
            for event in pygame.event.get(): # Iterate over all events in the event queue
                gameQuit(newGame)
                keyInput = pygame.key.get_pressed() # Get the current state of all keyboard keys
                if keyInput[pygame.K_h]: # If the 'H' key is pressed
                    newGame = False # Exit the newGame loop
                if keyInput[pygame.K_a]: # If the 'A' key is pressed
                    newGame = False # Exit the newGame loop

    #Pause screen loop
    while paused:
        screen.blit(bg,(0,0))
        draw.drawPauseScreen()
        pygame.display.update()
        for event in pygame.event.get():
            gameQuit(paused)
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_p]:
                paused = False
            if keyInput[pygame.K_n]:
                newGame = True
                paused = False
 
    gameFlags = [newGame, gameOver, paused]

    #gamePlay Loop
    counter=0
    while (not any(gameFlags)):#while none of the game flags are true
        clock.tick(60)#tick(n) means the while loop and all code in it will run n times per second
        #Draw game elements to screen
        screen.fill("Black")#Clears screen by filling the screen with black color        
        draw.refreshScreen(board, tetromino,tetrominonext)
        
        counter+=1
        if counter%60==0:
            timer_seconds -= 1
        if timer_seconds == 0:
            gameOver=True
            timer_seconds=time#reset timer to initial value
 

        #Step game forward
        timeCount += clock.get_rawtime()
        if (timeCount >= board.getDropInterval()):
            timeCount = 0
            locked = board.moveOrLockPiece(tetromino, Direction.DOWN)
            if (locked):
                tetromino = board.newPieceOrGameOver(tetromino,tetrominonext)
                tetrominonext=board.generatePiece() # Generate the next tetromino piece
        
                if tetromino == None:
                    gameOver = True
                    break
            draw.refreshScreen(board, tetromino,tetrominonext)
        
        #Check for user input
        for event in pygame.event.get():
            gameQuit()
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_p]:
                paused = True
            if keyInput[pygame.K_n]:
                newGame = True
            if keyInput[pygame.K_UP]:
                board.rotatePiece(tetromino, Rotation.CLOCKWISE)
            if keyInput[pygame.K_RIGHT]:
                board.moveOrLockPiece(tetromino, Direction.RIGHT)
            if keyInput[pygame.K_LEFT]:
                board.moveOrLockPiece(tetromino, Direction.LEFT)
            if keyInput[pygame.K_DOWN]:
                locked = board.moveOrLockPiece(tetromino, Direction.DOWN)
                if (locked):
                    tetromino = board.newPieceOrGameOver(tetromino,tetrominonext)
                    if tetromino == None:
                        gameOver = True
            if keyInput[pygame.K_RETURN]:
                board.dropAndLockPiece(tetromino)
                tetromino = board.newPieceOrGameOver(tetromino,tetrominonext)
                if tetromino == None:
                    gameOver = True

        gameFlags = [newGame, gameOver, paused]
    
    #Game over screen loop
    while gameOver:
        screen.blit(bg,(0,0))#Clears screen by filling the screen with black color
        draw.drawGameOver(board)
        pygame.display.update()
        for event in pygame.event.get():
            gameQuit(gameOver)
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_n] or keyInput[pygame.K_p]:
                newGame = True
                gameOver = False

import copy, random #for generating blocks
import sys #needed to quit the pygame
import pygame
from enum import *

pygame.init()#initialising pygame

display_h = pygame.display.Info().current_h #system's height
pygame.display.set_caption("Tetris_group3")#sets the title of the screen
blockSize = display_h // 30 #1/30 of that height is a block, so that a 20 by 10 blocks tetris grid is visible in 2/3 rd by 1/3rd of the dispay screen
height = 25* blockSize
width=height+10
screen = pygame.display.set_mode((width, height))#initializes the game screen with given dimensions
bg = pygame.image.load('bg.jpg').convert()
screen.blit(bg,(0,0))
clock = pygame.time.Clock()#we need this to time the game and control frame rate (how fast the game progresses)

time=10
timer_seconds=time #the game is timed using this variable as a counter and  gets over after these many seconds

class Board :#defining functions for the tetris game's grid

    def __init__(self, colour = "Black"):
        self.colour = colour
        self.width = 10
        self.height = 20
        self.linesCleared = 0 #to keep track of score
        self.emptyGrid() #creating a 2D list to represent the grid.
        self.pieceList = [] #creating an array containing the tetromino pieces. Each tetromino is specified by the coordinates of its color.
        self.nextPiece=self.generatePiece() #the next piece that will come into play
        self.holeCount = None
        self.startInterval = 1000
        self.level = 1
        
    def emptyGrid(self):
        self.grid = []#creating a 2D list to represent the grid. 
        self.emptyRow = []
        for x in range(self.width):
            self.emptyRow.append(0)
        for rowCount in range(self.height):
            self.grid.append(copy.copy(self.emptyRow))

    def centrePiece(self, tetromino):#this moves the given tetromino form its default position at top left corner, to middle of top row which is where the pieces shouuld appear from initially.
        for coord in tetromino.vertexCoords:#iterating over the list of all vertex coordinates which are used to draw the piece.
            coord[0] += (self.width/2)-2  #for x coordinate of each vertex it is shifted to the middle of the grid
        tetromino.centre[0] += (self.width/2)-2 #tetromino.centre[0] is the x coordinate of the centre of tetromino and it is shifted by as much as the vertex is shifted to maintain shape of block
        for coord in tetromino.blockCoords:#done for the block coordinates
            coord[0] += (self.width/2)-2
        
    def generatePiece(self):
        if (len(self.pieceList) == 0):
            self.pieceList = list(Tetromino.Shapes.keys())
            random.shuffle(self.pieceList)
        tetromino = Tetromino(self.pieceList.pop())#returns a tetromino which is a 2d array of vertex coords, block coords and centre
        self.centrePiece(tetromino)
        return (tetromino)
    
    def isOutOfBounds(self, tetromino):
        minX = tetromino.getMinXCoord()
        maxX = tetromino.getMaxXCoord()
        minY = tetromino.getMinYCoord()
        maxY = tetromino.getMaxYCoord()
        if (minX < 0) or (minY < 0) or (maxX > self.width) or (maxY > self.height):
            return True
        else:
            return False

    def moveOrLockPiece(self, tetromino, direction, count = 1):
        x = direction.value[0]
        y = direction.value[1]
        for i in range(count):
            tetromino.incrementCoords(x, y)
            if (self.isOutOfBounds(tetromino) or self.isGridBlocked(tetromino)):
                tetromino.incrementCoords(-x,-y)
                if (y > 0):
                    self.lockPieceOnGrid(tetromino)
                    clearedRowCount = self.clearFullRows()
                    self.updateScores(clearedRowCount)
                    return True
        return False
    def updateScores(self, clearedRowCount):
        self.linesCleared += clearedRowCount

    def getDropInterval(self):
        scale = pow(0.8, self.level)
        dropInterval = int(self.startInterval * scale)
        return dropInterval

    def isGridBlocked(self, tetromino):
        for coord in tetromino.blockCoords:
            y = int(coord[1])
            x = int(coord[0])
            if self.grid[y][x] != 0:
                return True
        return False

    def lockPieceOnGrid(self, tetromino):
        for coord in tetromino.blockCoords:
            y = int(coord[1])
            x = int(coord[0])
            self.grid[y][x] = copy.copy(tetromino.colour)
    
    def clearFullRows(self):
        fullRowCount = 0
        y = self.height - 1
        while (y > 0):
            emptyBlocks = 0
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    emptyBlocks +=1
            if emptyBlocks == self.width:
                return fullRowCount
            elif emptyBlocks == 0:
                fullRowCount += 1
                self.grid[y] = copy.copy(self.emptyRow)
                for i in range (y, 1, -1):
                    self.grid[i] = copy.deepcopy(self.grid[i-1])
                y += 1
            y-=1
        return fullRowCount
         
    def rotatePiece(self, tetromino, rotation = None, count = 1):
        for i in range(count):
            tetromino.rotateCoords(rotation)
            if (self.isOutOfBounds(tetromino) or self.isGridBlocked(tetromino)):
                tetromino.rotateCoords(-rotation)
                break

    def newPieceOrGameOver(self, tetromino,tetrominonext):
        if (tetromino.xOffset == 0) and (tetromino.yOffset == 0):
            return None
        else:
            tetromino = tetrominonext
            return tetromino
    
    def dropAndLockPiece(self, tetromino):
        isLocked = False
        while (not isLocked):
            isLocked = self.moveOrLockPiece(tetromino,Direction.DOWN)

    def dropPieceWithoutLock(self, tetromino):
            while not ((self.isOutOfBounds(tetromino) or self.isGridBlocked(tetromino))):
                tetromino.incrementCoords(0, 1)
            tetromino.incrementCoords(0, -1)
    
    def moveLeftAndLockPiece(self, tetromino, count):
        self.moveOrLockPiece(tetromino, Direction.LEFT, count)
        self.dropAndLockPiece(tetromino)

class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
            
class Draw:
    

    def __init__(self):
        self.height=20
        self.boardWidth = 10 
        self.boardOffset = 4#leaves some left margin before start of the grid
        self.boardOutline = (blockSize // 15) if (blockSize >= 15) else 1#to see individual cells in board
        self.pieceOutline = (blockSize // 15) if (blockSize >= 15) else 1#to see tetromino piece in board
        self.boardRect = pygame.Rect(self.boardOffset*blockSize, self.boardOffset*blockSize, (self.boardWidth*blockSize
                                                                     ) + self.boardOutline, height-self.boardOffset)
        #pygame.Rect(x,y,w,h) creates a rectangle object of width w and height h whose top left corner is at position x,y 
        self.fontColour = (255, 0, 50) #font colour

    def drawBackground(self, board):
        self.drawBoard(board)

    def drawBoard(self, board):

        pygame.draw.rect(screen, board.colour, self.boardRect)        #pygame.draw.rect(surface, color of rect, pygame.rect,default=fill whole else specify width of border) draws the rect of specified color
        for x in range(self.boardOffset, (self.boardWidth + self.boardOffset)):#coordinates along width of grid
            for y in range(self.boardOffset, self.height+ self.boardOffset):#coordinates along height of grid
                cell = pygame.Rect(x*blockSize + self.boardOutline,
                                   y*blockSize + self.boardOutline,
                                   blockSize - self.boardOutline, blockSize - self.boardOutline)
                #adds margins to x and y coordinates and subtract margins from width and height coordinates to accomodate borders of each individual cell 
                pygame.draw.rect(screen, "White", cell)#draws each of the cells in the board grid

    def getScaledCoords(self, vertexCoords):#scaled coords of current tetromino at top centre of grid
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + self.boardOffset)*blockSize
            coord[1] = (coord[1]+self.boardOffset)*blockSize
        return copyCoords

    def getScaledCoords1(self, vertexCoords):#scaled coord of display for next tetromino at side of the grid
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + self.boardWidth+self.boardOffset-1)*blockSize
            coord[1] = (coord[1]+self.boardOffset+2)*blockSize
        return copyCoords
    def drawTetromino1(self, tetromino):
        pygame.draw.polygon(screen, tetromino.colour, self.getScaledCoords1(tetromino.vertexCoords))
    def drawTetromino(self, tetromino):
        pygame.draw.polygon(screen, tetromino.colour, self.getScaledCoords(tetromino.vertexCoords))
        pygame.draw.polygon(screen, "Black", self.getScaledCoords(tetromino.vertexCoords), self.pieceOutline)#draws a black outline surrounding the tetromino piece

    def drawGridPieces(self, board):
        for y in range(int(board.height)):
            for x in range(int(board.width)):
                if board.grid[y][x] != 0:
                    pygame.draw.rect(screen, board.grid[y][x], ((x+self.boardOffset)*blockSize, y*blockSize, blockSize, blockSize))

    def updateDisplay(self, board, tetromino):
        self.board = board
        self.tetromino = tetromino
        pygame.display.update()
    
    def drawStats(self, board):
        fontSize = int(1.5*blockSize)# Determine font size
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize, bold=True)# Load game font
        nextText = gameFont.render("Next piece", True, self.fontColour)# Render text
        time = gameFont.render(str(timer_seconds), True, self.fontColour)
        timeText = gameFont.render("Time remaining", True, self.fontColour)
        lineNum = gameFont.render(str(board.linesCleared), True, self.fontColour)
        lineText = gameFont.render("Lines cleared", True, self.fontColour)
        pauseText=gameFont.render("Press P to pause", True, self.fontColour)
        nextYPos = int(board.height*0.2)
        timeYPos = nextYPos + 6
        lineYPos = timeYPos + 4
        pauseYpos = lineYPos + 4
        screen.blit(nextText, ((self.boardOffset+11)*blockSize, (nextYPos)*blockSize))# Blit text onto the screen
        screen.blit(time, ((self.boardOffset+15)*blockSize, (timeYPos+1.5)*blockSize))
        screen.blit(timeText, ((self.boardOffset+11)*blockSize, (timeYPos)*blockSize))
        screen.blit(lineText, ((self.boardOffset+11)*blockSize, lineYPos*blockSize))
        screen.blit(lineNum, ((self.boardOffset+15)*blockSize, (lineYPos+1.5)*blockSize))
        screen.blit(pauseText, ((self.boardOffset+11)*blockSize, pauseYpos*blockSize))
    def draw_text_with_highlight(self,text, x, y,fontSize = int(2 * blockSize),highlight_color = (250, 200, 0)):
        # Render the text
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize,bold=True)# Get a font object with the system's first available font at the specified size
        text_surface = gameFont.render(text, True, self.fontColour)# Render text using the font, antialiasing enabled, with specified font color

        # Create a rectangle with the same size as the text
        rect = text_surface.get_rect()
        rect.topleft = (x, y)
        # Draw the highlight rectangle
        pygame.draw.rect(screen, highlight_color, rect)

        # Draw the text on top of the highlight and blit the rendered text onto the screen at a specific position
        screen.blit(text_surface, rect.topleft)
    def drawGameOver(self, board):
        self.draw_text_with_highlight("GAME OVER", blockSize*(self.boardWidth/2+2), (board.height/2-1)*blockSize)
        self.draw_text_with_highlight("PRESS N", blockSize*(self.boardWidth/2+3), (board.height/2+2)*blockSize)
    def drawStartScreen(self, board):
        self.draw_text_with_highlight("WELCOME TO TETRIS!", (self.boardWidth//2-1.5)*blockSize, ((board.height/2)-5)*blockSize,highlight_color = (20, 0, 200))
        self.draw_text_with_highlight("PRESS  A  :  AI MODE", (self.boardWidth//2-1)*blockSize, (board.height/2)*blockSize,highlight_color = (20, 200, 20))
        self.draw_text_with_highlight("PRESS  H  :  HUMAN", (self.boardWidth//2-0.7)*blockSize, ((board.height/2)+self.boardOffset+1)*blockSize,highlight_color = (100, 190, 200))

    def drawPauseScreen(self):
        self.draw_text_with_highlight("Game Menu!", (self.boardWidth//2+self.boardOffset-1)*blockSize, 3*blockSize,highlight_color = (80, 190, 200))
        self.draw_text_with_highlight("N:                        New Game", (self.boardWidth//2)*blockSize, 7*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("P:                        Pause/Unpause", (self.boardWidth//2 )*blockSize, 9*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Left Arrow:         Move Left", (self.boardWidth//2 )*blockSize, 11*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Right Arrow:      Move Right", (self.boardWidth//2 )*blockSize, 13*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Up Arrow:          Rotate", (self.boardWidth//2 )*blockSize, 15*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Space:               Hard Drop", (self.boardWidth//2 )*blockSize, 17*blockSize,  int(1.5*blockSize))

    def refreshScreen(self, board, tetromino,tetrominonext):
        screen.fill("Black")#Clears screen by filling the screen with black color
        self.drawBoard(board)#creating the grid
        self.drawTetromino(tetromino)
        self.drawStats(board)
        self.drawTetromino1(tetrominonext)#draw next tetromino piece        
        pygame.display.update()
        
class Rotation(IntEnum):
    CLOCKWISE = 1
    
class Tetromino():
    # Dictionary mapping color names to RGB tuples
    Colours = {
        
        "red" : (255,0,0),         #RGB tuples represent colors using three values: red, green, and blue.  
        "orange" : (255,163,47),    #Each component can have a value between 0 and 255
        "yellow" : (255,236,33),     #0 represents no intensity of that color   
        "green" : (147,240,59),       #255 represents the maximum intensity.
        "blue" : (55,138,255),
        "pink" : (255,119,253),
        "purple" : (149,82,234)}

    Shapes = {
        #Every shape is 3 element list where the first element is list of vertices, 
        #2nd is a list of top left corner co-ordinates of constituent blocks and
        #3rd is the centre of rotation 
        "O" : [ [[0,0],[2,0],[2,2],[0,2]], [[0,0],[1,0],[0,1],[1,1]], [1,1] ],
        "I" : [ [[0,0],[4,0],[4,1],[0,1]], [[0,0],[1,0],[2,0],[3,0]], [2,1] ], 
        "S" : [ [[1,0],[3,0],[3,1],[2,1],[2,2],[0,2],[0,1],[1,1]], [[1,0],[2,0],[0,1],[1,1]], [1.5,1.5] ],
        "Z" : [ [[0,0],[2,0],[2,1],[3,1],[3,2],[1,2],[1,1],[0,1]], [[0,0],[1,0],[1,1],[2,1]], [1.5,1.5] ],
        "J" : [ [[0,0],[3,0],[3,2],[2,2],[2,1],[0,1]], [[0,0],[1,0],[2,0],[2,1]], [1.5,0.5] ],
        "L" : [ [[0,0],[3,0],[3,1],[1,1],[1,2],[0,2]], [[0,0],[1,0],[2,0],[0,1]], [1.5,0.5] ],
        "T" : [ [[0,0],[3,0],[3,1],[2,1],[2,2],[1,2],[1,1],[0,1]], [[0,0],[1,0],[2,0],[1,1]], [1.5,0.5] ]
    }

    def __init__(self, shape = None):
        self.rotations = 0
        self.xOffset = 0
        self.yOffset = 0
        if self.Shapes.get(shape) is not None:
            self.shape = shape
        else:
            self.shape = random.choice(list(self.Shapes.keys()))
        self.vertexCoords = copy.deepcopy(self.Shapes[self.shape][0])#for more meaningful variables
        #and if we dont make deepcopy then vertex will keep shifting for every new game!
        self.blockCoords = self.Shapes[self.shape][1]
        self.centre = self.Shapes[self.shape][2]        
        self.colour = random.choice(list(self.Colours.values()))

    def getMinXCoord(self):
        x = 38400
        for coord in self.vertexCoords:
            if coord[0] < x:
                x = coord[0]
        return x
    
    def getMaxXCoord(self):
        x = 0
        for coord in self.vertexCoords:
            if coord[0] > x:
                x = coord[0]
        return x
    
    def getMinYCoord(self):
        y = 21600
        for coord in self.vertexCoords:
            if coord[1] < y:
                y = coord[1]
        return y

    def getMaxYCoord(self):
        y = 0
        for coord in self.vertexCoords:
            if coord[1] > y:
                y = coord[1]
        return y
    def incrementCoords(self, x = 0 , y = 0):
        self.xOffset += x
        self.yOffset += y
        self.centre[0] += x
        self.centre[1] += y
        for coord in self.vertexCoords:
            coord[0] += x
            coord[1] += y
        for coord in self.blockCoords:
            coord[0] += x
            coord[1] += y

    def rotateCoords(self, rotation = 0):
        if rotation != 0:
            self.rotations += rotation
            direction = rotation / abs(rotation)
            for i in range(abs(rotation)):
                for coord in self.vertexCoords:
                    x = coord[0] - self.centre[0]
                    y = coord[1] - self.centre[1]
                    coord[1] = self.centre[1] + (direction * x)
                    coord[0] = self.centre[0] - (direction * y)
                for coord in self.blockCoords:
                    x = coord[0] - self.centre[0]
                    y = coord[1] - self.centre[1]
                    coord[1] = self.centre[1] + (direction * x)
                    coord[0] = self.centre[0] - (direction * y)
                    #This line is needed to adjust so the block coord is always top left coord of "block"
                    coord[int((1 - direction)/2)] += -1

        
newGame = True
gameOver = False
paused = False
locked = False
draw = Draw()

def gameQuit(parameter=None):
    if event.type == pygame.QUIT: # If the user quits the game
        parameter = False # Exit the parameter's loop
        pygame.quit() # Quit pygame
        sys.exit() # Exit the script
                

while True:
    
    #reset game and timer
    if newGame:
        board = Board() # Create a new instance of the Board class
        tetromino = board.generatePiece() # Generate a new tetromino piece
        tetrominonext=board.generatePiece() # Generate the next tetromino piece
        screen.blit(bg,(0,0))#refresh the background image
        draw.drawStartScreen(board) # Draw the start screen
        timer_seconds=time # Set the timer_seconds variable to initial value of time
        timeCount = 0

    #newGame screen loop
        while newGame:
            pygame.display.update() # Update the display
            for event in pygame.event.get(): # Iterate over all events in the event queue
                gameQuit(newGame)
                keyInput = pygame.key.get_pressed() # Get the current state of all keyboard keys
                if keyInput[pygame.K_h]: # If the 'H' key is pressed
                    newGame = False # Exit the newGame loop
                if keyInput[pygame.K_a]: # If the 'A' key is pressed
                    newGame = False # Exit the newGame loop

    #Pause screen loop
    while paused:
        screen.blit(bg,(0,0))
        draw.drawPauseScreen()
        pygame.display.update()
        for event in pygame.event.get():
            gameQuit(paused)
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_p]:
                paused = False
            if keyInput[pygame.K_n]:
                newGame = True
                paused = False
 
    gameFlags = [newGame, gameOver, paused]

    #gamePlay Loop
    counter=0
    while (not any(gameFlags)):#while none of the game flags are true
        clock.tick(60)#tick(n) means the while loop and all code in it will run n times per second
        #Draw game elements to screen
        screen.fill("Black")#Clears screen by filling the screen with black color        
        draw.refreshScreen(board, tetromino,tetrominonext)
        
        counter+=1
        if counter%60==0:
            timer_seconds -= 1
        if timer_seconds == 0:
            gameOver=True
            timer_seconds=time#reset timer to initial value
 

        #Step game forward
        timeCount += clock.get_rawtime()
        if (timeCount >= board.getDropInterval()):
            timeCount = 0
            locked = board.moveOrLockPiece(tetromino, Direction.DOWN)
            if (locked):
                tetromino = board.newPieceOrGameOver(tetromino,tetrominonext)
                tetrominonext=board.generatePiece() # Generate the next tetromino piece
        
                if tetromino == None:
                    gameOver = True
                    break
            draw.refreshScreen(board, tetromino,tetrominonext)
        
        #Check for user input
        for event in pygame.event.get():
            gameQuit()
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_p]:
                paused = True
            if keyInput[pygame.K_n]:
                newGame = True
            if keyInput[pygame.K_UP]:
                board.rotatePiece(tetromino, Rotation.CLOCKWISE)
            if keyInput[pygame.K_RIGHT]:
                board.moveOrLockPiece(tetromino, Direction.RIGHT)
            if keyInput[pygame.K_LEFT]:
                board.moveOrLockPiece(tetromino, Direction.LEFT)
            if keyInput[pygame.K_DOWN]:
                locked = board.moveOrLockPiece(tetromino, Direction.DOWN)
                if (locked):
                    tetromino = board.newPieceOrGameOver(tetromino,tetrominonext)
                    if tetromino == None:
                        gameOver = True
            if keyInput[pygame.K_RETURN]:
                board.dropAndLockPiece(tetromino)
                tetromino = board.newPieceOrGameOver(tetromino,tetrominonext)
                if tetromino == None:
                    gameOver = True

        gameFlags = [newGame, gameOver, paused]
    
    #Game over screen loop
    while gameOver:
        screen.blit(bg,(0,0))#Clears screen by filling the screen with black color
        draw.drawGameOver(board)
        pygame.display.update()
        for event in pygame.event.get():
            gameQuit(gameOver)
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_n] or keyInput[pygame.K_p]:
                newGame = True
                gameOver = False
            

import copy, random #for generating blocks
import sys #needed to quit the pygame
import pygame

pygame.init()#initialising pygame

display_h = pygame.display.Info().current_h #system's height
blockSize = display_h // 30 #1/30 of that height is a block, so that a 20 by 10 blocks tetris grid is visible in 2/3 rd by 1/3rd of the dispay screen
height = 25* blockSize
width=height+10
screen = pygame.display.set_mode((width, height))#initializes the game screen with given dimensions
pygame.display.set_caption("Tetris_group3")#sets the title of the screen
bg = pygame.image.load('bg.jpg').convert()
screen.blit(bg,(0,0))
clock = pygame.time.Clock()#we need this to time the game and control frame rate (how fast the game progresses)

time=10
timer_seconds=time #the game is timed using this variable as a counter and  gets over after these many seconds

class Board :#defining functions for the tetris game's grid

    def __init__(self, colour = "Black"):
        self.colour = colour
        self.width = 10
        self.height = 20
        self.linesCleared = 0 #to keep track of score
        self.emptyGrid() #creating a 2D list to represent the grid.
        self.pieceList = [] #creating an array containing the tetromino pieces. Each tetromino is specified by the coordinates of its color.
        self.nextPiece=self.generatePiece() #the next piece that will come into play
        
    def emptyGrid(self):
        self.grid = []#creating a 2D list to represent the grid. 
        self.emptyRow = []
        for x in range(self.width):
            self.emptyRow.append(0)
        for rowCount in range(self.height):
            self.grid.append(self.emptyRow)

    def centrePiece(self, tetromino):#this moves the given tetromino form its default position at top left corner, to middle of top row which is where the pieces shouuld appear from initially.
        for coord in tetromino.vertexCoords:#iterating over the list of all vertex coordinates which are used to draw the piece.
            coord[0] += (self.width/2)-2  #for x coordinate of each vertex it is shifted to the middle of the grid
        tetromino.centre[0] += (self.width/2)-2 #tetromino.centre[0] is the x coordinate of the centre of tetromino and it is shifted by as much as the vertex is shifted to maintain shape of block
        for coord in tetromino.blockCoords:#done for the block coordinates
            coord[0] += (self.width/2)-2
        
    def generatePiece(self):
        if (len(self.pieceList) == 0):
            self.pieceList = list(Tetromino.Shapes.keys())
            random.shuffle(self.pieceList)
        tetromino = Tetromino(self.pieceList.pop())#returns a tetromino which is a 2d array of vertex coords, block coords and centre
        self.centrePiece(tetromino)
        return (tetromino)
            
class Draw:
    

    def __init__(self):
        self.height=20
        self.boardWidth = 10 
        self.boardOffset = 4#leaves some left margin before start of the grid
        self.boardOutline = (blockSize // 15) if (blockSize >= 15) else 1#to see individual cells in board
        self.pieceOutline = (blockSize // 15) if (blockSize >= 15) else 1#to see tetromino piece in board
        self.boardRect = pygame.Rect(self.boardOffset*blockSize, self.boardOffset*blockSize, (self.boardWidth*blockSize
                                                                     ) + self.boardOutline, height-self.boardOffset)
        #pygame.Rect(x,y,w,h) creates a rectangle object of width w and height h whose top left corner is at position x,y 
        self.fontColour = (255, 0, 50) #font colour

    def drawBoard(self, board):

        pygame.draw.rect(screen, board.colour, self.boardRect)        #pygame.draw.rect(surface, color of rect, pygame.rect,default=fill whole else specify width of border) draws the rect of specified color
        for x in range(self.boardOffset, (self.boardWidth + self.boardOffset)):#coordinates along width of grid
            for y in range(self.boardOffset, self.height+ self.boardOffset):#coordinates along height of grid
                cell = pygame.Rect(x*blockSize + self.boardOutline,
                                   y*blockSize + self.boardOutline,
                                   blockSize - self.boardOutline, blockSize - self.boardOutline)
                #adds margins to x and y coordinates and subtract margins from width and height coordinates to accomodate borders of each individual cell 
                pygame.draw.rect(screen, "White", cell)#draws each of the cells in the board grid

    def getScaledCoords(self, vertexCoords):#scaled coords of current tetromino at top centre of grid
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + self.boardOffset)*blockSize
            coord[1] = (coord[1]+self.boardOffset)*blockSize
        return copyCoords

    def getScaledCoords1(self, vertexCoords):#scaled coord of display for next tetromino at side of the grid
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + self.boardWidth+self.boardOffset-1)*blockSize
            coord[1] = (coord[1]+self.boardOffset+2)*blockSize
        return copyCoords
    def drawTetromino1(self, tetromino):
        pygame.draw.polygon(screen, tetromino.colour, self.getScaledCoords1(tetromino.vertexCoords))
    def drawTetromino(self, tetromino):
        pygame.draw.polygon(screen, tetromino.colour, self.getScaledCoords(tetromino.vertexCoords))
        pygame.draw.polygon(screen, "Black", self.getScaledCoords(tetromino.vertexCoords), self.pieceOutline)#draws a black outline surrounding the tetromino piece

    
    def drawStats(self, board):
        fontSize = int(1.5*blockSize)# Determine font size
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize, bold=True)# Load game font
        nextText = gameFont.render("Next piece", True, self.fontColour)# Render text
        time = gameFont.render(str(timer_seconds), True, self.fontColour)
        timeText = gameFont.render("Time remaining", True, self.fontColour)
        lineNum = gameFont.render(str(board.linesCleared), True, self.fontColour)
        lineText = gameFont.render("Lines cleared", True, self.fontColour)
        pauseText=gameFont.render("Press P to pause", True, self.fontColour)
        nextYPos = int(board.height*0.2)
        timeYPos = nextYPos + 6
        lineYPos = timeYPos + 4
        pauseYpos = lineYPos + 4
        screen.blit(nextText, ((self.boardOffset+11)*blockSize, (nextYPos)*blockSize))# Blit text onto the screen
        screen.blit(time, ((self.boardOffset+15)*blockSize, (timeYPos+1.5)*blockSize))
        screen.blit(timeText, ((self.boardOffset+11)*blockSize, (timeYPos)*blockSize))
        screen.blit(lineText, ((self.boardOffset+11)*blockSize, lineYPos*blockSize))
        screen.blit(lineNum, ((self.boardOffset+15)*blockSize, (lineYPos+1.5)*blockSize))
        screen.blit(pauseText, ((self.boardOffset+11)*blockSize, pauseYpos*blockSize))
    def draw_text_with_highlight(self,text, x, y,fontSize = int(2 * blockSize),highlight_color = (250, 200, 0)):
        # Render the text
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize,bold=True)# Get a font object with the system's first available font at the specified size
        text_surface = gameFont.render(text, True, self.fontColour)# Render text using the font, antialiasing enabled, with specified font color

        # Create a rectangle with the same size as the text
        rect = text_surface.get_rect()
        rect.topleft = (x, y)
        # Draw the highlight rectangle
        pygame.draw.rect(screen, highlight_color, rect)

        # Draw the text on top of the highlight and blit the rendered text onto the screen at a specific position
        screen.blit(text_surface, rect.topleft)
    def drawGameOver(self, board):
        self.draw_text_with_highlight("GAME OVER", blockSize*(self.boardWidth/2+2), (board.height/2-1)*blockSize)
        self.draw_text_with_highlight("PRESS N", blockSize*(self.boardWidth/2+3), (board.height/2+2)*blockSize)
    def drawStartScreen(self, board):
        self.draw_text_with_highlight("WELCOME TO TETRIS!", (self.boardWidth//2-1.5)*blockSize, ((board.height/2)-5)*blockSize,highlight_color = (20, 0, 200))
        self.draw_text_with_highlight("PRESS  A  :  AI MODE", (self.boardWidth//2-1)*blockSize, (board.height/2)*blockSize,highlight_color = (20, 200, 20))
        self.draw_text_with_highlight("PRESS  H  :  HUMAN", (self.boardWidth//2-0.7)*blockSize, ((board.height/2)+self.boardOffset+1)*blockSize,highlight_color = (100, 190, 200))

    def drawPauseScreen(self):
        self.draw_text_with_highlight("Game Menu!", (self.boardWidth//2+self.boardOffset-1)*blockSize, 3*blockSize,highlight_color = (80, 190, 200))
        self.draw_text_with_highlight("N:                        New Game", (self.boardWidth//2)*blockSize, 7*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("P:                        Pause/Unpause", (self.boardWidth//2 )*blockSize, 9*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Left Arrow:         Move Left", (self.boardWidth//2 )*blockSize, 11*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Right Arrow:      Move Right", (self.boardWidth//2 )*blockSize, 13*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Up Arrow:          Rotate", (self.boardWidth//2 )*blockSize, 15*blockSize, int(1.5*blockSize))
        self.draw_text_with_highlight("Space:               Hard Drop", (self.boardWidth//2 )*blockSize, 17*blockSize,  int(1.5*blockSize))

    def refreshScreen(self, board, tetromino,tetrominonext):
        screen.fill("Black")#Clears screen by filling the screen with black color
        self.drawBoard(board)#creating the grid
        self.drawTetromino(tetromino)
        self.drawStats(board)
        self.drawTetromino1(tetrominonext)#draw next tetromino piece        
        pygame.display.update()

class Tetromino():
    # Dictionary mapping color names to RGB tuples
    Colours = {
        
        "red" : (255,0,0),         #RGB tuples represent colors using three values: red, green, and blue.  
        "orange" : (255,163,47),    #Each component can have a value between 0 and 255
        "yellow" : (255,236,33),     #0 represents no intensity of that color   
        "green" : (147,240,59),       #255 represents the maximum intensity.
        "blue" : (55,138,255),
        "pink" : (255,119,253),
        "purple" : (149,82,234)}

    Shapes = {
        #Every shape is 3 element list where the first element is list of vertices, 
        #2nd is a list of top left corner co-ordinates of constituent blocks and
        #3rd is the centre of rotation 
        "O" : [ [[0,0],[2,0],[2,2],[0,2]], [[0,0],[1,0],[0,1],[1,1]], [1,1] ],
        "I" : [ [[0,0],[4,0],[4,1],[0,1]], [[0,0],[1,0],[2,0],[3,0]], [2,1] ], 
        "S" : [ [[1,0],[3,0],[3,1],[2,1],[2,2],[0,2],[0,1],[1,1]], [[1,0],[2,0],[0,1],[1,1]], [1.5,1.5] ],
        "Z" : [ [[0,0],[2,0],[2,1],[3,1],[3,2],[1,2],[1,1],[0,1]], [[0,0],[1,0],[1,1],[2,1]], [1.5,1.5] ],
        "J" : [ [[0,0],[3,0],[3,2],[2,2],[2,1],[0,1]], [[0,0],[1,0],[2,0],[2,1]], [1.5,0.5] ],
        "L" : [ [[0,0],[3,0],[3,1],[1,1],[1,2],[0,2]], [[0,0],[1,0],[2,0],[0,1]], [1.5,0.5] ],
        "T" : [ [[0,0],[3,0],[3,1],[2,1],[2,2],[1,2],[1,1],[0,1]], [[0,0],[1,0],[2,0],[1,1]], [1.5,0.5] ]
    }

    def __init__(self, shape = None):
        self.rotations = 0
        self.xOffset = 0
        self.yOffset = 0
        if self.Shapes.get(shape) is not None:
            self.shape = shape
        else:
            self.shape = random.choice(list(self.Shapes.keys()))
        self.vertexCoords = copy.deepcopy(self.Shapes[self.shape][0])#for more meaningful variables
        #and if we dont make deepcopy then vertex will keep shifting for every new game!
        self.blockCoords = self.Shapes[self.shape][1]
        self.centre = self.Shapes[self.shape][2]        
        self.colour = random.choice(list(self.Colours.values()))
        
newGame = True
gameOver = False
paused = False
draw = Draw()

def gameQuit(parameter=None):
    if event.type == pygame.QUIT: # If the user quits the game
        parameter = False # Exit the parameter's loop
        pygame.quit() # Quit pygame
        sys.exit() # Exit the script
                

while True:
    #reset game and timer
    if newGame:
        board = Board() # Create a new instance of the Board class
        tetromino = board.generatePiece() # Generate a new tetromino piece
        tetrominonext=board.generatePiece() # Generate the next tetromino piece
        screen.blit(bg,(0,0))#refresh the background image
        draw.drawStartScreen(board) # Draw the start screen
        timer_seconds=time # Set the timer_seconds variable to initial value of time
        

    #newGame screen loop
        while newGame:
            pygame.display.update() # Update the display
            for event in pygame.event.get(): # Iterate over all events in the event queue
                gameQuit(newGame)
                keyInput = pygame.key.get_pressed() # Get the current state of all keyboard keys
                if keyInput[pygame.K_h]: # If the 'H' key is pressed
                    newGame = False # Exit the newGame loop
                if keyInput[pygame.K_a]: # If the 'A' key is pressed
                    newGame = False # Exit the newGame loop

    #Pause screen loop
    while paused:
        screen.blit(bg,(0,0))
        draw.drawPauseScreen()
        pygame.display.update()
        for event in pygame.event.get():
            gameQuit(paused)
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_p]:
                paused = False
            if keyInput[pygame.K_n]:
                newGame = True
                paused = False
 
    gameFlags = [newGame, gameOver, paused]

    #gamePlay Loop
    counter=0
    while (not any(gameFlags)):#while none of the game flags are true
        clock.tick(60)#tick(n) means the while loop and all code in it will run n times per second
        #Draw game elements to screen
        screen.fill("Black")#Clears screen by filling the screen with black color        
        draw.refreshScreen(board, tetromino,tetrominonext)
        
        counter+=1
        if counter%60==0:
            timer_seconds -= 1
        if timer_seconds == 0:
            gameOver=True
            timer_seconds=time#reset timer to initial value
        
        #Check for user input
        for event in pygame.event.get():
            gameQuit()
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_p]:
                paused = True
            if keyInput[pygame.K_n]:
                newGame = True

        gameFlags = [newGame, gameOver, paused]
    tetromino=tetrominonext
    #Game over screen loop
    while gameOver:
        screen.blit(bg,(0,0))#Clears screen by filling the screen with black color
        draw.drawGameOver(board)
        pygame.display.update()
        for event in pygame.event.get():
            gameQuit(gameOver)
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_n] or keyInput[pygame.K_p]:
                newGame = True
                gameOver = False
                '''
