class Map:
    def __init__(self):
        self.rows = []
    def GetHeight(self):
        return len(self.rows)
    def GetWidth(self):
        return len(self.rows[0])
    def HasTree(self,x,y):
        newX = x%self.GetWidth()
        return self.rows[y][newX]
    def GetTreesAlongSlope(self, dx, dy):
        x = 0
        y = 0
        treeCount = 0
        while y < input.GetHeight():
            hasTree = input.HasTree(x,y)
            if hasTree:
                treeCount += 1
            x += dx
            y += dy
        return treeCount
        

input = Map()
with open("input.txt") as FILE:
    for line in FILE:
        row = []
        for c in line:
            if c == '.':
                row.append(False)
            elif c == '#':
                row.append(True)
        input.rows.append(row)
        
#Part a
print(input.GetTreesAlongSlope(3,1))

#Part b
print(input.GetTreesAlongSlope(1,1)*input.GetTreesAlongSlope(3,1)*input.GetTreesAlongSlope(5,1)*input.GetTreesAlongSlope(7,1)*input.GetTreesAlongSlope(1,2))