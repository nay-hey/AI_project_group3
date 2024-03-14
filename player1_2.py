import pygame
import random, copy
import sys

# Define constants
pygame.init()
display_h = pygame.display.Info().current_h  # system's height
pygame.display.set_caption("Tetris_group3")  # sets the title of the screen
GRID_WIDTH = 20
GRID_HEIGHT = 20
screen = pygame.display.set_mode((GRID_WIDTH * 30, GRID_HEIGHT * 30))  # initializes the game screen with given dimensions
bg = pygame.image.load('bg.jpg').convert()
screen.blit(bg, (0, 0))
BLOCK_SIZE = display_h // 30
SCREEN_HEIGHT = 25 * BLOCK_SIZE
SCREEN_WIDTH = SCREEN_HEIGHT + 10
time = 10
timer_seconds = time  # the game is timed using this variable as a counter and  gets over after these many seconds
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

class Board:  # defining functions for the tetris game's grid

    def __init__(self, colour="Black"):
        self.colour = colour
        self.width = 10
        self.height = 20
        self.score = 0
        self.linesCleared = 0  # to keep track of score
        # self.emptyGrid() #creating a 2D list to represent the grid.
        self.pieceList = []  # creating an array containing the tetromino pieces. Each tetromino is specified by the coordinates of its color.
        # self.nextPiece=self.generatePiece() #the next piece that will come into play


class Draw:
    def __init__(self):
        self.height = 20
        self.boardWidth = 10
        self.boardOffset = 4  # leaves some left margin before start of the grid
        self.boardOutline = (BLOCK_SIZE // 15) if (BLOCK_SIZE >= 15) else 1  # to see individual cells in board
        self.pieceOutline = (BLOCK_SIZE // 15) if (BLOCK_SIZE >= 15) else 1  # to see tetromino piece in board
        self.boardRect = pygame.Rect(self.boardOffset * BLOCK_SIZE, self.boardOffset * BLOCK_SIZE,
                                      (self.boardWidth * BLOCK_SIZE) + self.boardOutline,
                                      GRID_HEIGHT - self.boardOffset)
        self.fontColour = (255, 0, 50)  # font colour
    def draw_main_screen(self):
        self.draw_text_with_highlight("WELCOME TO TETRIS!", (self.boardWidth//2-1.5)*BLOCK_SIZE, ((GRID_HEIGHT/2)-5)*BLOCK_SIZE,highlight_color = (20, 0, 200))
        self.draw_text_with_highlight("PRESS  A  :  AI MODE", (self.boardWidth//2-1)*BLOCK_SIZE, (GRID_HEIGHT/2)*BLOCK_SIZE,highlight_color = (20, 200, 20))
        self.draw_text_with_highlight("PRESS  H  :  HUMAN", (self.boardWidth//2-0.7)*BLOCK_SIZE, ((GRID_HEIGHT/2)+self.boardOffset+1)*BLOCK_SIZE,highlight_color = (100, 190, 200))
    def drawGameOver(self, board):
        self.draw_text_with_highlight("GAME OVER", BLOCK_SIZE*(self.boardWidth/2+2), (board.height/2-1)*BLOCK_SIZE)
        self.draw_text_with_highlight("PRESS N", BLOCK_SIZE*(self.boardWidth/2+3), (board.height/2+2)*BLOCK_SIZE)
    def drawBoard(self, board):

        pygame.draw.rect(screen, board.colour, self.boardRect)        #pygame.draw.rect(surface, color of rect, pygame.rect,default=fill whole else specify width of border) draws the rect of specified color
        for x in range(self.boardOffset, (self.boardWidth + self.boardOffset)):#coordinates along width of grid
            for y in range(self.boardOffset, self.height+ self.boardOffset):#coordinates along height of grid
                cell = pygame.Rect(x*BLOCK_SIZE + self.boardOutline,
                                   y*BLOCK_SIZE + self.boardOutline,
                                   BLOCK_SIZE - self.boardOutline, BLOCK_SIZE - self.boardOutline)
                #adds margins to x and y coordinates and subtract margins from width and height coordinates to accomodate borders of each individual cell 
                pygame.draw.rect(screen, "White", cell)#draws each of the cells in the board grid

    def drawStats(self, board):
        fontSize = int(1.5*BLOCK_SIZE)# Determine font size
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
        screen.blit(nextText, ((self.boardOffset+11)*BLOCK_SIZE, (nextYPos)*BLOCK_SIZE))# Blit text onto the screen
        screen.blit(time, ((self.boardOffset+15)*BLOCK_SIZE, (timeYPos+1.5)*BLOCK_SIZE))
        screen.blit(timeText, ((self.boardOffset+11)*BLOCK_SIZE, (timeYPos)*BLOCK_SIZE))
        screen.blit(lineText, ((self.boardOffset+11)*BLOCK_SIZE, lineYPos*BLOCK_SIZE))
        screen.blit(lineNum, ((self.boardOffset+15)*BLOCK_SIZE, (lineYPos+1.5)*BLOCK_SIZE))
        screen.blit(pauseText, ((self.boardOffset+11)*BLOCK_SIZE, pauseYpos*BLOCK_SIZE))
    

    def draw_text_with_highlight(self, text, x, y, fontSize=int(2 * BLOCK_SIZE), highlight_color=(250, 200, 0)):
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0], size=fontSize, bold=True)
        text_surface = gameFont.render(text, True, self.fontColour)
        rect = text_surface.get_rect()
        rect.topleft = (x, y)
        pygame.draw.rect(screen, highlight_color, rect)
        screen.blit(text_surface, rect.topleft)
    def getScaledCoords(self, vertexCoords):#scaled coords of current tetromino at top centre of grid
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + self.boardOffset)*BLOCK_SIZE
            coord[1] = (coord[1]+self.boardOffset)*BLOCK_SIZE
        return copyCoords

    def getScaledCoords1(self, vertexCoords):#scaled coord of display for next tetromino at side of the grid
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + self.boardWidth+self.boardOffset-1)*BLOCK_SIZE
            coord[1] = (coord[1]+self.boardOffset+2)*BLOCK_SIZE
        return copyCoords
    
class Tetromino():
    SHAPE_COLORS = [
    (255, 0, 0),
    (255,163,47),
    (255,236,33),
    (147,240,59),
    (55,138,255),
    (255,119,253),
    (149,82,234)
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
        self.clock = pygame.time.Clock()
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.score = 0
        self.game_over = False
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        self.board = Board()  # Instantiate Board object
        self.drawer = Draw()

    def new_piece(self):
        return random.choice(Tetromino.SHAPES)

    def draw_grid(self):
        screen.fill(BLACK)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = WHITE if self.grid[y][x] == 0 else Tetromino.SHAPE_COLORS[self.grid[y][x] - 1]
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self, piece, offset_x, offset_y):
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x]:
                    color = Tetromino.SHAPE_COLORS[piece[y][x] - 1]
                    pygame.draw.rect(screen, color,
                                     ((x + offset_x) * BLOCK_SIZE, (y + offset_y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, GRAY,
                                     ((x + offset_x) * BLOCK_SIZE, (y + offset_y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def drop_piece_hard(self):
        while not self.check_collision(self.current_piece, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        self.merge_piece()
        self.current_piece = self.new_piece()
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        if self.check_collision(self.current_piece, self.piece_x, self.piece_y):
            self.game_over = True
                
    def move_piece_down(self):
        if not self.check_collision(self.current_piece, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        else:
            self.merge_piece()
            self.current_piece = self.new_piece()
            self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
            self.piece_y = 0
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
                        y + offset_y < 0 or y + offset_y >= GRID_HEIGHT or
                        x + offset_x < 0 or x + offset_x >= GRID_WIDTH or
                        self.grid[y + offset_y][x + offset_x] != 0
                ):
                    return True
        return False

    def merge_piece(self):
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                if self.current_piece[y][x]:
                    self.grid[y + self.piece_y][x + self.piece_x] = self.current_piece[y][x]

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1
        self.score += lines_cleared ** 2

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece_right()
                    elif event.key == pygame.K_DOWN:
                        self.move_piece_down()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:  # Added for drop hard feature
                        self.drop_piece_hard()
            self.move_piece_down()
            self.clear_lines()

            self.draw_grid()
            self.draw_piece(self.current_piece, self.piece_x, self.piece_y)
            pygame.display.update()
            self.clock.tick(10)  # Adjust game speed

if __name__ == "__main__":
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
                        # Handle human mode if needed
                        pass
                elif current_screen == "tetris":
                    # Handle Tetris game controls
                    pass

        if current_screen == "main":
            screen.blit(bg, (0, 0))  # Blit the background image onto the screen
            drawer.draw_main_screen()
            pygame.display.update()
        elif current_screen == "tetris":
            screen.blit(bg, (0, 0))  # Blit the background image onto the screen
            drawer.draw_main_screen()
            pygame.display.update()
