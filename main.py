import sys
import state
import copy

def backTrack(board):
    myStack=[]
    myStack.append(board)
    while len(myStack)>0:
        curBoard = myStack.pop()
        smallestDomain=curBoard.getSmallestDomain()
        for i, num in enumerate(smallestDomain.domain):
            newBoard=copy.deepcopy(curBoard)
            newSquare=newBoard.board[smallestDomain.row][smallestDomain.col]
            newSquare.domain=[str(num)]
            newSquare.chars=str(num)
            newBoard.solveList.append((newSquare.row, newSquare.col, newSquare.chars))
            works=newBoard.constraintSearch()
            if works==True:
                return newBoard
                break
            # if works==False:
            #     continue
            myStack.append(newBoard)
    curBoard.solveList = []
def main():
    #if len(sys.argv) != 2:
    #    print("Usage: python3 main.py <SUDOKU_FILE>")
    #    sys.exit(-1)
    f=open('board.txt', 'r')
    games=f.readlines()
    gameCount=0
    for game in games:
        count=0
        board=state.State()
        for row in range(0, 9):
            for col in range(0,9):
                c = game[count]
                count+=1
                if not c: break
                board.setupSquare(c,col,row)
        works = board.constraintSearch()
        g=open('solvelist.txt', 'w')
        if works == False or works==None:
            solvedBoard=backTrack(board)
            solvedBoard.printBoard()
            solveList = solvedBoard.solveList
            for x in solveList:
                g.write(str(x[0]) + " " + str(x[1]) + " " + str(x[2]) + "\n")
        else:
            solveList = board.solveList
            for x in solveList:
                g.write(str(x[0]) + " " + str(x[1]) + " " + str(x[2]) + "\n")
            board.printBoard()



if (__name__ == "__main__"):
    main()
