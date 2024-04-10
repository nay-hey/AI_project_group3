
from time import sleep
import pygame
import sys
import random
from random import choice
from copy import deepcopy,copy
import numpy as np
from random import randint



pygame.init()
timer_seconds = 100
clock = pygame.time.Clock()
BLACK = (0, 0, 50)
WHITE = 255, 255, 255
GREEN = (0, 255, 0)
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



RED = "windowIcon1.png"
ORANGE = "windowIcon2.png"
YELLOW = "windowIcon3.png"
GREEN = "windowIcon4.png"
CYAN = "windowIcon5.png"
INDIGO = "windowIcon6.png"
TURQ = "windowIcon7.png"

BODIES = [
    (((0, 0), (0, 1), (0, 2), (1, 2)), RED),  # L
    (((0, 0), (1, 0), (2, 0), (1, 1)), ORANGE),  # T
    (((0, 0), (1, 0), (1, 1), (1, 2)), YELLOW),  # J
    (((0, 0), (0, 1), (0, 2), (0, 3)), GREEN),  # I
    (((1, 0), (2, 0), (0, 1), (1, 1)), CYAN),  # S
    (((0, 0), (1, 0), (0, 1), (1, 1)), INDIGO),  # O
    (((0, 0), (1, 0), (1, 1), (2, 1)), TURQ),  # Z
]


A = 0.5
B = 0.5


class Greedy_AI:
    def get_best_move(self, board, piece, depth=1):
        best_x = -1
        best_piece = None
        min_cost = 100000000
        # moves = []
        for i in range(4):
            piece = piece.get_next_rotation()
            for x in range(board.width):
                try:
                    y = board.drop_height(piece, x)
                except:
                    continue
                c = self.cost(board.board, x, y, piece)
                if c < min_cost:
                    min_cost = c
                    best_x = x
                    best_y = y
                    best_piece = piece
        # return best_x, best_piece
        return best_x, best_piece

    def cost(self, board, x, y, piece):

        board_copy = deepcopy(board)

        for pos in piece.body:
            board_copy[y + pos[1]][x + pos[0]] = True

        holes = 0
        max_height = 0
        num_cleared = 0
        cum_wells = 0
        for i in range(len(board_copy)):
            if all(board_copy[i]):
                num_cleared += 1
            for j in range(len(board_copy[0])):

                if board_copy[i][j]:
                    max_height = max(max_height, i)
                    continue
                has = False
                for k in range(i + 1, len(board_copy)):
                    if board_copy[k][j]:
                        has = True
                        break
                if has:
                    # has a block above
                    holes += 1
        agg_height = 0
        for col in range(len(board_copy[i])):
            agg = 0
            for row in range(len(board_copy)):
                if board_copy[row][col]:
                    agg = row
            agg_height += agg
        heights = []
        for col in range(len(board_copy[i])):
            mh = 0
            for row in range(len(board_copy)):
                if board_copy[row][col]:
                    mh = row
            heights.append(mh)
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])

        c = 0.5 * agg_height + 0.35 * holes + 0.18 * bumpiness - 0.76 * num_cleared
        # c = agg_height + holes + bumpiness - num_cleared
        
        return c


class Piece:
    def __init__(self, body=None, color=None):
        if body == None:
            self.body, self.color = choice(BODIES)
        else:
            self.body = body
            self.color = color
        self.skirt = self.calc_skirt()

    def calc_skirt(self):
        skirt = []
        for i in range(4):
            low = 1000
            for b in self.body:
                if b[0] == i:
                    low = min(low, b[1])
            if low != 1000:
                skirt.append(low)
        return skirt

    def get_next_rotation(self):
        width = len(self.skirt)
        # height = max([b[1] for b in self.body])
        new_body = [(width - b[1], b[0]) for b in self.body]
        leftmost = min([b[0] for b in new_body])
        new_body = [(b[0] - leftmost, b[1]) for b in new_body]
        return Piece(new_body, self.color)


def main():
    for b in BODIES:
        p = Piece(b)
        print(p.skirt)


if __name__ == "__main__":
    main()


class Board:
    def __init__(self):
        self.width, self.height = 10, 20
        self.board = self.init_board()
        self.colors = self.init_board()
        self.widths = [0] * (self.height + 4)
        self.heights = [0] * self.width

    def init_board(self):
        b = []
        for row in range(self.height + 4):
            row = []
            for col in range(self.width):
                row.append(False)
            b.append(row)
        return b

    def undo(self):
        self.board = self.last_board
        self.colors = self.last_colors
        self.widths = self.last_widths
        self.heights = self.last_heights

    def place(self, x, y, piece):
        # check if valid
        for pos in piece.body:
            target_y = y + pos[1]
            target_x = x + pos[0]
            if (
                target_y < 0
                or target_y >= self.height + 4
                or target_x < 0
                or target_x >= self.width
                or self.board[y + pos[1]][x + pos[0]]
            ):
                return Exception("Bad placement")
        for pos in piece.body:
            self.board[y + pos[1]][x + pos[0]] = True
            self.colors[y + pos[1]][x + pos[0]] = piece.color
            self.widths[y + pos[1]] += 1
            self.heights[x + pos[0]] = max(self.heights[x + pos[0]], y + pos[1] + 1)
        return 0

    def drop_height(self, piece, x):
        y = -1
        for i in range(len(piece.skirt)):
            y = max(self.heights[x + i] - piece.skirt[i], y)
        return y

    def top_filled(self):
        return sum([w for w in self.widths[-4:]]) > 0

    def clear_rows(self):
        num = 0
        to_delete = []
        for i in range(len(self.widths)):
            if self.widths[i] < self.width:
                continue
            num += 1
            to_delete.append(i)

        for row in to_delete:
            del self.board[row]
            self.board.append([False] * self.width)

            del self.widths[row]
            self.widths.append(0)

            del self.colors[row]
            self.colors.append([False] * self.width)

        if num > 0:
            heights = []
            for col in range(self.width):
                m = 0
                for row in range(self.height):
                    if self.board[row][col]:
                        m = row + 1
                heights.append(m)
            # print(heights)
            self.heights = heights
        return num

class Game:
    def __init__(self, mode, agent=None):
        self.board = Board()
        pygame.init()
        self.curr_piece = Piece()
        self.y = 20
        self.x = 5
        self.screenWidth = 400
        self.screenHeight = 600
        self.top = 0
        self.pieces_dropped = 0
        self.rows_cleared = 0
        self.image_dict = {
            'windowIcon1.png': pygame.image.load("windowIcon1.png"),
            'windowIcon2.png': pygame.image.load("windowIcon2.png"),
            'windowIcon3.png': pygame.image.load("windowIcon3.png"),
            'windowIcon4.png': pygame.image.load("windowIcon4.png"),
            'windowIcon5.png': pygame.image.load("windowIcon5.png"),
            'windowIcon6.png': pygame.image.load("windowIcon6.png"),
            'windowIcon7.png': pygame.image.load("windowIcon7.png"),
        }
        if mode == "greedy":
            self.ai = Greedy_AI()
        elif mode == "genetic":
            pass
        else:
            self.ai = None

    def run_no_visual(self):
        if self.ai == None:
            return -1
        while True:
            x, piece = self.ai.get_best_move(self.board, self.curr_piece)
            self.curr_piece = piece
            y = self.board.drop_height(self.curr_piece, x)
            self.drop(y, x=x)
            if self.board.top_filled():
                break
        print(self.pieces_dropped, self.rows_cleared)
        return self.pieces_dropped, self.rows_cleared

    def run(self):
        pygame.init()
        global timer_seconds
        self.screenSize = self.screenWidth+300, self.screenHeight
        self.pieceHeight = (self.screenHeight - self.top) / self.board.height
        self.pieceWidth = self.screenWidth / self.board.width -10
        self.screen = pygame.display.set_mode(self.screenSize )
        running = True
        if self.ai != None:
            MOVEEVENT, t = pygame.USEREVENT + 1, 100
        else:
            MOVEEVENT, t = pygame.USEREVENT + 1, 500
        pygame.time.set_timer(MOVEEVENT, t)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    running = False
                if self.ai != None:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    if event.type == MOVEEVENT:
                        x, piece = self.ai.get_best_move(self.board, self.curr_piece)
                        self.curr_piece = piece

                        while self.x != x:
                            if self.x - x < 0:
                                self.x += 1
                            else:
                                self.x -= 1
                            self.y -= 1
                            for i in range(10):
                                for j in range(20):
                                    pygame.draw.rect(self.screen, BLACK, (i*self.pieceWidth,j*self.pieceHeight,self.pieceWidth-1, self.pieceHeight-1))
                           
                            self.draw()
                            pygame.display.flip()
                            sleep(0.01)

                        y = self.board.drop_height(self.curr_piece, x)
                        while self.y != y:
                            self.y -= 1

                            for i in range(10):
                                for j in range(20):
                                    pygame.draw.rect(self.screen, BLACK, (i*self.pieceWidth,j*self.pieceHeight,self.pieceWidth-2, self.pieceHeight-2))
                           
                            self.draw()
                            pygame.display.flip()
                            sleep(0.01)

                        self.drop(y, x=x)
                        if self.board.top_filled():
                            running = False
                            break
                    continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        y = self.board.drop_height(self.curr_piece, self.x)
                        self.drop(y)
                        if self.board.top_filled():
                            running = False
                            break
                    if event.key == pygame.K_a:
                        if self.x - 1 >= 0:
                            occupied = False
                            for b in self.curr_piece.body:
                                if self.y + b[1] >= self.board.width:
                                    continue
                                if self.board.board[self.y + b[1]][self.x + b[0] - 1]:
                                    occupied = True
                                    break
                            if not occupied:
                                self.x -= 1
                    if event.key == pygame.K_d:
                        if self.x + 1 <= self.board.width - len(self.curr_piece.skirt):
                            occupied = False
                            for b in self.curr_piece.body:
                                if self.y + b[1] >= self.board.width:
                                    continue
                                if self.board.board[self.y + b[1]][self.x + b[0] + 1]:
                                    occupied = True
                                    break
                            if not occupied:
                                self.x += 1
                    if event.key == pygame.K_w:
                        self.curr_piece = self.curr_piece.get_next_rotation()
                if event.type == MOVEEVENT:
                    if self.board.drop_height(self.curr_piece, self.x) == self.y:
                        self.drop(self.y)
                        if self.board.top_filled():
                            running = False
                        break
                    self.y -= 1
            
            self.screen.fill(BLACK)
            self.draw_text_with_highlight("Score: " + str(self.rows_cleared*100 + self.pieces_dropped*20), (self.screenWidth), (self.screenHeight / 2 - 2))           
            self.draw_text_with_highlight("Time Remaining: " + str(timer_seconds), 320, 150)
            
            self.draw()
            pygame.display.flip()
            clock.tick(10)
            if timer_seconds == 0:
                running =False
            else:
                timer_seconds -= 1
        pygame.quit()
        sys.exit()
    def draw_text_with_highlight(self, text, x, y, fontSize=int(1.5 *28), highlight_color=(0, 0, 50)):
        gameFont = pygame.font.Font(font_file, fontSize)
        text_surface = gameFont.render(text, True, (255, 255, 255))  # White text
        rect = text_surface.get_rect()
        rect.topleft = (x, y)
        pygame.draw.rect(self.screen, highlight_color, rect)
        self.screen.blit(text_surface, rect.topleft)
    def drop(self, y, x=None):
        if x == None:
            x = self.x
        self.board.place(x, y, self.curr_piece)
        self.x = 5
        self.y = 20
        self.curr_piece = Piece()
        self.pieces_dropped += 1
        self.rows_cleared += self.board.clear_rows()

    def draw(self):
        self.draw_pieces()
        self.draw_hover()
        self.draw_grid()

    def draw_grid(self):
        for row in range(0, self.board.height):
            start = (0, row * self.pieceHeight + self.top)
            end = (self.screenWidth -100, row * self.pieceHeight + self.top)
            pygame.draw.line(self.screen, WHITE, start, end, width=2)
        for col in range(1, self.board.height):
            start = (col * self.pieceWidth-300, self.top)
            end = (col * self.pieceWidth-300, self.screenHeight)
            pygame.draw.line(self.screen, WHITE, start, end, width=2)
        # border
        tl = (0, 0)
        bl = (0, self.screenHeight - 2)
        br = (self.screenWidth - 100, self.screenHeight - 2)
        tr = (self.screenWidth - 100, 0)
        pygame.draw.line(self.screen, WHITE, tl, tr, width=2)
        pygame.draw.line(self.screen, WHITE, tr, br, width=2)
        pygame.draw.line(self.screen, WHITE, br, bl, width=2)
        pygame.draw.line(self.screen, WHITE, tl, bl, width=2)

    def draw_pieces(self):
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.board[row][col]:
                    tl = (
                        col * self.pieceWidth,
                        (self.board.height - row - 1) * self.pieceHeight,
                    )
                    color = self.board.colors[row][col]  # Retrieve color from the board's color matrix
                    image = self.image_dict[color]  # Retrieve image corresponding to the color
                    self.screen.blit(image, tl)
    def draw_hover(self):
        for b in self.curr_piece.body:
            tl = (
                (self.x + b[0]) * self.pieceWidth,
                (self.board.height - (self.y + b[1]) - 1) * self.pieceHeight,
            )
            color = self.curr_piece.color
            if color in self.image_dict:
                image = self.image_dict[color]
                # Blit the image onto the screen
                self.screen.blit(image, tl)
                #pygame.display.flip()
                
