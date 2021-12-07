draws = []
class Board:
    def __init__(self):
        self.rows = []

    def RowComplete(self,rowIdx,draws):
        for x in self.rows[rowIdx]:
            if x not in draws:
                return False
        return True
    def ColComplete(self,colIdx,draws):
        for row in self.rows:
            if row[colIdx] not in draws:
                return False
        return True
    def DiagComplete(self,diagIdx,draws):
        if diagIdx == 0:
            for i in range(5):
                if self.rows[i][i] not in draws:
                    return False
            return True
        else:
            for i in range(5):
                if self.rows[i][4-i] not in draws:
                    return False
            return True
    def IsComplete(self,draws):
        for i in range(5):
            if self.RowComplete(i,draws):
                return True
            if self.ColComplete(i,draws):
                return True
        #for i in range(2):
        #    if self.DiagComplete(i,draws):
        #        print("Diag")
        #        return True
        return False
    def Score(self, draws, thisDraw):
        score = 0
        for row in range(5):
            for col in range(5):
                x = self.rows[row][col]
                if x not in draws:
                    score += x
        return score*thisDraw
boards = []
        
DRAWS = 0
BOARDS = 1
state = DRAWS
with open("input.txt") as FILE:
    lines = FILE.readlines()
    currentBoard = Board()
    for line in lines:
        if len(line.strip()) == 0:
            state = BOARDS
            currentBoard = Board()
            boards.append(currentBoard)
        elif state == DRAWS:
            draws = [int(x) for x in line.strip().split(',')]
        else:
            currentBoard.rows.append([int(x) for x in filter(None,line.strip().split(' '))])

#part a
print(len(boards))
drawsSoFar = set()
found = False
for x in draws:
    drawsSoFar.add(x)
    for board in boards:
        if board.IsComplete(drawsSoFar):
            print(x)
            print (board.Score(drawsSoFar,x))
            found = True
            break
    if found:
        break

#part b

drawsSoFar = set()
found = False
incompleteBoard = None
for x in draws:
    drawsSoFar.add(x)
    completeBoards = 0
    for board in boards:
        if board.IsComplete(drawsSoFar):
            completeBoards += 1
        else:
            incompleteBoard = board
    if completeBoards == len(boards):
        print("Part b")
        print(incompleteBoard.Score(drawsSoFar,x))
        break
