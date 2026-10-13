class board():
    def __init__(self):
        self.tiles = []
        for y in range(0,9):
            self.tiles.append([])
            for x in range(0,9):
                self.tiles[y].append(tile())

    ##How to add a number to a tile on the board
    def numberAdded(self, tilex: int, tiley: int, newNum: str):
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
    def findLegalMoves(self,tilex: int,tiley: int) -> set[str]:
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
    def checkSpecificLegalMove(self, tilex: int, tiley: int, num: str) -> bool:
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
    def numberRemoved(self, tilex: int, tiley: int):
        numRemoved = self.tiles[tiley][tilex].currentNum
        self.tiles[tiley][tilex].currentNum = "."
        self.tiles[tiley][tilex].legalNums = self.findLegalMoves(tilex,tiley)
        #Edit legal nums for row, column, subsquare. 
        #Iterate every connected tile to tilex,tiley
        #Check if the now removed number can be placed on any connecting tile legally
        for tempx in range(tilex-1,-1,-1):
            if self.checkSpecificLegalMove(tempx,tiley, numRemoved):
                self.tiles[tiley][tempx].legalNums.add(numRemoved)
        for tempx in range(tilex+1,9):
            if self.checkSpecificLegalMove(tempx,tiley, numRemoved):
                self.tiles[tiley][tempx].legalNums.add(numRemoved)
        
        for tempy in range(tiley-1,-1,-1):
            if self.checkSpecificLegalMove(tilex,tempy, numRemoved):
                self.tiles[tempy][tilex].legalNums.add(numRemoved)
        for tempy in range(tiley+1,9):
            if self.checkSpecificLegalMove(tilex,tempy, numRemoved):
                self.tiles[tempy][tilex].legalNums.add(numRemoved)
        
        subTopLeftx = (tilex//3)*3
        subTopLefty = (tiley//3)*3
        for tempy in range(0,3):
            for tempx in range(0,3):
                if self.checkSpecificLegalMove(subTopLeftx+tempx,subTopLefty+tempy, numRemoved):
                    self.tiles[subTopLefty+tempy][subTopLeftx+tempx].legalNums.add(numRemoved)
    
    




class tile():
    def __init__(self):
        self.currentNum = "."
        self.legalNums = {"1","2","3","4","5","6","7","8","9"}