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
        self.boardOffset = 4  # leaves some left margin before start of the grid
        self.boardOutline = (BLOCK_SIZE // 15) if (BLOCK_SIZE >= 15) else 1  # to see individual cells in board
        self.pieceOutline = (BLOCK_SIZE // 15) if (BLOCK_SIZE >= 15) else 1  # to see tetromino piece in board
        self.boardRect = pygame.Rect(self.boardOffset * BLOCK_SIZE, self.boardOffset * BLOCK_SIZE,
                                      (self.boardWidth * BLOCK_SIZE) + self.boardOutline,
                                      self.board.GRID_HEIGHT - self.boardOffset)
        self.fontColour = (255, 0, 50)  # font colour
    def draw_score(self, score, fontColour, boardOffset, height):
        fontSize = int(1.5 * BLOCK_SIZE)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
        score_text = gameFont.render("Score: " + str(score), True, fontColour)
        screen.blit(score_text, ((boardOffset + 11) * BLOCK_SIZE, (height / 2 - 2) * BLOCK_SIZE))

    def draw_height(self, height, fontColour, boardOffset, height1):
        fontSize = int(1.5 * BLOCK_SIZE)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
        height_text = gameFont.render("Max Height: " + str(height), True, fontColour)
        screen.blit(height_text, ((boardOffset + 11) * BLOCK_SIZE, (height1 / 2 - 4) * BLOCK_SIZE))

    def drawHoles(self, num_holes, fontColour, boardOffset, height):
        fontSize = int(1.5 * BLOCK_SIZE)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
        holeText = gameFont.render("Holes:"+ str(num_holes), True, fontColour)
        screen.blit(holeText, ((boardOffset + 11) * BLOCK_SIZE, (height / 2 - 8) * BLOCK_SIZE))
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
                                      (self.board.GRID_HEIGHT // 2 - 1) * BLOCK_SIZE)  # Update here
 


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
        self.draw_text_with_highlight("Space:               Hard Drop", (self.boardWidth // 2) * BLOCK_SIZE,
                                      17 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))

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
        timeText = gameFont.render("Time remaining", True, self.fontColour)
        lineNum = gameFont.render(str(board.linesCleared), True, self.fontColour)
        lineText = gameFont.render("Lines cleared", True, self.fontColour)
        pauseText = gameFont.render("Press P to pause", True, self.fontColour)
        nextYPos = int(self.height * 0.2)
        timeYPos = nextYPos + 6
        lineYPos = timeYPos + 4
        pauseYpos = lineYPos + 4
        screen.blit(timeText, ((self.boardOffset + 11) * BLOCK_SIZE, (timeYPos) * BLOCK_SIZE))
        screen.blit(lineText, ((self.boardOffset + 11) * BLOCK_SIZE, lineYPos * BLOCK_SIZE))
        screen.blit(lineNum, ((self.boardOffset+15)*BLOCK_SIZE, (lineYPos+1.5)*BLOCK_SIZE))
        screen.blit(pauseText, ((self.boardOffset + 11) * BLOCK_SIZE, pauseYpos * BLOCK_SIZE))
        score_text = gameFont.render("Score: {}".format(board.score), True, self.fontColour)
        high_score_text = gameFont.render("High Score: {}".format(board.high_score), True, self.fontColour)
        screen.blit(score_text, ((self.boardOffset + 11) * BLOCK_SIZE, (pauseYpos + 4) * BLOCK_SIZE))
        screen.blit(high_score_text, ((self.boardOffset + 11) * BLOCK_SIZE, (pauseYpos + 6) * BLOCK_SIZE))
        

        time_surface = gameFont.render(str(timer_seconds), True, self.fontColour)
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
        self.piece_x = self.board.GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0

    def new_piece(self):
        next_piece = random.choice(Tetromino.SHAPES)
        self.next_piece = next_piece  # Update next piece
        return next_piece
    def draw_grid(self):
        screen.fill(BLACK)
        for y in range(self.board.GRID_HEIGHT):
            for x in range(self.board.GRID_WIDTH):
                color = WHITE if self.grid[y][x] == 0 else Tetromino.SHAPE_COLORS[self.grid[y][x] - 1]
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self, piece, offset_x, offset_y):
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x]:
                    color = Tetromino.SHAPE_COLORS[piece[y][x] - 1]
                    pygame.draw.rect(screen, color,
                                     ((x + offset_x) * BLOCK_SIZE, (y + offset_y) * BLOCK_SIZE, BLOCK_SIZE,
                                      BLOCK_SIZE))
                    pygame.draw.rect(screen, GRAY,
                                     ((x + offset_x) * BLOCK_SIZE, (y + offset_y) * BLOCK_SIZE, BLOCK_SIZE,
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
            for y in range(max_height, self.board.GRID_HEIGHT):  # Start from the top of the grid
                if self.grid[y][x] != 0:  # If we encounter a filled cell
                    hole_found = True  # Update flag to indicate that a filled cell has been found
                elif hole_found:  # If a filled cell has been found and we encounter an empty cell
                    num_holes += 1  # Count it as a hole
        return num_holes

    def run(self):
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
            if not self.paused:  # Only update the game if not paused
                self.move_piece_down()
                self.clear_lines()
            self.draw_grid()
            fontSize = int(1.5 * BLOCK_SIZE)
            nextYPos = int(self.drawer.height * 0.2)
            gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
            nextText = gameFont.render("Next piece", True, self.drawer.fontColour)
            self.draw_piece(self.next_piece, self.board.GRID_WIDTH + 7, 6)  # Draw next piece
            screen.blit(nextText, ((self.drawer.boardOffset + 12) *BLOCK_SIZE, (nextYPos) * BLOCK_SIZE))
            self.draw_piece(self.current_piece, self.piece_x, self.piece_y)
            self.drawer.drawStats(self.board, timer_seconds)
            self.drawer.draw_score(self.score, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            filled_rows = sum(1 for row in self.grid if any(row))
            self.drawer.draw_height(filled_rows, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            max_height_range = (0, filled_rows)
            num_holes = self.count_holes_in_range(filled_rows)
            self.drawer.drawHoles(num_holes, self.drawer.fontColour, self.drawer.boardOffset, self.drawer.height)
            pygame.display.update()
            self.clock.tick(5)  # Adjust game speed
            if timer_seconds == 0:
                self.game_over = True
            else:
                timer_seconds -= 1
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
                        game.run()
                    elif event.key == pygame.K_a:
                        current_screen = "tetris"
                        game.run()
                    elif event.key == pygame.K_p:  # Pause/unpause when P key is pressed
                        game.paused = not game.paused
                elif current_screen == "tetris":
                    if event.key == pygame.K_p:  # Pause/unpause when P key is pressed
                        game.paused = not game.paused
                    elif game.game_over and event.key == pygame.K_n:  # Restart the game if 'N' is pressed
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
        elif current_screen == "tetris":
            if game.paused:  # If paused, only draw the pause screen
                screen.blit(bg, (0, 0))
                drawer.drawPauseScreen()
            elif game.game_over:  # If the game is over, switch to the game over screen
                current_screen = "game_over_screen"
            else:
                screen.blit(bg, (0, 0))  # Blit the background image onto the screen
                drawer.drawBoard(game.board)
                game.draw_grid()
                game.draw_piece(game.current_piece, game.piece_x, game.piece_y)
                drawer.drawStats(game.board, timer_seconds)
                pygame.display.update()
        elif current_screen == "game_over_screen":
                screen.blit(bg, (0, 0))
                drawer.drawGameOver()
                drawer.draw_text_with_highlight("Score: " + str(game.score), BLOCK_SIZE * (game.board.GRID_WIDTH // 2 - 1),
                                (game.board.GRID_HEIGHT // 2 + 2) * BLOCK_SIZE)
                drawer.draw_text_with_highlight("High Score: {}".format(game.board.high_score), BLOCK_SIZE * (game.board.GRID_WIDTH // 2 - 1),
                                                (game.board.GRID_HEIGHT // 2 + 4) * BLOCK_SIZE)  # Adjusted position for high score
                drawer.draw_text_with_highlight("PRESS N to play again", BLOCK_SIZE * (game.board.GRID_WIDTH // 2 - 2),
                                                (game.board.GRID_HEIGHT // 2 + 6) * BLOCK_SIZE)  # Adjusted position for play again
                pygame.display.update()
                timer_seconds = time

    
    
