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
      
   bestCoords = None
   bestCount = 0
   for y0 in xrange(len(grid)):
      for x0 in xrange(len(grid[y0])):
         if grid[y0][x0]:
            count = GetNumVisibleAsteroids(grid, x0, y0)
            if count > bestCount:
               bestCount = count
               bestCoords = (x0, y0)
            #print "(" + str(x0) + ", " + str(y0) + ") - " + str(count)
               
   print bestCount
   print bestCoords