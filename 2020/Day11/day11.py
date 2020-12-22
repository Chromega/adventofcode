import copy

FLOOR = 0
EMPTY = 1
OCCUPIED = 2
EDGE = 3

class Map:
    def __init__(self):
        self.rows = []
        
    def Copy(self):
        return copy.deepcopy(self)
        
    def Step(self):
        newRows = []
        for y in range(self.GetHeight()):
            newRow = []
            for x in range(self.GetWidth()):
                state = self.Get(x,y)
                numAdjacent = self.GetNumAdjacentOccupied(x,y)
                if state == FLOOR:
                    newRow.append(FLOOR)
                elif state == EMPTY:
                    if numAdjacent == 0:
                        newRow.append(OCCUPIED)
                    else:
                        newRow.append(EMPTY)
                elif state == OCCUPIED:
                    if numAdjacent >= 4:
                        newRow.append(EMPTY)
                    else:
                        newRow.append(OCCUPIED)
            newRows.append(newRow)
        
        for y in range(self.GetHeight()):
            for x in range(self.GetWidth()):
                if self.rows[y][x] != newRows[y][x]:
                    self.rows = newRows
                    return True
        
        self.rows = newRows
        return False
        
    def Step2(self):
        newRows = []
        for y in range(self.GetHeight()):
            newRow = []
            for x in range(self.GetWidth()):
                state = self.Get(x,y)
                if state == FLOOR:
                    newRow.append(FLOOR)
                elif state == EMPTY:
                    numAdjacent = self.GetNumVisibleOccupied(x,y)
                    if numAdjacent == 0:
                        newRow.append(OCCUPIED)
                    else:
                        newRow.append(EMPTY)
                elif state == OCCUPIED:
                    numAdjacent = self.GetNumVisibleOccupied(x,y)
                    if numAdjacent >= 5:
                        newRow.append(EMPTY)
                    else:
                        newRow.append(OCCUPIED)
            newRows.append(newRow)
        
        for y in range(self.GetHeight()):
            for x in range(self.GetWidth()):
                if self.rows[y][x] != newRows[y][x]:
                    self.rows = newRows
                    return True
        
        self.rows = newRows
        return False
        
    def GetHeight(self):
        return len(self.rows)
        
    def GetWidth(self):
        return len(self.rows[0])
        
    def Get(self, x, y):
        if y < 0 or y >= self.GetHeight() or x < 0 or x >= self.GetWidth():
            return EDGE
        return self.rows[y][x]
        
    def GetNumAdjacentOccupied(self,x,y):
        count = 0
        for dx in range(-1,2):
            for dy in range(-1,2):
                if dx == 0 and dy == 0:
                    continue
                if self.Get(x+dx,y+dy) == OCCUPIED:
                    count += 1
        return count
        
    def GetNumVisibleOccupied(self,x,y):
        count = 0
        for dx in range(-1,2):
            for dy in range(-1,2):
                if dx == 0 and dy == 0:
                    continue
                magnitude = 1
                while True:
                    newX = x + magnitude*dx
                    newY = y + magnitude*dy
                    if self.Get(newX,newY) == EDGE:
                        break
                    if self.Get(newX,newY) == OCCUPIED:
                        count += 1
                        break
                    if self.Get(newX,newY) == EMPTY:
                        break
                    magnitude += 1
        return count
                    
    def CountOccupied(self):
        count = 0
        for y in range(self.GetHeight()):
            for x in range(self.GetWidth()):
                if self.rows[y][x] == OCCUPIED:
                    count += 1
        return count
        
    def Print(self):
        for y in range(self.GetHeight()):
            rowStr = ""
            for x in range(self.GetWidth()):
                rowStr += str(self.rows[y][x])
            print(rowStr)
        print(" ")
  
input = Map()  
with open("input.txt") as FILE:
    for line in FILE:
        line = line.strip()
        row = []
        for c in line:
            if c == '.':
                row.append(FLOOR)
            elif c == '#':
                row.append(OCCUPIED)
            elif c == "L":
                row.append(EMPTY)
        input.rows.append(row)

        
#part a 28:40
partA = input.Copy()
    
while partA.Step():
    pass#partA.Print()
print(partA.CountOccupied())

#part b
partB = input.Copy()
while partB.Step2():
    pass #partB.Print()
print(partB.CountOccupied())