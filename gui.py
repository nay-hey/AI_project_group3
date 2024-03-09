import copy, random #for generating blocks
import sys #needed to quit the pygame
import pygame

pygame.init()#initialising pygame

display_h = pygame.display.Info().current_h #system's height
blockSize = display_h // 30 #1/30 of that height is a block, so that a 20 by 10 blocks tetris grid is visible in 2/3 rd by 1/3rd of the dispay screen
height = 20* blockSize
width=height+10
screen = pygame.display.set_mode((width, height))#initializes the game screen with given dimensions
pygame.display.set_caption("Tetris_group3")#sets the title of the screen

clock = pygame.time.Clock()#we need this to time the game and control frame rate (how fast the game progresses)

timer_seconds=10 #the game is timed using this variable as a counter and  gets over after these many seconds

class Board :#defining functions for the tetris game's grid

    def __init__(self, colour = "White"):
        self.colour = colour
        self.width = 10
        self.height = 20
        self.linesCleared = 0 #to keep track of score
        self.emptyGrid() #creating a 2D list to represent the grid.
        self.pieceList = [] #creating an array containing the tetromino pieces. Each tetromino is specified by the coordinates of its color.
        self.heldPiece=self.generatePiece() #the next piece that will come into play
        
    def emptyGrid(self):
        self.grid = []#creating a 2D list to represent the grid. 
        self.emptyRow = []
        for x in range(self.width):
            self.emptyRow.append(0)
        for rowCount in range(self.height):
            self.grid.append(copy.copy(self.emptyRow))#creates a shallow copy which reflects changes  made in self.emptyRow to 
            #self.emptyGrid instantaneously.


    def centrePiece(self, tetromino):#this moves the given tetromino form its default position at top left corner, to middle of top row which is where the pieces shouuld appear from initially.
        tetromino.centre[0] += (self.width/2) - 2 #tetromino.centre[0] is the x coordinate of the centre of tetromino and it is shifted to the middle of the grid
        for coord in tetromino.vertexCoords:#iterating over the list of all vertex coordinates
            coord[0] += (self.width/2) - 2 #similarly for x coordinate of each vertex it is shifted by as much as the centre is shifted to maintain shape of block
        for coord in tetromino.blockCoords:#done for the block coordinates
            coord[0] += (self.width/2) - 2 
        
    def generatePiece(self):
        if (len(self.pieceList) == 0):
            self.pieceList = list(Tetromino.Shapes.keys())
            random.shuffle(self.pieceList)
        tetromino = Tetromino(self.pieceList.pop())
        self.centrePiece(tetromino)
        return (tetromino)
        
    
class Draw:

    def __init__(self):
        self.boardWidth = 10 
        self.boardOffset = 2
        self.boardOutline = (blockSize // 15) if (blockSize >= 15) else 1#to see individual cells in board
        self.pieceOutline = (blockSize // 15) if (blockSize >= 15) else 1#to see tetromino piece in board
        self.boardRect = pygame.Rect(self.boardOffset*blockSize, 0, (self.boardWidth*blockSize
                                                                     ) + self.boardOutline, height)
        #pygame.Rect(x,y,w,h) creates a rectangle of width w and height h at position x,y 
        self.fontColour = (255, 0, 125) #font colour
        self.heldWidth = 4
        self.heldXOffset = self.boardWidth + (self.boardOffset*2)
        self.heldYOffset = 1.25
        self.heldRect = pygame.Rect(self.heldXOffset*blockSize, self.heldYOffset*blockSize, self.heldWidth*blockSize, self.heldWidth*blockSize)
        

    def drawBoard(self, board):
        pygame.draw.rect(screen, board.colour, self.heldRect, self.boardOutline)
        pygame.draw.rect(screen, board.colour, self.boardRect)        #pygame.draw.rect(surface, color of rect, pygame.rect) draws the rect of specified color
        for x in range(self.boardOffset, (self.boardWidth + self.boardOffset)):#coordinates along width of grid
            for y in range(0, height):#coordinates along height of grid
                cell = pygame.Rect(x*blockSize + self.boardOutline,
                                   y*blockSize + self.boardOutline,
                                   blockSize - self.boardOutline, blockSize - self.boardOutline)
                #adds margins to x and y coordinates and subtract margins from width and height coordinates to accomodate borders of each individual cell 
                pygame.draw.rect(screen, "Black", cell)#draws each of the cells in the board grid

    def getScaledCoords(self, vertexCoords):
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + 2)*blockSize
            coord[1] = coord[1]*blockSize
        return copyCoords

    def getScaledCoords1(self, vertexCoords):
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + 11)*blockSize
            coord[1] = (coord[1]+2)*blockSize
        return copyCoords
    def drawTetromino1(self, tetromino):
        pygame.draw.polygon(screen, tetromino.colour, self.getScaledCoords1(tetromino.vertexCoords))
    def drawTetromino(self, tetromino):
        pygame.draw.polygon(screen, tetromino.colour, self.getScaledCoords(tetromino.vertexCoords))
        pygame.draw.polygon(screen, "Black", self.getScaledCoords(tetromino.vertexCoords), self.pieceOutline)

    
    def drawStats(self, board):
        fontSize = int(blockSize)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize)
        nextText = gameFont.render("Next piece", True, self.fontColour)
        time = gameFont.render(str(timer_seconds), True, self.fontColour)
        timeText = gameFont.render("Time remaining", True, self.fontColour)
        lineNum = gameFont.render(str(board.linesCleared), True, self.fontColour)
        lineText = gameFont.render("Lines cleared", True, self.fontColour)
        nextYPos = int(board.height*0.33)
        timeYPos = nextYPos + 3
        lineYPos = timeYPos + 3
        screen.blit(nextText, ((self.boardOffset+12)*blockSize, (nextYPos)*blockSize))
        screen.blit(time, ((self.boardOffset+12)*blockSize, (timeYPos+1)*blockSize))
        screen.blit(timeText, ((self.boardOffset+12)*blockSize, (timeYPos)*blockSize))
        screen.blit(lineText, ((self.boardOffset+12)*blockSize, lineYPos*blockSize))
        screen.blit(lineNum, ((self.boardOffset+12)*blockSize, (lineYPos+1)*blockSize))
        
    def drawGameOver(self, board):
        fontSize = int(2 * blockSize)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize)
        gameOverText = gameFont.render("GAME OVER", True, self.fontColour)
        screen.blit(gameOverText, (blockSize, ((board.height/2)-1)*blockSize))

    def drawStartScreen(self, board):
        fontSize = int(2 * blockSize)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize)
        pressText = gameFont.render("PRESS", True, self.fontColour)
        aText = gameFont.render("A FOR", True, self.fontColour)
        aiText = gameFont.render(" AI", True, self.fontColour)
        hText = gameFont.render("H FOR", True, self.fontColour)
        humanText = gameFont.render("HUMAN", True, self.fontColour)
        screen.blit(pressText, (2*blockSize, ((board.height/2)-3)*blockSize))
        screen.blit(aText, (2*blockSize, ((board.height/2)-1)*blockSize))
        screen.blit(aiText, (3*blockSize, ((board.height/2)+1)*blockSize))
        screen.blit(pressText, (12*blockSize, ((board.height/2)-3)*blockSize))
        screen.blit(hText, (12*blockSize, ((board.height/2)-1)*blockSize))
        screen.blit(humanText, (12*blockSize, ((board.height/2)+1)*blockSize))
        pygame.draw.line(screen, self.fontColour, (10*blockSize, blockSize), (10*blockSize, 20*blockSize), self.boardOutline*2)

    def drawPauseScreen(self):
        fontSize = int(2 * blockSize)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize)
        pauseText = gameFont.render("PAUSED", True, self.fontColour)
        screen.blit(pauseText, (5.5*blockSize, (blockSize)))
        fontSize = int(blockSize)
        gameFont = pygame.font.SysFont(pygame.font.get_fonts()[0],size=fontSize)
        newText = gameFont.render("N:             New Game", True, self.fontColour)
        escText = gameFont.render("P:           Unpause", True, self.fontColour)
        leftText = gameFont.render("Left Arrow:    Move Left", True, self.fontColour)
        rightText = gameFont.render("Right Arrow:   Move Right", True, self.fontColour)
        upText = gameFont.render("Up Arrow:      Rotate", True, self.fontColour)
        enterText = gameFont.render("Space:         Hard Drop", True, self.fontColour)
        screen.blit(newText, (blockSize, (5*blockSize)))
        screen.blit(escText, (blockSize, (6*blockSize)))
        screen.blit(leftText, (blockSize, (7*blockSize)))
        screen.blit(rightText, (blockSize, (8*blockSize)))
        screen.blit(upText, (blockSize, (9*blockSize)))
        screen.blit(enterText, (blockSize, (10*blockSize)))

    def refreshScreen(self, board, tetromino,tetrominonext):
        screen.fill("Grey")#background around the grid
        self.drawBoard(board)#creating the grid
        self.drawTetromino(tetromino)
        self.drawStats(board)
        self.drawTetromino1(tetrominonext)#draw next tetromino piece
        pygame.display.update()

class Tetromino():
    Colours = {
        "red" : (255,0,0),
        "orange" : (255,163,47),
        "yellow" : (255,236,33),
        "green" : (147,240,59),
        "blue" : (55,138,255),
        "pink" : (255,119,253),
        "purple" : (149,82,234)
    }

    Shapes = {
        #Every shape is 3 element list where the first element is list of vertices, 
        #2nd is a list of top left corner coord of constituent blocks and
        #3rd is the centre of rotation 
        "O" : [ [[0,0],[2,0],[2,2],[0,2]], [[0,0],[1,0],[0,1],[1,1]], [1,1] ],
        "I" : [ [[0,0],[4,0],[4,1],[0,1]], [[0,0],[1,0],[2,0],[3,0]], [2,1] ], 
        "S" : [ [[1,0],[3,0],[3,1],[2,1],[2,2],[0,2],[0,1],[1,1]], [[1,0],[2,0],[0,1],[1,1]], [1.5,1.5] ],
        "Z" : [ [[0,0],[2,0],[2,1],[3,1],[3,2],[1,2],[1,1],[0,1]], [[0,0],[1,0],[1,1],[2,1]], [1.5,1.5] ],
        "J" : [ [[0,0],[3,0],[3,2],[2,2],[2,1],[0,1]], [[0,0],[1,0],[2,0],[2,1]], [1.5,0.5] ],
        "L" : [ [[0,0],[3,0],[3,1],[1,1],[1,2],[0,2]], [[0,0],[1,0],[2,0],[0,1]], [1.5,0.5] ],
        "T" : [ [[0,0],[3,0],[3,1],[2,1],[2,2],[1,2],[1,1],[0,1]], [[0,0],[1,0],[2,0],[1,1]], [1.5,0.5] ]
    }

    def __init__(self, shape = None, rotations = 0):
        self.rotations = 0
        self.xOffset = 0
        self.yOffset = 0
        if self.Shapes.get(shape) is not None:
            self.shape = shape
        else:
            self.shape = random.choice(list(self.Shapes.keys()))
        self.vertexCoords = copy.deepcopy(self.Shapes[self.shape][0])
        self.blockCoords = copy.deepcopy(self.Shapes[self.shape][1])
        self.centre = copy.copy(self.Shapes[self.shape][2])        
        self.colour = random.choice(list(self.Colours.values()))
        
newGame = True
gameOver = False
paused = False
draw = Draw()

while True:
                
    screen.fill("Black")#Clears screen by filling the screen with black color

    #reset game and timer
    if newGame:
        board = Board()
        tetromino = board.generatePiece()
        tetrominonext=board.generatePiece()
        draw.drawStartScreen(board)
        timer_seconds=10
        

    #newGame screen loop
        while newGame:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    newGame = False
                    pygame.quit()
                    sys.exit()
                keyInput = pygame.key.get_pressed()
                if keyInput[pygame.K_h]:
                    newGame = False
                if keyInput[pygame.K_a]:
                    newGame = False

    #Pause screen loop
    while paused:
        draw.drawPauseScreen()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False
                pygame.quit()
                sys.exit()
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_p]:
                paused = False
            if keyInput[pygame.K_n]:
                newGame = True
                paused = False
 
    gameFlags = [newGame, gameOver, paused]

    #gamePlay Loop
    counter=0
    while (not any(gameFlags)):
        clock.tick(60)#tick(n) means the while loop and all code in it will run n times per second
        #Draw game elements to screen
        draw.refreshScreen(board, tetromino,tetrominonext)

        
        counter+=1
        if counter%60==0:
            timer_seconds -= 1
        if timer_seconds == 0:
            gameOver=True
            timer_seconds=10
        
        #Check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_p]:
                paused = True
            if keyInput[pygame.K_n]:
                newGame = True

        gameFlags = [newGame, gameOver, paused]

    #Game over screen loop
    while gameOver:
        draw.drawGameOver(board)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                gameOver = False
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_n] or keyInput[pygame.K_p]:
                newGame = True
                gameOver = False
