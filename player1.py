import pygame
from gui import Draw, Tetromino, Board

class Player:





    def isGameOver(self):
        if any(self.grid[0]):
            return True
        else:
            return False
            
    def updateGame(self):
        completedRows = self.deleteCompletedRows()
        clearedRowCount = len(completedRows)
        self.updateScores(clearedRowCount)
        return clearedRowCount

    def deleteCompletedRows(self):
        completedRows = []
        for i, row in enumerate(self.grid):
            if all(row):
                completedRows.append(i)
        for rowIndex in completedRows:
            del self.grid[rowIndex]
            self.grid.insert(0,self.emptyRow)
        return completedRows

    def updateScores(self, clearedRowCount):
        self.linesCleared += clearedRowCount
        self.score += (self._lineScores[clearedRowCount -1 ]) #for now no levels introduced in tetris game

while True:
    clearedRowCount = board.updateGame()
    if gameOverCondition:  
        gameOver = True

    draw.refreshScreen(board, tetromino, tetrominonext)

    if gameOver:
        draw.drawGameOver(board)
        pygame.display.update()
