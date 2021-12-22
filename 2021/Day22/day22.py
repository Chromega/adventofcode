import copy
import functools

NUM_DIMENSIONS = 3

def SegmentIntersects(s1,s2): #1d (min,max) segments, max is exclusive
    return s1[1] > s2[0] and s2[1] > s1[0]
    
class Cuboid():
    def __init__(self):
        self.min = (0,0,0)
        self.max = (0,0,0) #exclusive
        self.on = True
        
    def GetSize(self):
        return (self.max[0]-self.min[0])*(self.max[1]-self.min[1])*(self.max[2]-self.min[2])
        
    def IntersectsWithOther(self,other):
        for i in range(NUM_DIMENSIONS):
            s1 = (self.min[i],self.max[i])
            s2 = (other.min[i],other.max[i])
            if not SegmentIntersects(s1,s2): #we dont intersect, so no change to c1 needed
                return False
        return True
        
    def __str__(self):
        return str(self.min) + "->" + str(self.max) + "..." + str(self.GetSize())

input = []
with open("input.txt") as FILE:
    currentScanner = None
    for line in FILE.readlines():
        line = line.strip()
        tokens = line.split(' ')
        coordsToken = tokens[1].split(',')
        x = [int(x) for x in coordsToken[0][2:].split('..')]
        y = [int(x) for x in coordsToken[1][2:].split('..')]
        z = [int(x) for x in coordsToken[2][2:].split('..')]
        c = Cuboid()
        c.min = (x[0],y[0],z[0])
        c.max = (x[1]+1,y[1]+1,z[1]+1)
        c.on = tokens[0]=="on"
        input.append(c)


def IntersectCuboids(c1, c2): #return new c1 replacement
    #check if any overlap
    if not c1.IntersectsWithOther(c2):
        return [c1]
            
    perAxisValues = []
    for i in range(NUM_DIMENSIONS):
        thisAxisValues = [c1.min[i],c1.max[i],c2.min[i],c2.max[i]]
        thisAxisValues.sort()
        perAxisValues.append(thisAxisValues)
        
    newCuboids = []
    for i in range(3):
        xSegment = (perAxisValues[0][i],perAxisValues[0][i+1])
        for j in range(3):
            ySegment = (perAxisValues[1][j],perAxisValues[1][j+1])
            for k in range(3):
                zSegment = (perAxisValues[2][k],perAxisValues[2][k+1])
                possibleNewCuboid = Cuboid()
                possibleNewCuboid.min = (xSegment[0],ySegment[0],zSegment[0])
                possibleNewCuboid.max = (xSegment[1],ySegment[1],zSegment[1])
                possibleNewCuboid.on = c1.on
                #print(possibleNewCuboid)
                if not possibleNewCuboid.IntersectsWithOther(c2) and possibleNewCuboid.IntersectsWithOther(c1):
                    newCuboids.append(possibleNewCuboid)
    return newCuboids
    
#part a
cuboidsToAdd = copy.deepcopy(input)
state = []
printedA = False
for c in cuboidsToAdd:
    if not printedA and abs(c.min[0])>50:
        print(functools.reduce(lambda a,b: a+b.GetSize(), state, 0))
        printedA = True
    newState = []
    for existingCuboid in state:
        newCuboids = IntersectCuboids(existingCuboid,c)
        newState.extend(newCuboids)
    if c.on:
        newState.append(c)
    state = newState
    
print(functools.reduce(lambda a,b: a+b.GetSize(), state, 0))