EAST = 0
SOUTHEAST = 1
SOUTHWEST = 2
WEST = 3
NORTHWEST = 4
NORTHEAST = 5
NUM_DIRECTIONS = 6

#Tile X == normal x
#Tile Y = zigzagging vertically
#origin is in the right zigzag column
# \ \
# / /
# \ \   v +y  ->+x
# / /

def GetTileInDirection(pos, direction):
    if direction == EAST:
        return (pos[0]+1,pos[1])
    elif direction == WEST:
        return (pos[0]-1,pos[1])
        
    inRightCol = pos[1]%2==0
    if inRightCol:
        if direction == SOUTHEAST:
            return (pos[0]+1,pos[1]+1)
        elif direction == SOUTHWEST:
            return (pos[0],pos[1]+1)
        elif direction == NORTHWEST:
            return (pos[0],pos[1]-1)
        elif direction == NORTHEAST:
            return (pos[0]+1,pos[1]-1)
    else:
        if direction == SOUTHEAST:
            return (pos[0],pos[1]+1)
        elif direction == SOUTHWEST:
            return (pos[0]-1,pos[1]+1)
        elif direction == NORTHWEST:
            return (pos[0]-1,pos[1]-1)
        elif direction == NORTHEAST:
            return (pos[0],pos[1]-1)
            
def GetNumAdjacent(flippedTiles, pos):
    count = 0
    for direction in range(NUM_DIRECTIONS):
        testTile = GetTileInDirection(pos, direction)
        if testTile in flippedTiles:
            count += 1
    return count
            
            
input = []
with open("input.txt") as FILE:
    INPUTSTATE_NORMAL = 0
    INPUTSTATE_PENDING_NORTH = 1
    INPUTSTATE_PENDING_SOUTH = 2
    
    for line in FILE:
        line = line.strip()
        if len(line) == 0:
            continue
        directions = []
        
        inputState = INPUTSTATE_NORMAL
        for c in line:
            if inputState == INPUTSTATE_NORMAL:
                if c == 'e':
                    directions.append(EAST)
                elif c == 'w':
                    directions.append(WEST)
                elif c == 'n':
                    inputState = INPUTSTATE_PENDING_NORTH
                elif c == 's':
                    inputState = INPUTSTATE_PENDING_SOUTH
            elif inputState == INPUTSTATE_PENDING_NORTH:
                if c == 'e':
                    directions.append(NORTHEAST)
                elif c == 'w':
                    directions.append(NORTHWEST)
                inputState = INPUTSTATE_NORMAL
            elif inputState == INPUTSTATE_PENDING_SOUTH:
                if c == 'e':
                    directions.append(SOUTHEAST)
                elif c == 'w':
                    directions.append(SOUTHWEST)
                inputState = INPUTSTATE_NORMAL
        input.append(directions)
        
#Part A
flippedTiles = set()
for directions in input:
    currentTile = (0,0)
    for direction in directions:
        currentTile = GetTileInDirection(currentTile, direction)
    if currentTile in flippedTiles:
        flippedTiles.remove(currentTile)
    else:
        flippedTiles.add(currentTile)
print(len(flippedTiles))

#Part B
for i in range(100):
    newFlippedTiles = set(flippedTiles)
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    for tile in flippedTiles:
        if tile[0] < minX:
            minX = tile[0]
        if tile[0] > maxX:
            maxX = tile[0]
        if tile[1] < minY:
            minY = tile[1]
        if tile[1] > maxY:
            maxY = tile[1]
    
    for y in range(minY-1,maxY+2):
        for x in range(minX-1,maxX+2):
            testTile = (x,y)
            isFlipped = testTile in flippedTiles
            numAdjacent = GetNumAdjacent(flippedTiles, testTile)
            if isFlipped and (numAdjacent == 0 or numAdjacent > 2):
                newFlippedTiles.remove(testTile)
            elif (not isFlipped) and (numAdjacent == 2):
                newFlippedTiles.add(testTile)
    
    flippedTiles = newFlippedTiles
print(len(flippedTiles))
