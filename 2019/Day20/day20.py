import math
import time

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
NUM_DIRECTIONS = 4

WALL = "#"
CLEAR = "."

NUM_BOTS = 4

def MirrorDirection(direction):
   return (direction+2)%4
   
def IncrementPosition(pos, direction, distance=1):
   if len(pos) == 2:
      if direction == UP:
         return (pos[0], pos[1]+distance)
      elif direction == DOWN:
         return (pos[0], pos[1]-distance)
      elif direction == LEFT:
         return (pos[0]-distance, pos[1])
      elif direction == RIGHT:
         return (pos[0]+distance, pos[1])
   else:
      if direction == UP:
         return (pos[0], pos[1]+distance, pos[2])
      elif direction == DOWN:
         return (pos[0], pos[1]-distance, pos[2])
      elif direction == LEFT:
         return (pos[0]-distance, pos[1], pos[2])
      elif direction == RIGHT:
         return (pos[0]+distance, pos[1], pos[2])
      
class MapData:
   def __init__(self):
      self.map = []
      self.width = 0
      self.height = 0
      self.startPos = None
      self.endPos = None
      self.innerTeleportSpots = {}
      self.outerTeleportSpots = {}
      
   def FromString(self, mapStr):
      self.map = []
      for rowStr in mapStr.splitlines():
         row = []
         for c in rowStr.rstrip('\n'):
            row.append(c)
         if len(row) > 0:
            self.map.append(row)
      self.map = self.map[::-1]
      self.height = len(self.map)
      self.width = len(self.map[0])
      self.innerTeleportSpots = {}
      self.outerTeleportSpots = {}
      
      unpairedWarps = {}
      for y in xrange(self.height):
         for x in xrange(self.width):
            pos = (x,y)
            c = self.GetCharacterAt(pos)
            if c == CLEAR:
               for direction in xrange(NUM_DIRECTIONS):
                  testPos = IncrementPosition(pos, direction)
                  testChar = self.GetCharacterAt(testPos)
                  if testChar.isupper():
                     otherTile = IncrementPosition(testPos, direction)
                     otherChar = self.GetCharacterAt(otherTile)
                     if direction == RIGHT or direction == DOWN:
                        warpName = testChar + otherChar
                     else:
                        warpName = otherChar + testChar
                     if warpName in unpairedWarps:
                        outerInnerTestTile = IncrementPosition(otherTile, direction)
                        outerInnerTestChar = self.GetCharacterAt(outerInnerTestTile)
                        otherPos = unpairedWarps[warpName]
                        if outerInnerTestChar == "!":
                           self.outerTeleportSpots[pos] = otherPos
                           self.innerTeleportSpots[otherPos] = pos
                        else:
                           self.innerTeleportSpots[pos] = otherPos
                           self.outerTeleportSpots[otherPos] = pos
                     else:
                        unpairedWarps[warpName] = pos
                     break
      self.startPos = unpairedWarps["AA"]
      self.startPos = (self.startPos[0], self.startPos[1], 0)
      self.endPos = unpairedWarps["ZZ"]
      self.endPos = (self.endPos[0], self.endPos[1], 0)
   
   def ToString(self):
      mapStr = ""
      for y in xrange(len(self.map)-1, -1, -1):
         row = self.map[y]
         for c in row:
            mapStr += c
         mapStr += "\n"
      return mapStr.rstrip()
         
   def FindShortestDistance(self):
         
      exploredTiles = set()
      currentTiles = set()
      
      exploredTiles.add(self.startPos)
      currentTiles.add(self.startPos)
      """
      print len(self.outerTeleportSpots)
      print len(self.innerTeleportSpots)
      print self.innerTeleportSpots
      
      print self.startPos
      print self.endPos"""
      
      iterations = 1
      while len(currentTiles) > 0:
         print str(iterations)# + ": " + str(len(currentTiles)) + " " + str(currentTiles)
         newTiles = set()
         for tile in currentTiles:
            for direction in xrange(NUM_DIRECTIONS):
               testTile = IncrementPosition(tile, direction)
               #DUPLICATED
               if testTile == self.endPos:
                  return iterations
               if testTile not in exploredTiles:
                  tileType = self.GetCharacterAt(testTile)
                  if tileType == CLEAR:
                     newTiles.add(testTile)
                     exploredTiles.add(testTile)
               #END DUPLICATED
            tile2D = (tile[0], tile[1])
            if tile2D in self.innerTeleportSpots:
               testTile = self.innerTeleportSpots[tile2D]
               testTile = (testTile[0], testTile[1], tile[2]+1)
               #DUPLICATED
               if testTile == self.endPos:
                  return iterations
               if testTile not in exploredTiles:
                  tileType = self.GetCharacterAt(testTile)
                  if tileType == CLEAR:
                     newTiles.add(testTile)
                     exploredTiles.add(testTile)
               #END DUPLICATED
            if tile[2] > 0: #can't take outer teleports at outermost level
               if tile2D in self.outerTeleportSpots:
                  testTile = self.outerTeleportSpots[tile2D]
                  testTile = (testTile[0], testTile[1], tile[2]-1)
                  #DUPLICATED
                  if testTile == self.endPos:
                     return iterations
                  if testTile not in exploredTiles:
                     tileType = self.GetCharacterAt(testTile)
                     if tileType == CLEAR:
                        newTiles.add(testTile)
                        exploredTiles.add(testTile)
                  #END DUPLICATED
         currentTiles = newTiles
         iterations += 1
      
   def GetCharacterAt(self, pos):
      x = pos[0]
      y = pos[1]
      
      if x < 0 or x >= self.width or y < 0 or y >= self.height:
         return "!"
      
      return self.map[y][x]
      
   def IsWall(self, pos):
      c = self.GetCharacterAt(pos)
      return c == WALL
      
   def IsClear(self, pos):
      c = self.GetCharacterAt(pos)
      return c == CLEAR
      
   def IsDeadEnd(self, pos):
      numWalls = 0
      if not self.IsClear(pos):
         return False
      for i in xrange(NUM_DIRECTIONS):
         newPos = IncrementPosition(pos, i)
         if self.IsWall(newPos):
            numWalls += 1
      return numWalls >= 3
   
   def FillGaps(self):
      numGapsFilled = 0
      for y in xrange(self.height):
         for x in xrange(self.width):
            pos = (x,y)
            if self.IsDeadEnd(pos):
               self.map[y][x] = WALL
               numGapsFilled += 1
      #Go Agane
      if numGapsFilled > 0:
         self.FillGaps()
         

mapData = MapData()
mapStr = ""
with open("input.txt", "r") as FILE:
   mapStr = FILE.read()
   
#mapStr = 
"""             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """
mapData.FromString(mapStr)
   

print mapData.ToString()
print mapData.FindShortestDistance()