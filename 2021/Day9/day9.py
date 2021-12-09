input = []
basins = [] #part b

with open("input.txt") as FILE:
    for line in FILE.readlines():
        row = []
        basinRow = []
        for c in line.strip():
            row.append(int(c))
            basinRow.append(None) #part b
        input.append(row)
        basins.append(basinRow) #part b
        
#part a
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

def AddCoordinates2D(c1,c2):
    return (c1[0]+c2[0],c1[1]+c2[1])
    
partACount = 0
for y in range(len(input)):
    for x in range(len(input[y])):
        val = input[y][x]
        isLowPoint = True
        for direction in cardinalDirections:
            newPos = AddCoordinates2D((x,y),direction)
            hasValue, adjacentVal = TryGetPoint(input,newPos)
            if hasValue and adjacentVal <= val:
                isLowPoint = False
                break
        if isLowPoint:
            partACount += val+1
            basins[y][x] = (x,y) #part b
print(partACount)

#part b
foundNewBasins = True
while foundNewBasins:
    foundNewBasins = False
    for y in range(len(input)):
        for x in range(len(input[y])):
            val = input[y][x]
            nearestBasin = basins[y][x]
            if nearestBasin is not None:
                continue
            if val == 9:
                continue
            for direction in cardinalDirections:
                newPos = AddCoordinates2D((x,y),direction)
                pointExists, adjacentBasin = TryGetPoint(basins,newPos)
                if pointExists and adjacentBasin is not None:
                    basins[y][x] = adjacentBasin
                    foundNewBasins = True
                    break

basinCounts = {}
for y in range(len(basins)):
    for x in range(len(basins[y])):
        basin = basins[y][x]
        if basin is not None:
            if basin in basinCounts:
                basinCounts[basin] = basinCounts[basin]+1
            else:
                basinCounts[basin] = 1
sortedBasinCoordinates = sorted(basinCounts,key=basinCounts.get,reverse=True)
print(basinCounts[sortedBasinCoordinates[0]]*basinCounts[sortedBasinCoordinates[1]]*basinCounts[sortedBasinCoordinates[2]])