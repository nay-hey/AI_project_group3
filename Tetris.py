import pygame
import random
import copy
import sys
from collections import deque
from game import Game
from game1 import Game1

pygame.init()  # Initializing pygame

font_file = "Cyberverse Condensed Bold Italic.otf"  # Update with the correct file name
font = pygame.font.Font("Cyberverse Condensed Bold Italic.otf", 24)
display_h = pygame.display.Info().current_h 
display_w = pygame.display.Info().current_w # system's height
if display_h <= display_w:
    BLOCK_SIZE = display_h // 30

else:
    BLOCK_SIZE = display_w // 30
SCREEN_WIDTH_PERCENTAGE = 0.6  # 60%
SCREEN_HEIGHT_PERCENTAGE = 0.8  # 80%

# Calculating screen dimensions based on percentages
SCREEN_WIDTH= int(display_w* SCREEN_WIDTH_PERCENTAGE)
SCREEN_HEIGHT = int(display_h * SCREEN_HEIGHT_PERCENTAGE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # initializes the game screen with given dimensions
pygame.display.set_caption("Tetris_group3")  # sets the title of the screen
bg = pygame.image.load('bg10.jpg').convert()
screen.blit(bg, (0,0))
time = 300
timer_seconds = time  # the game is timed using this variable as a counter and gets over after these many seconds

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)


class Board:  # defining functions for the tetris game's grid

    def __init__(self):
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
    def __init__(self,font_file = font_file):
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
        self.font_file = font_file
    def draw_score(self, score, fontColour, boardOffset, height):
        fontSize = int(1.5 * BLOCK_SIZE)
        gameFont = pygame.font.Font(self.font_file, fontSize)
        score_text = gameFont.render("Score: " + str(score), True, self.fontColour1)
        screen.blit(score_text, ((boardOffset + 11) * BLOCK_SIZE, (height / 2 - 2) * BLOCK_SIZE))

    def drawHoles(self, num_holes, fontColour, boardOffset, height):
        fontSize = int(1.5 * BLOCK_SIZE)
        gameFont = pygame.font.Font(self.font_file, fontSize)
        holeText = gameFont.render("Holes:"+ str(num_holes), True, self.fontColour1)
        pauseYpos=int(self.height * 0.2)+14
        screen.blit(holeText, ((self.boardOffset + 11) * BLOCK_SIZE, (pauseYpos + 2) * BLOCK_SIZE))
  
    def draw_main_screen(self):
        # Assuming self.boardWidth and self.board.GRID_HEIGHT are available

        # Define text lines and their corresponding highlight colors
        text_lines = [
        ("WELCOME TO TETRIS!", (255, 0, 255)),  # Magenta
        ("PRESS  A  :  AI MODE", (255, 20, 147)),  # Deep pink
        ("PRESS  R  : RANDOM BLOCK", (255, 255, 255)),  # Black
        ("PRESS  I  :  AI GENERATED BLOCK", (184, 134, 11)),  # Dark goldenrod (dark yellow)
        ("PRESS  J  :  AI VS AI", (255, 140, 0))  # Dark orange
    ]


        # Calculate the base position for text alignment
        base_x = self.boardWidth // 2
        base_y = self.board.GRID_HEIGHT // 2

        # Define the vertical spacing between text lines
        line_spacing = 4

        # Calculate the total number of lines
        total_lines = len(text_lines)

        # Calculate the starting y position based on the number of lines and the line spacing
        start_y = base_y - ((total_lines - 1) * line_spacing) // 2
    
        border_color =  (0, 0, 20)  # Navy blue

        # Draw each text line with appropriate positioning
        for i, (text, highlight_color) in enumerate(text_lines):
            # Calculate the y position for the current line
            y_position = start_y + i * line_spacing

            # Draw the text with highlight
            text_surface = font.render(text, True, highlight_color)

            # Get the size of the rendered text surface
            text_width, text_height = text_surface.get_size()

            # Calculate the x position for centering the text
            x_position = base_x * 3 * BLOCK_SIZE - text_width // 2

            # Create a rectangle around the text with a border
            text_rect = pygame.Rect(x_position - 5, y_position * BLOCK_SIZE - 5, text_width + 10, text_height + 10)

            # Draw the rectangle with a navy blue border
            pygame.draw.rect(screen, border_color, text_rect)

            # Blit the text surface onto the screen
            screen.blit(text_surface, (x_position, y_position * BLOCK_SIZE))
                          

    def drawGameOver(self):
        gameFont = pygame.font.Font(self.font_file)
        self.draw_text_with_highlight("GAME OVER", BLOCK_SIZE * (self.boardWidth // 2 + 2),
                                      (self.board.GRID_HEIGHT // 2 - 2) * BLOCK_SIZE)  # Update here
 


    def drawPauseScreen(self):
        self.draw_text_with_highlight("Game Menu!", (self.boardWidth // 2 + self.boardOffset - 1) * BLOCK_SIZE,
                                    3 * BLOCK_SIZE, highlight_color=(80, 190, 200))
        self.draw_text_with_highlight("N:                New Game", (self.boardWidth // 2) * BLOCK_SIZE,
                                    7 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("P:                Pause/Unpause", (self.boardWidth // 2) * BLOCK_SIZE,
                                    9 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("Left Arrow:        Move Left", (self.boardWidth // 2) * BLOCK_SIZE,
                                    11 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("Right Arrow:      Move Right", (self.boardWidth // 2) * BLOCK_SIZE,
                                    13 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("Up Arrow:         Rotate", (self.boardWidth // 2) * BLOCK_SIZE,
                                    15 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("Down Arrow:       Move down", (self.boardWidth // 2) * BLOCK_SIZE,
                                    17 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))
        self.draw_text_with_highlight("Space:            Hard Drop", (self.boardWidth // 2) * BLOCK_SIZE,
                                    19 * BLOCK_SIZE, int(1.5 * BLOCK_SIZE))

    def drawStats(self, board, timer_seconds):
        fontSize = int(1.5 * BLOCK_SIZE)
        gameFont = pygame.font.Font(self.font_file, fontSize)
        timeText = gameFont.render("Time remaining", True, (255, 255, 255))  # White text
        pauseText = gameFont.render("Press P to pause", True, (255, 255, 255))  # White text
        nextYPos = int(self.height * 0.2)
        timeYPos = nextYPos + 6
        lineYPos = timeYPos + 4
        pauseYpos = lineYPos + 4
        screen.blit(timeText, ((self.boardOffset + 11) * BLOCK_SIZE, (timeYPos) * BLOCK_SIZE))
        screen.blit(pauseText, ((self.boardOffset + 11) * BLOCK_SIZE, pauseYpos * BLOCK_SIZE))
        score_text = gameFont.render("Score: {}".format(board.score), True, (255, 255, 255))  # White text
        high_score_text = gameFont.render("High Score: {}".format(board.high_score), True, (255, 255, 255))  # White text
        screen.blit(high_score_text, ((self.boardOffset + 11) * BLOCK_SIZE, (pauseYpos + 4) * BLOCK_SIZE))


        time_surface = gameFont.render(str(timer_seconds), True, (255, 255, 255))  # White text
        screen.blit(time_surface, ((self.boardOffset + 15) * BLOCK_SIZE, (timeYPos + 1.5) * BLOCK_SIZE))

    def draw_text_with_highlight(self, text, x, y, fontSize=int(2 * BLOCK_SIZE), highlight_color=(250, 200, 0)):
        gameFont = pygame.font.Font(self.font_file, fontSize)
        text_surface = gameFont.render(text, True, (255, 255, 255))  # White text
        rect = text_surface.get_rect()
        rect.topleft = (x, y)
        pygame.draw.rect(screen, highlight_color, rect)
        screen.blit(text_surface, rect.topleft)


class Tetromino:
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[2, 2, 2], [0, 2, 0]],  # T
        [[3, 3, 3], [3, 0, 0]],  # L
        [[4, 4, 4], [0, 0, 4]],  # J
        [[0, 5, 5], [5, 5, 0]],  # S
        [[6, 6], [6, 6]],  # O
        [[7, 7, 0], [0, 7, 7]]  # Z
    ]

    BLOCK_IMAGES = {
        0: "windowIcon1.png",   # Image for block index 1
        1: "windowIcon2.png",  # Image for block index 2
        2: "windowIcon3.png",  # Image for block index 3
        3: "windowIcon4.png",  # Image for block index 4
        4: "windowIcon5.png",  # Image for block index 5
        5: "windowIcon6.png",  # Image for block index 6
        6: "windowIcon7.png"   # Image for block index 7
    }
