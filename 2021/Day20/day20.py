code = []
initialMap = []

READ_CODE = 0
READ_MAP = 1
inputMode = READ_CODE
with open("input.txt") as FILE:
    currentScanner = None
    for line in FILE.readlines():
        line = line.strip()
        if len(line) == 0:
            inputMode = READ_MAP
        elif inputMode == READ_CODE:
            code = [x=="#" for x in line]
        else:
            initialMap.append([x=="#" for x in line])
            
def MapSliceToIndex(map, point):
    height = len(map)
    width = len(map[0])
    val = 0
    for y in range(point[1]-1,point[1]+2):
        for x in range(point[0]-1,point[0]+2):
            val *= 2
            inBounds = y>=0 and y < height and x >= 0 and x < width
            if not inBounds:
                x = max(0,x)
                x = min(x,width-1)
                y = max(0,y)
                y = min(y,height-1)
            if map[y][x]:
                val += 1
    return val
    
def PadMap(map,padding):
    oldHeight = len(map)
    oldWidth = len(map[0])
    newMap = []
    for i in range(padding):
        newMap.append([False]*(oldWidth+2*padding))
    for i in range(oldHeight):
        newRow = [False]*padding
        newRow += map[i]
        newRow += [False]*padding
        newMap.append(newRow)
    for i in range(padding):
        newMap.append([False]*(oldWidth+2*padding))
    return newMap
        
def Step(map,code):
    height = len(map)
    width = len(map[0])
    
    newMap = []
    for y in range(height):
        newRow = []
        for x in range(width):
            codeIdx = MapSliceToIndex(map,(x,y))
            val = code[codeIdx]
            newRow.append(val)
        newMap.append(newRow)
    return newMap
    
def PrintMap(map):
    print("")
    for row in map:
        s = ""
        for val in row:
            s += ("#" if val else ".")
        print(s)
#part a
map = PadMap(initialMap,3)
for i in range(2):
    map = Step(map,code)
    
count = 0
for row in map:
    for val in row:
        if val:
            count += 1
print(count)

#part b
map = PadMap(initialMap,51)
for i in range(50):
    map = Step(map,code)
    
count = 0
for row in map:
    for val in row:
        if val:
            count += 1
print(count)