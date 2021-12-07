segments = []

class Segment:
    def __init__(self):
        self.start = (0,0)
        self.end = (0,0)
        
    def IsCardinal(self):
        return self.start[0] == self.end[0] or self.start[1] == self.end[1]
        
    def GeneratePointsHit(self):
        points = []
        if self.start[0] == self.end[0]:
            x = self.start[0]
            minY = min(self.start[1],self.end[1])
            maxY = max(self.start[1],self.end[1])
            for y in range(minY,maxY+1):
                points.append((x,y))
        elif self.start[1] == self.end[1]:
            y = self.start[1]
            minX = min(self.start[0],self.end[0])
            maxX = max(self.start[0],self.end[0])
            for x in range(minX,maxX+1):
                points.append((x,y))
        else:
            width = abs(self.end[0]-self.start[0])
            for i in range(width+1):
                x = 0
                y = 0
                if self.start[0]>self.end[0]:
                    x = self.start[0]-i
                else:
                    x = self.start[0]+i
                if self.start[1]>self.end[1]:
                    y = self.start[1]-i
                else:
                    y = self.start[1]+i
                points.append((x,y))
        return points

with open("input.txt") as FILE:
    for line in FILE.readlines():
        coordinates = line.split(" -> ")
        s = Segment()
        startTokens = coordinates[0].split(",")
        endTokens = coordinates[1].split(",")
        s.start = (int(startTokens[0]),int(startTokens[1]))
        s.end = (int(endTokens[0]),int(endTokens[1]))
        segments.append(s)
print(len(segments))

#part a
pointsHit = {}

for s in segments:
    if s.IsCardinal():
        points = s.GeneratePointsHit()
        for p in points:
            if p in pointsHit:
                pointsHit[p] = pointsHit[p]+1
            else:
                pointsHit[p] = 1
 
partA = 0
for key in pointsHit:
   if pointsHit[key] > 1:
       partA += 1
print(partA)

#part b
pointsHit = {}

for s in segments:
    points = s.GeneratePointsHit()
    for p in points:
        if p in pointsHit:
            pointsHit[p] = pointsHit[p]+1
        else:
            pointsHit[p] = 1
 
partA = 0
for key in pointsHit:
   if pointsHit[key] > 1:
       partA += 1
print(partA)