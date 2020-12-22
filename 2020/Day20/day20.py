EDGE_WIDTH = 10

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
NUM_DIRECTIONS = 4

def CountTrue(rows):
    count = 0
    for row in rows:
        for x in row:
            if x:
                count += 1
    return count

def FlipAndRotateCoordinate(pos,size,flip,turns):
    newX = pos[0]+1
    newY = pos[1]+1
    
    while turns < 0:
        turns += NUM_DIRECTIONS
    
    if flip:
        newX = -newX
        
    for i in range(turns):
        rotX = -newY
        rotY = newX
        newX = rotX
        newY = rotY
        
    if newX < 0:
        newX += size+1
    if newY < 0:
        newY += size+1
    
    return (newX-1, newY-1)

def FlipAndRotate(rows, flip, turns):
    #assuming square
    size = len(rows)
    
    newMat = []
    for row in range(size):
        row = []
        for col in range(size):
            row.append(0)
        newMat.append(row)
    
    for y in range(size):
        for x in range(size):
            pos = (x,y)
            newPos = FlipAndRotateCoordinate(pos, size, flip, turns)
            newMat[newPos[1]][newPos[0]] = rows[y][x]
            
    return newMat
    
def PrintMatrix(rows):
    for row in rows:
        s = ""
        for c in row:
            s += str(c)
        print(s)
        
def PrintPuzzle(rows, serpentTiles):
    count = 0
    for y in range(len(rows)):
        row = rows[y]
        s = ""
        for x in range(len(row)):
            c = row[x]
            if ((x,y) in serpentTiles):
                s += "O"
                if c != True:
                    print("ERROR")
            elif c == True:
                s += "#"
                count += 1
            else:
                s += "."
        print(s)
    print(count)
            

def DirectionToUnitVector(direction):
    if direction == UP:
        return (0,-1)
    elif direction == RIGHT:
        return (1,0)
    if direction == DOWN:
        return (0,1)
    elif direction == LEFT:
        return (-1,0)
        
def RotateNQuarters(direction, n):
    direction += n
    while direction < 0:
        direction += 4
    direction %= 4
    return direction
        

def FlipEdgeId(id):
     # convert number into binary representation  
     # output will be like bin(10) = '0b10101'  
     binary = bin(id)  
    
     # skip first two characters of binary  
     # representation string and reverse  
     # remaining string and then append zeros  
     # after it. binary[-1:1:-1]  --> start  
     # from last character and reverse it until  
     # second last character from left  
     reverse = binary[-1:1:-1]  
     reverse = reverse + (EDGE_WIDTH - len(reverse))*'0'
    
     # converts reversed binary string into integer  
     return (int(reverse,2))  
        
class Tile:
    def __init__(self):
        self.id = 0
        self.rows = []
        self.allEdgeIds = []
        self.possibleConnections = set()
        
        #HFlip THEN rotate
        self.flipped = False
        self.rotations = 0
        self.pos = (0,0)
        
    def ComputeEdgeIds(self):
        north = self.ComputeEdgeId([0,0],[1,0])
        east = self.ComputeEdgeId([EDGE_WIDTH-1,0],[0,1])
        south = self.ComputeEdgeId([EDGE_WIDTH-1,EDGE_WIDTH-1],[-1,0])
        west = self.ComputeEdgeId([0,EDGE_WIDTH-1],[0,-1])
        
        self.allEdgeIds.append(north)
        self.allEdgeIds.append(east)
        self.allEdgeIds.append(south)
        self.allEdgeIds.append(west)
        self.allEdgeIds.append(FlipEdgeId(north))
        self.allEdgeIds.append(FlipEdgeId(west))
        self.allEdgeIds.append(FlipEdgeId(south))
        self.allEdgeIds.append(FlipEdgeId(east))
        
    def GetAbsoluteEdge(self, direction):
        #factors in flip and rot state
        if self.flipped:
            flipMult = 1
            flipAdd = 4
        else:
            flipMult = 1
            flipAdd = 0
        localDirection = RotateNQuarters(direction, -flipMult*self.rotations)
        return self.allEdgeIds[localDirection+flipAdd]
        
    def Get(self,x,y):
        return self.rows[y][x]
    def ComputeEdgeId(self, start, step):
        result = 0
        for i in range(EDGE_WIDTH):
            result *= 2
            pos = start[:]
            pos[0]+=i*step[0]
            pos[1]+=i*step[1]
            if self.Get(pos[0],pos[1])==1:
                result += 1
        return result
    def GetTransformedAndClippedRows(self):
        rows = FlipAndRotate(self.rows, self.flipped, self.rotations)
        rows = [row[1:-1] for row in rows[1:-1]] #TODO
        """for y in range(EDGE_WIDTH):
            for x in range(EDGE_WIDTH):
                if x == 0 or y == 0 or x == EDGE_WIDTH-1 or y == EDGE_WIDTH-1:
                    pass
                else:
                    rows[y][x] = False"""
        return rows
        
class Jigsaw:
    def __init__(self):
        self.tiles = []
        self.tileGrid = {} #(x,y)->Tile
        self.idToTile = {} #int->Tile
        self.idMatches = {} #int->set(Tile)
        self.assembledPuzzle = []
        self.tileRecursionCount = 0
        
    def Get(self,x,y):
        if (x,y) in self.tileGrid:
            return self.tileGrid((x,y))
        else:
            return None
            
    def ComputeEdgeIdMatches(self):
        for tile in self.tiles:
            tile.ComputeEdgeIds()
            
        for tile in self.tiles:
            self.idToTile[tile.id] = tile
            
        for tile in self.tiles:
            for edgeId in tile.allEdgeIds:
                if edgeId in self.idMatches:
                    self.idMatches[edgeId].add(tile)
                else:
                    self.idMatches[edgeId] = {tile}

        for tile in self.tiles:
            for edgeId in tile.allEdgeIds:
                for matchingTile in self.idMatches[edgeId]:
                    if matchingTile!=tile:
                        tile.possibleConnections.add(matchingTile)
        
    def FillGrid(self):
        self.tileGrid = {}
        tile = self.tiles[0]
        #SEAN TEST!!!
        #tile = self.idToTile[2063]
        tile.flipped = False
        tile.rotations = 0
        self.tileGrid[(0,0)] = tile
        
        self.FillMatchesFromTile(tile)
        
    def FillMatchesFromTile(self, tile):
            
        for direction in range(NUM_DIRECTIONS):
            edgeId = tile.GetAbsoluteEdge(direction)
            edgeIdOnOther = FlipEdgeId(edgeId)
            
            directionOnOther = RotateNQuarters(direction,2)
            
            otherTile = None
            for matchingTile in self.idMatches[edgeIdOnOther]:
                if matchingTile != tile:
                    otherTile = matchingTile
                    
            if otherTile == None:
                continue
                
            unit = DirectionToUnitVector(direction)
            posX = tile.pos[0]+unit[0]
            posY = tile.pos[1]+unit[1]
            pos = (posX,posY)
            
            if pos in self.tileGrid:
                continue
            
            found = False
            for flipped in [False,True]:
                for rotations in range(NUM_DIRECTIONS):
                    otherTile.flipped = flipped
                    otherTile.rotations = rotations
                    otherEdgeId = otherTile.GetAbsoluteEdge(directionOnOther)
                    if otherEdgeId == edgeIdOnOther:
                        found = True
                        break
                if found:
                    break
                    
            if not found:
                print("Problem")
                
            #if len(self.tileGrid) < 200: #TODO: Debug
            print("Matched " + str(tile.id) + " with " + str(otherTile.id) + ", placed at " + str(pos) + " in direction " + str(direction) + " flipped: " + str(otherTile.flipped) + ", rots:" + str(otherTile.rotations) + ", edge Id:" + str(edgeIdOnOther))
            self.tileGrid[pos] = otherTile
            otherTile.pos = pos
            self.FillMatchesFromTile(otherTile)
            
    def AssemblePuzzle(self):
        minX = 0
        maxX = 0
        minY = 0
        maxY = 0
        for pos in self.tileGrid:
            tile = self.tileGrid[pos]
            print(str(pos) + ": " + str(tile.id) + " " + str(tile.flipped) + " " + str(tile.rotations))
            if pos[0] < minX:
                minX = pos[0]
            if pos[1] < minY:
                minY = pos[1]
            if pos[0] > maxX:
                maxX = pos[0]
            if pos[1] > maxY:
                maxY = pos[1]
                
        rows = []
        for y in range(minY, maxY+1):
            transformedRows = []
            for x in range(minX, maxX+1):
                if (x,y) not in self.tileGrid:
                    empty = []
                    for ye in range(EDGE_WIDTH):
                        emptyRow = []
                        for xe in range(EDGE_WIDTH):
                            emptyRow.append(False)
                        empty.append(emptyRow)
                    
                    transformedRows.append(empty)
                else:
                    transformedRows.append(self.tileGrid[(x,y)].GetTransformedAndClippedRows())
            for rowNum in range(EDGE_WIDTH-2): #TODO: -2
                row = []
                for tileRows in transformedRows:
                    row.extend(tileRows[rowNum])
                rows.append(row)
        self.assembledPuzzle = rows
        return rows
            
    def FindMaskOccurences(self, mask, flipped, rotations):
        maskHeight = len(mask)
        maskWidth = len(mask[0])
        
        rotatedPuzzle = FlipAndRotate(self.assembledPuzzle, flipped, rotations)
        
        puzzleHeight = len(rotatedPuzzle)
        puzzleWidth = len(rotatedPuzzle[0])
        
        serpentTiles = set()
        
        numMasks = 0
        for startY in range(puzzleHeight-maskHeight+1):
            for startX in range(puzzleWidth-maskWidth+1):
                invalid = False
                for y in range(maskHeight):
                    for x in range(maskWidth):
                        if mask[y][x]:
                            if rotatedPuzzle[startY+y][startX+x]:
                                pass
                            else:
                                invalid = True
                                break
                if not invalid:
                    numMasks += 1
                    for y in range(maskHeight):
                        for x in range(maskWidth):
                            if mask[y][x]:
                                serpentTiles.add((startX+x,startY+y))
                    
                    
        return (numMasks,serpentTiles)
                    
            
jigsaw = Jigsaw()
with open("input.txt") as FILE:
    currentTile = Tile()
    for line in FILE:
        line = line.strip()
        if line.startswith("Tile"):
            currentTile.id = int(line.split(' ')[1][:-1])
        elif len(line)!=0:
            row = []
            for c in line:
                if c == '#':
                    row.append(1)
                else:
                    row.append(0)
            currentTile.rows.append(row)
        else:
            jigsaw.tiles.append(currentTile)
            currentTile = Tile()
    if len(currentTile.rows)>0:
        jigsaw.tiles.append(currentTile)
    
    
#Part A    
jigsaw.ComputeEdgeIdMatches()
                
product = 1
for tile in jigsaw.tiles:
    if len(tile.possibleConnections)==2:
        product *= tile.id
print("Part A: " + str(product)) #29293767579581

for tile in jigsaw.tiles:
    if len(tile.possibleConnections)>4:
       print(tile.id)
       
#Part B
jigsaw.FillGrid()
rows = jigsaw.AssemblePuzzle()

maskStr = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
mask = []

for row in maskStr.split('\n'):
    mask.append([(c == '#') for c in row])
    
totalTrue = CountTrue(jigsaw.assembledPuzzle)
maskTrue = CountTrue(mask)

print(mask)

print(totalTrue)
print(maskTrue)

PrintPuzzle(rows, {})

for flipped in [False,True]:
    for rotations in range(NUM_DIRECTIONS):
        monsters,serpentTiles = jigsaw.FindMaskOccurences(mask, flipped, rotations)
        if monsters > 0:
            print((flipped, rotations))
            PrintPuzzle(FlipAndRotate(rows,flipped,rotations), serpentTiles)
            print("Part B: " + str(totalTrue-len(serpentTiles))) #2094 too high, 2079 too high
        

    
"""
a = [[1,2,3],[4,5,6],[7,8,9]]
PrintMatrix(FlipAndRotate(a, False, 1))
print(FlipAndRotateCoordinate((0,0),3,True,0))"""
