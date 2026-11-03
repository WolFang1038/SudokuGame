import copy

class board():
    def __init__(self):
        self.tiles = []
        for y in range(0,9):
            self.tiles.append([])
            for x in range(0,9):
                self.tiles[y].append(tile())
        self.previousBoards = []

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
                    self.tiles[tempy][tempx].legalNums.remove(newNum)


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



    def solve(self):

        ##FUNCTION DOESNT WORK. triedTiles need to check numbers tried as well as which tiles have been tried
        def makeNewMove() -> bool:
        ##Find tile(s) with least legalMoves
            triedTiles = {}
            while True:
            ##Save current boardPositionTemp
                
                tilex = 10
                tiley = 10
                leastLegalMoves = 10
                canContinue = False
                for y in range(0,9):
                    for x in range(0,9):
                        if leastLegalMoves > len(self.tiles[y][x].legalNums) and self.tiles[y][x].currentNum == ".":
                            if (tiley,tilex) in triedTiles:
                                if (leastLegalMoves > len(triedTiles[tiley,tilex])):
                                    leastLegalMoves = len(self.tiles[y][x].legalNums)
                                    tilex = x
                                    tiley = y
                                    canContinue = True
                            else:
                                leastLegalMoves = len(self.tiles[y][x].legalNums)
                                tilex = x
                                tiley = y
                                canContinue = True

                ##If no legal moves are possible
                if leastLegalMoves == 10:
                    ##backtrack/ checkwin
                    return False
                elif (canContinue):
                    
                    for num in self.tiles[tiley][tilex].legalNums:
                        ##make move, check if its been played before, if yes then undo, if no make new move
                        self.numberAdded(tiley,tilex,num)
                        if ((tiley,tilex) not in triedTiles):
                            triedTiles[tiley,tilex] = set()
                        triedTiles[tiley,tilex].add(num)
                        if self.tiles not in self.previousBoards:     ##New board iteration
                            self.previousBoards.append(copy.deepcopy(self.tiles))
                            return True
                        else:
                            self.numberRemoved(tiley,tilex)

        
        route = [copy.deepcopy(self.tiles)]   ##Create a stack starting with current tiles
        solving = True
        while solving:
            if (not makeNewMove()):
                if (self.checkWin()):
                    ##Won
                    pass 
                else:
                    ##pop board position
                    self.tiles = copy.deepcopy(route[-2])
                    route.pop(-1)
            else:
                route.append(copy.deepcopy(self.tiles))

            

        ##Every move push the new tiles to the stack
        ##Every deadend pop from stack
        ##Stack creates a route to the end for backtracking
    
    




class tile():
    def __init__(self):
        self.currentNum = "."
        self.legalNums = {"1","2","3","4","5","6","7","8","9"}