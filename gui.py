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
        self.score = 0
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
