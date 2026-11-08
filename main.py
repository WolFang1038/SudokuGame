import copy



class tile():
    def __init__(self, num: str):
        self.currentNum = num
        self.legalNums = {"1","2","3","4","5","6","7","8","9"}


class board():
    def __init__(self,providedTiles: list[str]):
        ##Creating blank board
        self.tiles = []
        if len(providedTiles) == 0:
            for y in range(0,9):
                self.tiles.append([])
                for x in range(0,9):
                    self.tiles[y].append(tile("."))
        
        ##Loading premade board
        elif len(providedTiles) == 81:
            y = 0
            x = 0
            for num in providedTiles:
                if x == 0:
                    self.tiles.append([])
                self.tiles[y].append(tile(num))
                x += 1
                if x == 9:
                    y += 1
                    x = 0
            for y in range(0,9):
                for x in range(0,9):
                    self.tiles[y][x].legalNums = self.findLegalMoves(y,x)

        else:
            print("Incorrect board layout")

    def printBoard(self):
        for y in range(0,9):
            row = []
            for x in range(0,9):
                row.append(self.tiles[y][x].currentNum)
            print(row)


    ##How to add a number to a tile on the board
    def numberAdded(self, tiley: int, tilex: int, newNum: str):
        self.tiles[tiley][tilex].currentNum = newNum
        #Edit legal nums for row
        for tempx in range(tilex-1,-1,-1):
            if newNum in self.tiles[tiley][tempx].legalNums:
                self.tiles[tiley][tempx].legalNums.remove(newNum)
        
        for tempx in range(tilex+1,9):
            if newNum in self.tiles[tiley][tempx].legalNums:
                self.tiles[tiley][tempx].legalNums.remove(newNum)

        #Edit legal nums for column
        for tempy in range(tiley-1,-1,-1):
            if newNum in self.tiles[tempy][tilex].legalNums:
                self.tiles[tempy][tilex].legalNums.remove(newNum)
        
        for tempy in range(tiley+1,9):
            if newNum in self.tiles[tempy][tilex].legalNums:
                self.tiles[tempy][tilex].legalNums.remove(newNum)

        #Edit legal nums for subsquare
        subTopLeftx = (tilex//3)*3
        subTopLefty = (tiley//3)*3
        for tempy in range(0,3):
            for tempx in range(0,3):
                if newNum in self.tiles[subTopLefty+tempy][subTopLeftx+tempx].legalNums:
                    self.tiles[subTopLefty+tempy][subTopLeftx+tempx].legalNums.remove(newNum)


    ##Finds all legal moves for the given tile
    def findLegalMoves(self,tiley: int,tilex: int) -> set[str]:
        newLegalNums = set()
        for tempx in range(tilex-1,-1,-1):
            newLegalNums.add(self.tiles[tiley][tempx].currentNum)
        for tempx in range(tilex+1,9):
            newLegalNums.add(self.tiles[tiley][tempx].currentNum)
        for tempy in range(tiley-1,-1,-1):
            newLegalNums.add(self.tiles[tempy][tilex].currentNum)
        for tempy in range(tiley+1,9):
            newLegalNums.add(self.tiles[tempy][tilex].currentNum)
        subTopLeftx = (tilex//3)*3
        subTopLefty = (tiley//3)*3
        for tempy in range(0,3):
            for tempx in range(0,3):
                newLegalNums.add(self.tiles[subTopLefty+tempy][subTopLeftx+tempx].currentNum)
        newLegalNums.add(".")
        legalNums = {"1","2","3","4","5","6","7","8","9","."}
        for num in newLegalNums:
            legalNums.remove(num)
        return legalNums

    ##Checks if given tile can legally hold given number
    def checkSpecificLegalMove(self, tiley: int, tilex: int, num: str) -> bool:
        canHold = True
        ##Checking Horizontals
        for tempx in range(tilex-1,-1,-1):
            if self.tiles[tiley][tempx].currentNum == num:
                canHold = False
        for tempx in range(tilex+1,9):
                    if self.tiles[tiley][tempx].currentNum == num:
                        canHold = False
        ##Checking verticals
        if canHold:
            for tempy in range(tiley-1,-1,-1):
                if self.tiles[tempy][tilex].currentNum == num:
                    canHold = False
            for tempy in range(tiley+1,9):
                if self.tiles[tempy][tilex].currentNum == num:
                    canHold = False
            ##Checking subsquare
            if canHold:
                subTopLeftx = (tilex//3)*3
                subTopLefty = (tiley//3)*3
                for tempy in range(0,3):
                    for tempx in range(0,3):
                        if self.tiles[subTopLefty+tempy][subTopLeftx+tempx].currentNum == num:
                            canHold = False
        return canHold


    ##How to remove a number from a tile on the board
    def numberRemoved(self, tiley: int, tilex: int):
        numRemoved = self.tiles[tiley][tilex].currentNum
        self.tiles[tiley][tilex].currentNum = "."
        self.tiles[tiley][tilex].legalNums = self.findLegalMoves(tiley,tilex)
        #Edit legal nums for row, column, subsquare. 
        #Iterate every connected tile to tilex,tiley
        #Check if the now removed number can be placed on any connecting tile legally
        for tempx in range(tilex-1,-1,-1):
            if self.checkSpecificLegalMove(tiley,tempx, numRemoved):
                self.tiles[tiley][tempx].legalNums.add(numRemoved)
        for tempx in range(tilex+1,9):
            if self.checkSpecificLegalMove(tiley,tempx, numRemoved):
                self.tiles[tiley][tempx].legalNums.add(numRemoved)
        
        for tempy in range(tiley-1,-1,-1):
            if self.checkSpecificLegalMove(tempy,tilex, numRemoved):
                self.tiles[tempy][tilex].legalNums.add(numRemoved)
        for tempy in range(tiley+1,9):
            if self.checkSpecificLegalMove(tempy,tilex, numRemoved):
                self.tiles[tempy][tilex].legalNums.add(numRemoved)
        
        subTopLeftx = (tilex//3)*3
        subTopLefty = (tiley//3)*3
        for tempy in range(0,3):
            for tempx in range(0,3):
                if self.checkSpecificLegalMove(subTopLefty+tempy,subTopLeftx+tempx, numRemoved):
                    self.tiles[subTopLefty+tempy][subTopLeftx+tempx].legalNums.add(numRemoved)

    ##Checks if the board is solved
    def checkWin(self) -> bool:

        ##Checks every row for duplicates
        for row in self.tiles:
            currentRowNums = set()
            for tile in row:
                currentRowNums.add(tile.currentNum)
                if tile.currentNum == ".":      ##Makes sure there is no blank tiles
                    return False
            if len(currentRowNums) != 9:
                return False

        ##Checks every column for duplicates
        for x in range(0,9):
            currentColumnNums = set()
            for y in range(0,9):
                currentColumnNums.add(self.tiles[y][x].currentNum)
            if len(currentColumnNums) != 9:
                return False

        ##Check every 3x3 for duplicates
        for tempy in range(0,9,3):
            for tempx in range(0,9,3):
                subSquare = set()
                for y in range(0,3):
                    for x in range(0,3):
                        subSquare.add(self.tiles[tempy+y][tempx+x].currentNum)
                if len(subSquare) != 9:
                    return False
        ##If every, row, column, and subSquare are legal and all tiles are occupied then the board is solved.
        return True

            
    def solve(self, solvedBoards: list) -> list:     ##Finds all legal boards
        ##Looks at the board and returns tile with least possible legal moves
        ##If no tiles are free returns empty tuple
        def findNextTile() -> tuple:
            leastLegalMoves = 10
            nextTile = set()
            for y in range(0,9):
                for x in range(0,9):
                    if leastLegalMoves > len(self.tiles[y][x].legalNums) and self.tiles[y][x].currentNum == ".":
                        leastLegalMoves = len(self.tiles[y][x].legalNums)
                        nextTile = (y,x)
            
            return nextTile                    
                            

        ##Try tile with fewest legalmoves, try all legal numbers, if fail then try with the the with next fewest legal moves
        nextTile = findNextTile()
        if len(nextTile) == 0:
            if self.checkWin():
                solvedBoards.append(copy.deepcopy(self))
            return solvedBoards
        elif len(self.tiles[nextTile[0]][nextTile[1]].legalNums) == 0:
            return solvedBoards

        ##Add new number to the tempboard
        for num in self.tiles[nextTile[0]][nextTile[1]].legalNums:
            tempBoard = copy.deepcopy(self)
            tempBoard.numberAdded(nextTile[0],nextTile[1],num)
        
            ##Finds if tempBoard is full
            full = True
            for row in tempBoard.tiles:
                for tile in row:
                    if tile.currentNum == ".":
                        full = False
            if full:
                ##If solved, return to start of recursion
                if tempBoard.checkWin():
                    solvedBoards.append(copy.deepcopy(tempBoard))

            else:
                tempBoard.solve(solvedBoards)

        ##Final return of all found solved board positions
        return solvedBoards



##----------------------
## Main Program
## Test if board functions as intended.
gameBoard = board([
    ".",".",".",".",".",".",".",".",".",
    ".",".",".",".",".",".",".",".",".",
    "1","9","8","3","4","2","5","6","7",
    "8","5","9","7","6","1","4","2","3",
    "4","2","6","8","5","3","7","9","1",
    "7","1","3","9","2","4","8","5","6",
    "9","6","1","5","3","7","2","8","4",
    "2","8","7","4","1","9","6","3","5",
    "3","4","5","2","8","6","1","7","9"
])
gameBoard.printBoard()
solvedBoards = gameBoard.solve([])
for finishedBoard in solvedBoards:
    print()
    finishedBoard.printBoard()
    
print("Found: ",len(solvedBoards), " finished boards")

