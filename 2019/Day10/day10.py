import math

def gcd(x,y):
   while (y):
      x,y = y,x%y
   return x
   
def GetNumVisibleAsteroids(grid, x0, y0):
   count = 0
   for y1 in xrange(len(grid)):
      for x1 in xrange(len(grid[y0])):
         if x0 == x1 and y0 == y1:
            continue
      
         if grid[y1][x1]:
            deltaY = y1 - y0
            deltaX = x1 - x0
            
            if deltaX == 0:
               gcdDelta = int(math.fabs(deltaY))
            elif deltaY == 0:
               gcdDelta = int(math.fabs(deltaX))
            else:
               gcdDelta = gcd(int(math.fabs(deltaX)), int(math.fabs(deltaY)))
            stepX = deltaX/gcdDelta
            stepY = deltaY/gcdDelta
            
            asteroidInTheWay = False
            for i in xrange(1, gcdDelta):
               if grid[y0+stepY*i][x0+stepX*i]:
                  asteroidInTheWay = True
                  break
            if not asteroidInTheWay:
               count += 1
               #print "Hit " + str((x1,y1))
               #print gcdDelta
               #print (stepX, stepY)
   return count
   
   
def FindNextAsteroidToVaporize(grid, x0, y0, lastAngle):   
   bestAngleDelta = 360
   bestDistance = 0
   bestCoords = None
   bestAngle = 0
   
   for y1 in xrange(len(grid)):
      for x1 in xrange(len(grid[y0])):
         if x0 == x1 and y0 == y1:
            continue
      
         if grid[y1][x1]:
            deltaY = y1 - y0
            deltaX = x1 - x0
            
            angle = math.atan2(deltaX, -deltaY) * 180 / math.pi
            angleDelta = (angle - lastAngle + 360)%360
            distance = math.fabs(deltaX)+math.fabs(deltaY) #manhattan fine
            
            isBest = False
            if angleDelta < bestAngleDelta:
               isBest = True
            elif angleDelta == bestAngleDelta:
               if distance < bestDistance:
                  isBest = True
            
            if isBest:
               bestCoords = (x1, y1)
               bestAngleDelta = angleDelta
               bestDistance = distance
               bestAngle = angle
            
   return bestCoords, bestAngle

with open("input.txt", "r") as FILE:
   grid = []
   for line in FILE.readlines():
      row = []
      for c in line.strip():
         if c == '#':
            row.append(True)
         else:
            row.append(False)
      grid.append(row)
      
   x0 = 17
   y0 = 22
   #x0 = 11
   #y0 = 13
   
   vaporized = []
   angle = -.000001
   while True:
      nextCoords, angle = FindNextAsteroidToVaporize(grid, x0, y0, angle)
      if nextCoords is not None:
         vaporized.append(nextCoords)
         grid[nextCoords[1]][nextCoords[0]] = False
      else:
         break
      angle += .000001
   print vaporized
   print vaporized[199]
   print vaporized[199][0]*100+vaporized[199][1]