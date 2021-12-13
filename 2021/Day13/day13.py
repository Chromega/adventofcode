input = set()
folds = []

class XFold:
    def __init__(self,x):
        self.x = x
    def Transform(self, coord):
        x, y = coord
        if x > self.x:
            x = 2*self.x - x
        return (x,y)
        
        
class YFold:
    def __init__(self,y):
        self.y = y
    def Transform(self, coord):
        x, y = coord
        if y > self.y:
            y = 2*self.y - y
        return (x,y)

READ_COORDINATES=0
READ_FOLDS=1
inputMode = READ_COORDINATES
with open("input.txt") as FILE:
    for line in FILE.readlines():
        line = line.strip()
        if inputMode == READ_COORDINATES:
            if len(line)==0:
                inputMode = READ_FOLDS
            else:
                coords = line.split(',')
                newCoord = (int(coords[0]),int(coords[1]))
                input.add(newCoord)
        else:
            tokens = line.split('=')
            if tokens[0][-1]=='x':
                folds.append(XFold(int(tokens[1])))
            else:
                folds.append(YFold(int(tokens[1])))

#part a
foldedInput = input.copy()
for fold in folds:
    nextFoldedInput = set()
    for point in foldedInput:
        newPoint = fold.Transform(point)
        nextFoldedInput.add(newPoint)
    foldedInput = nextFoldedInput
    print(len(foldedInput)) 

#part b
minX = 9999999
maxX = -9999999
minY = 9999999
maxY = -9999999
for point in foldedInput:
    x,y = point
    minX = min(x,minX)
    maxX = max(x,maxX)
    minY = min(y,minY)
    maxY = max(y,maxY)
    
for y in range(minY,maxY+1):
    row = ""
    for x in range(minX,maxX+1):
        coord = (x,y)
        if coord in foldedInput:
            row += "#"
        else:
            row += "."
    print(row)
        