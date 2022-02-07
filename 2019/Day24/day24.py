import math
import time

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
NUM_DIRECTIONS = 4

BUG = "#"
CLEAR = "."
RECURSE = "?"

NUM_BOTS = 4

def MirrorDirection(direction):
   return (direction+2)%4
   
def IncrementPosition(pos, direction, distance=1):
   if len(pos) == 2:
      if direction == UP:
         return (pos[0], pos[1]-distance)
      elif direction == DOWN:
         return (pos[0], pos[1]+distance)
      elif direction == LEFT:
         return (pos[0]-distance, pos[1])
      elif direction == RIGHT:
         return (pos[0]+distance, pos[1])
   else:
      if direction == UP:
         return (pos[0], pos[1]-distance, pos[2])
      elif direction == DOWN:
         return (pos[0], pos[1]+distance, pos[2])
      elif direction == LEFT:
         return (pos[0]-distance, pos[1], pos[2])
      elif direction == RIGHT:
         return (pos[0]+distance, pos[1], pos[2])
      
class MapData:
   def __init__(self):
      self.map = {}
      self.width = 0
      self.height = 0
      
   def FromString(self, mapStr):
      self.map = {}
      level = []
      for rowStr in mapStr.splitlines():
         row = []
         for c in rowStr.rstrip('\n'):
            row.append(c)
         if len(row) > 0:
            level.append(row)
      self.height = len(level)
      self.width = len(level[0])
      self.map[0] = level
   
   def ToString(self):
      mapStr = ""
      
      minDepth = 0
      maxDepth = 0
      for levelDepth in self.map:
         if levelDepth < minDepth:
            minDepth = levelDepth
         if levelDepth > maxDepth:
            maxDepth = levelDepth
            
      for levelDepth in xrange(minDepth, maxDepth+1):
         mapStr += "Depth: "
         mapStr += str(levelDepth)
         mapStr += "\n"
         
         level = self.map[levelDepth]
         
         for y in xrange(self.height):
            row = level[y]
            for c in row:
               mapStr += c
            mapStr += "\n"
      return mapStr#.rstrip()
      
   def MakeSteppedLevelCopy(self, levelDepth):
      level = []
      for y in xrange(self.height):
         row = []
         for x in xrange(self.width):
            row.append(CLEAR)
         level.append(row)
      level[self.height/2][self.width/2] = RECURSE
         
      for y in xrange(self.height):
         for x in xrange(self.width):
            startVal = self.GetCharacterAt((x, y, levelDepth))
            adjacentBugs = self.GetNumAdjacentBugs((x, y, levelDepth))
            
            level[y][x] = startVal #default
            if startVal == BUG:
               if adjacentBugs is not 1:
                  level[y][x] = CLEAR
            elif startVal == CLEAR:
               if adjacentBugs == 1 or adjacentBugs == 2:
                  level[y][x] = BUG
      return level
      
   def CountBugs(self):
      count = 0
      for levelDepth in self.map:
         level = self.map[levelDepth]
         for y in xrange(self.height):
            for x in xrange(self.width):
               if level[y][x] == BUG:
                  count += 1
      return count
      
   def Step(self):
      scratch = {}
      minDepth = 0
      maxDepth = 0
      for levelDepth in self.map:
         scratch[levelDepth] = self.MakeSteppedLevelCopy(levelDepth)
         if levelDepth < minDepth:
            minDepth = levelDepth
         if levelDepth > maxDepth:
            maxDepth = levelDepth
      scratch[minDepth-1] = self.MakeSteppedLevelCopy(minDepth-1)
      scratch[maxDepth+1] = self.MakeSteppedLevelCopy(maxDepth+1)
      self.map = scratch
      
   def GetNumAdjacentBugs(self, pos):
      count = 0         
      for direction in xrange(NUM_DIRECTIONS):    
         adjChar = self.GetCharacterAt(IncrementPosition(pos, direction))
         if adjChar == BUG:
            count += 1
         elif adjChar == RECURSE:
            newDepth = pos[2]+1
            #Look inwards, very zen
            if direction == RIGHT:
               count += self.GetBugsInRange((0,0,newDepth),(0,self.height-1,newDepth))
            elif direction == LEFT:
               count += self.GetBugsInRange((self.width-1,0,newDepth),(self.width-1,self.height-1,newDepth))
            elif direction == UP:
               count += self.GetBugsInRange((0,self.height-1,newDepth),(self.width-1,self.height-1,newDepth))
            elif direction == DOWN:
               count += self.GetBugsInRange((0,0,newDepth),(self.width-1,0,newDepth))
         elif adjChar == None:
            #Look outwards, not very zen
            newDepth = pos[2]-1
            center = (self.width/2, self.height/2, newDepth)
            outerPos = IncrementPosition(center, direction)
            if self.GetCharacterAt(outerPos) == BUG:
               count += 1
      return count
      
   def GetBugsInRange(self, min, max):
      count = 0
      for depth in xrange(min[2], max[2]+1):
         for y in xrange(min[1], max[1]+1):
            for x in xrange(min[0], max[0]+1):
               if self.GetCharacterAt((x,y,depth)) == BUG:
                  count += 1
      return count
      
   def GetCharacterAt(self, pos):
      x = pos[0]
      y = pos[1]
      depth = pos[2]
      
      if x == self.width/2 and y == self.height/2:
         return RECURSE
      
      
      if x < 0 or x >= self.width or y < 0 or y >= self.height:
         return None
         
      if depth not in self.map:
         return CLEAR
      
      return self.map[depth][y][x]
      
   def IsBug(self, pos):
      c = self.GetCharacterAt(pos)
      return c == BUG
      
   def IsClear(self, pos):
      c = self.GetCharacterAt(pos)
      return c == CLEAR

mapData = MapData()
mapStr = ""
with open("input.txt", "r") as FILE:
   mapStr = FILE.read()
   
#mapStr = 
"""....#
#..#.
#.?##
..#..
#...."""
   
mapData.FromString(mapStr)
mapData.map[0][2][2] = "?"

#print mapData.ToString()
#print "==================="
for i in xrange(200):
   mapData.Step()
   #print mapData.ToString()
   #print "==================="
print mapData.CountBugs()
   
"""
print mapData.ToString()
mapData.Step()
print mapData.ToString()
print mapData.GetNumAdjacentBugs((4,1))
mapData.Step()
print mapData.ToString()"""

"""exploredStates = set()
while True:
   score = mapData.GetScore()
   if score in exploredStates:
      print mapData.ToString()
      print score
      break
   exploredStates.add(score)
   
   mapData.Step()"""
