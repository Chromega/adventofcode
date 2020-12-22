class MapState():
    def __init__(self):
        self.active = set() #i,i,i,i

    def GetBounds(self):
        min = [0,0,0,0]
        max = [0,0,0,0]
        
        for pos in self.active:
            for dim in range(4):
                if pos[dim]<min[dim]:
                    min[dim]=pos[dim]
                if pos[dim]>max[dim]:
                    max[dim]=pos[dim]
                    
        return (min,max)
        
    def GetNumAdjacent(self, cell):
        count = 0
        for i in range(-1,2):
            for j in range(-1,2):
                for k in range(-1,2):
                    for l in range(-1,2):
                        if i == 0 and j == 0 and k == 0 and l == 0:
                            continue
                        cellToCheck=(cell[0]+i,cell[1]+j,cell[2]+k,cell[3]+l)
                        if cellToCheck in self.active:
                            count += 1
        return count
        
    def Step(self):
        newSet = set()
        
        min,max=self.GetBounds()
        
        for i in range(min[0]-1,max[0]+2):
            for j in range(min[1]-1,max[1]+2):
                for k in range(min[2]-1,max[2]+2):
                    for l in range(min[3]-1,max[3]+2):
                        myPos = (i,j,k,l)
                        myActiveState = myPos in self.active
                        numAdjacent = self.GetNumAdjacent(myPos)
                        if myActiveState:
                            if numAdjacent == 2 or numAdjacent == 3:
                                newSet.add(myPos)
                        else:
                            if numAdjacent == 3:
                                newSet.add(myPos)
                            
        newState = MapState()
        newState.active = newSet
        return newState
        
input = MapState()
with open("input.txt") as FILE:
    y = -1
    for line in FILE:
        y += 1
        line = line.strip()
        x = -1
        for c in line:
            x += 1
            if c == '#':
                input.active.add((x,y,0,0))
                
currentState = input
print(len(currentState.active))
for i in range(6):
    currentState = currentState.Step()
    print(len(currentState.active))