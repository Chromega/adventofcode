class Segment:
   isVertical = False
   parallelValue = 0
   perpendicularRange = (0,0)
   isReverse = False
   distanceToStart = 0
   
   def intersects(self, other):
      if self.isVertical == other.isVertical:
         return None
         
      if self.parallelValue >= other.perpendicularRange[0] and self.parallelValue <= other.perpendicularRange[1] and other.parallelValue >= self.perpendicularRange[0] and other.parallelValue <= self.perpendicularRange[1]:
         if self.isVertical:
            return [self.parallelValue, other.parallelValue]
         else:
            return [other.parallelValue, self.parallelValue]
         
      return None
      
   #assuming point is on line segment
   def DistanceToPoint(self, point):
      distanceThisSegment = 0
      if self.isVertical:
         if self.isReverse:
            distanceThisSegment = self.perpendicularRange[1] - point[1]
         else:
            distanceThisSegment = point[1] - self.perpendicularRange[0]
      else:
         if self.isReverse:
            distanceThisSegment = self.perpendicularRange[1] - point[0]
         else:
            distanceThisSegment = point[0] - self.perpendicularRange[0]
            
      return self.distanceToStart + distanceThisSegment

with open("input.txt", "r") as FILE:
   paths = [] #array of segment arrays
   for line in FILE.readlines():
      moves = line.strip().split(',')
      currentPosition = [0,0]
      path = []
      distanceSoFar = 0
      for move in moves:
         segment = Segment()
         startPos = currentPosition
         direction = move[0]
         distance = int(move[1:])
         
         if direction == 'U':
            segment.isVertical = True
            currentPosition = [startPos[0], startPos[1]+distance]
            segment.parallelValue = currentPosition[0]
            segment.perpendicularRange = [startPos[1], currentPosition[1]]
            segment.isReverse = False
         elif direction == 'D':
            segment.isVertical = True
            currentPosition = [startPos[0], startPos[1]-distance]
            segment.parallelValue = currentPosition[0]
            segment.perpendicularRange = [currentPosition[1], startPos[1]]
            segment.isReverse = True
         elif direction == 'L':
            segment.isVertical = False
            currentPosition = [startPos[0]-distance, startPos[1]]
            segment.parallelValue = currentPosition[1]
            segment.perpendicularRange = [currentPosition[0], startPos[0]]
            segment.isReverse = True
         elif direction == 'R':
            segment.isVertical = False
            currentPosition = [startPos[0]+distance, startPos[1]]
            segment.parallelValue = currentPosition[1]
            segment.perpendicularRange = [startPos[0], currentPosition[0]]
            segment.isReverse = False
         
         segment.distanceToStart = distanceSoFar
         distanceSoFar += distance
            
         path.append(segment)
      paths.append(path)
      
   smallestDistance = 999999999
   for seg1 in paths[0]:
      for seg2 in paths[1]:
         point = seg1.intersects(seg2)
         if point is not None:
            #distance = abs(point[0]) + abs(point[1]) #part 1
            distance = seg1.DistanceToPoint(point)+seg2.DistanceToPoint(point)
            if distance > 0 and distance < smallestDistance:
               smallestDistance = distance
   print smallestDistance