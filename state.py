import square

class State(object):
     def __init__(self):
        w, h = 9, 9;
        self.board = [[square.Square() for x in range(w)] for y in range(h)]
        self.parent=None
        self.children=[]
        self.myStack=[]
        self.smallestDomain=None
        self.solveList = []
     def parent(self):
        return self.parent
     def setupSquare(self, chars, col, row):
         neighbors=[]
         mySquare = self.board[row][col]
         mySquare.row=row
         mySquare.col=col
         mySquare.chars = str(chars)
         if mySquare.chars!=".":
            mySquare.setDomain()
         #figure out where it's neighbors are
         colStart = 0
         colEnd = 0
         rowStart = 0
         rowEnd = 0
         if col == 0 or col == 3 or col == 6:
             colStart = col
             colEnd = col+2
         elif col == 1 or col == 4 or col == 7:
             colStart = col-1
             colEnd = col+1
         elif col == 2 or col == 5 or col == 8:
             colStart = col-2
             colEnd = col
         if row == 0 or row == 3 or row == 6:
             rowStart = row
             rowEnd = row+2
         elif row == 1 or row == 4 or row == 7:
             rowStart = row-1
             rowEnd = row+1
         elif row == 2 or row == 5 or row == 8:
             rowStart = row-2
             rowEnd = row
        #Adds neighbors
         for x in range (0,9): #adds all squares in row
             newNeighbor=self.board[row][x]
             if newNeighbor not in neighbors and newNeighbor!=mySquare:
                 neighbors.append(newNeighbor)
                 mySquare.addNeighbor(newNeighbor)
         for x in range (0,9): #adds all squares in column
            newNeighbor=self.board[x][col]
            if newNeighbor not in neighbors and newNeighbor!=mySquare:
                neighbors.append(newNeighbor)
                mySquare.addNeighbor(newNeighbor)
         for x in range (rowStart, rowEnd+1): #adds all squares in box area
             for y in range(colStart,colEnd+1):
                 newNeighbor=self.board[x][y]
                 if newNeighbor not in neighbors and newNeighbor!=mySquare:
                     neighbors.append(newNeighbor)
                     mySquare.addNeighbor(newNeighbor)
     def constraintSearch(self):
        complete=True
        #add all unknown squares to the stack
        for row in range(0, 9):
            for col in range(0,9):
                mySquare=self.board[row][col]
                if mySquare.chars==".":
                    self.myStack.append(mySquare)
        while len(self.myStack)>0:
            curSquare = self.myStack.pop(0) #get next square in the queue
            changed=curSquare.compareNeighbors()
            if len(curSquare.domain)==0: # check if board is unsolvable
                return False
            if changed==True:
                if len(curSquare.domain)==1 and curSquare.chars !='.':
                    self.solveList.append((curSquare.row, curSquare.col, curSquare.chars))
                neighbors=curSquare.getNeighbors()
                for i, neighbor in enumerate(neighbors):
                    self.myStack.append(neighbor)
            # if curSquare.chars == ".":
            #     if self.smallestDomain==None:
            #         self.smallestDomain=curSquare
            #     else:
            #         len(curSquare.domain)<len(self.smallestDomain.domain)
            #         self.smallestDomain=curSquare
            # if len(self.myStack)==0:
            #     if curSquare.chars==".":
            #         complete=False
        if complete==True:
            for row in range(0, 9):
                for col in range(0,9):
                    mySquare=self.board[row][col]
                    if mySquare.chars==".":
                        complete=False
                        if self.smallestDomain==None:
                           self.smallestDomain=curSquare
                        else:
                            if (len(self.smallestDomain.domain)==2):
                                break
                            elif len(curSquare.domain)<len(self.smallestDomain.domain):
                                self.smallestDomain=curSquare
        if complete==True:
            return complete

     def getSmallestDomain(self):
        return self.smallestDomain

     def getSolveList(self):
        return self.solveList

     def printBoard(self):
        string = ""
        for row in range(0, 9):
            for col in range(0,9):
                string+=self.board[row][col].chars
        string+="\n"
        print(string)
