import math
import time

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
NUM_DIRECTIONS = 4

BUG = "#"
CLEAR = "."

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
      self.map = []
      self.width = 0
      self.height = 0
      self.scratch = []
      
   def FromString(self, mapStr):
      self.map = []
      for rowStr in mapStr.splitlines():
         row = []
         for c in rowStr.rstrip('\n'):
            row.append(c)
         if len(row) > 0:
            self.map.append(row)
      self.height = len(self.map)
      self.width = len(self.map[0])
      
      self.scratch = []
      for y in xrange(self.height):
         self.scratch.append([0 for i in xrange(self.width)])
   
   def ToString(self):
      mapStr = ""
      for y in xrange(len(self.map)):
         row = self.map[y]
         for c in row:
            mapStr += c
         mapStr += "\n"
      return mapStr#.rstrip()
      
   def GetScore(self):
      score = 0
      for y in xrange(self.height):
         for x in xrange(self.width):
            bug = self.map[y][x]==BUG
            if bug:
               shiftAmount = x + y*self.width
               score += 1 << shiftAmount
      return score
      
   def Step(self):
      for y in xrange(self.height):
         for x in xrange(self.width):
            startVal = self.GetCharacterAt((x,y))
            adjacentBugs = self.GetNumAdjacentBugs((x,y))
            
            self.scratch[y][x] = startVal #default
            if startVal == BUG:
               if adjacentBugs is not 1:
                  self.scratch[y][x] = CLEAR
            elif startVal == CLEAR:
               if adjacentBugs == 1 or adjacentBugs == 2:
                  self.scratch[y][x] = BUG
      self.SwapBuffers()
      
   def GetNumAdjacentBugs(self, pos):
      count = 0
      for direction in xrange(NUM_DIRECTIONS):
         if self.GetCharacterAt(IncrementPosition(pos, direction)) == BUG:
            count += 1
      return count
      
   def GetCharacterAt(self, pos):
      x = pos[0]
      y = pos[1]
      
      if x < 0 or x >= self.width or y < 0 or y >= self.height:
         return None
      
      return self.map[y][x]
      
   def IsBug(self, pos):
      c = self.GetCharacterAt(pos)
      return c == BUG
      
   def IsClear(self, pos):
      c = self.GetCharacterAt(pos)
      return c == CLEAR
         
   def SwapBuffers(self):
      temp = self.map
      self.map = self.scratch
      self.scratch = temp

mapData = MapData()
mapStr = ""
with open("input.txt", "r") as FILE:
   mapStr = FILE.read()
   
#mapStr = 
"""....#
#..#.
#..##
..#..
#...."""
   
mapData.FromString(mapStr)
   
"""
print mapData.ToString()
mapData.Step()
print mapData.ToString()
print mapData.GetNumAdjacentBugs((4,1))
mapData.Step()
print mapData.ToString()"""

exploredStates = set()
while True:
   score = mapData.GetScore()
   if score in exploredStates:
      print mapData.ToString()
      print score
      break
   exploredStates.add(score)
   
   mapData.Step()