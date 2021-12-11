from copy import copy,deepcopy

input = []

with open("input.txt") as FILE:
    for line in FILE.readlines():
        row = []
        for c in line.strip():
            row.append(int(c))
        input.append(row)
        
def TryGetPoint(matrix,coord):
    y = coord[1]
    x = coord[0]
    if y < 0 or y >= len(matrix):
        return (False,0)
    row = input[y]
    if x < 0 or x >= len(row):
        return (False,0)
    return (True,matrix[y][x])
    
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)
cardinalDirections = (UP,DOWN,LEFT,RIGHT)

UPLEFT = (-1,-1)
UPRIGHT = (1,-1)
DOWNLEFT = (-1,1)
DOWNRIGHT = (1,1)
diagonalDirections = (UPLEFT,UPRIGHT,DOWNLEFT,DOWNRIGHT)
adjacentDirections = (UP,DOWN,LEFT,RIGHT,UPLEFT,UPRIGHT,DOWNLEFT,DOWNRIGHT)

def AddCoordinates2D(c1,c2):
    return (c1[0]+c2[0],c1[1]+c2[1])
    
def PrintMat(mat):
    for row in mat:
        rowString = ""
        for val in row:
            rowString += str(val)
        print(rowString)
    print("")
    
height = len(input)
width = len(input[0])

#part a+b
numFlashes = 0
state = input
step = 0
while True:
    step += 1
    newState = deepcopy(state)
    
    for y in range(height):
        for x in range(width):
            newState[y][x] = state[y][x]+1
    
    numNewFlashes = 0
    while True:
        newFlashes = False
        for y in range(height):
            for x in range(width):
                if newState[y][x]>9:
                    newFlashes = True
                    numNewFlashes += 1
                    numFlashes += 1
                    newState[y][x] = 0
                    for direction in adjacentDirections:
                        neighbor = AddCoordinates2D((x,y),direction)
                        pointExists, value = TryGetPoint(newState, neighbor)
                        if pointExists and value > 0: #0 is already burst
                            newState[neighbor[1]][neighbor[0]] = value+1
        if newFlashes is False:
            break
    
    state = newState
    if step == 100:
        print(numFlashes)
    if numNewFlashes == width*height:
        print(step)
        break