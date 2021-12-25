import copy
EMPTY = '.'
EAST = '>'
SOUTH = 'v'

input = []
with open("input.txt") as FILE:
    for line in FILE.readlines():
        line = line.strip()
        input.append([x for x in line])

def GetCoordsInDirection(grid,pos,direction):
    height = len(grid)
    width = len(grid[0])
    if direction == EAST:
        return ((pos[0]+1)%width,pos[1])
    if direction == SOUTH:
        return (pos[0],(pos[1]+1)%height)
        
def PrintState(state):
    print('')
    for row in state:
        rowStr = ""
        for val in row:
            rowStr += val
        print(rowStr)
        
def Step(state):
    changed = False
    height = len(state)
    width = len(state[0])
    
    newState = copy.deepcopy(state)
    for cukeType in (EAST,SOUTH):
        for y in range(height):
            for x in range(width):
                val = state[y][x]
                if val == cukeType:
                    newX,newY = GetCoordsInDirection(state,(x,y),cukeType)
                    if state[newY][newX] == EMPTY:
                        newState[newY][newX] = cukeType
                        newState[y][x] = EMPTY
                        changed = True
        state = copy.deepcopy(newState)
    
    return changed,state
                    
count = 0
state = copy.deepcopy(input)
while True:
    count += 1
    changed,state = Step(state)
    if not changed:
        print(count)
        break