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
   if direction == UP:
      return (pos[0], pos[1]+distance)
   elif direction == DOWN:
      return (pos[0], pos[1]-distance)
   elif direction == LEFT:
      return (pos[0]-distance, pos[1])
   elif direction == RIGHT:
      return (pos[0]+distance, pos[1])
      
class MapData:
   def __init__(self):
      self.map = []
      self.width = 0
      self.height = 0
      self.teleportSpots = {}
      self.startPos = None
      self.endPos = None
      
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
      self.teleportSpots = {}
      
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
                        otherPos = unpairedWarps[warpName]
                        self.teleportSpots[otherPos] = pos
                        self.teleportSpots[pos] = otherPos
                     else:
                        unpairedWarps[warpName] = pos
                     break
      self.startPos = unpairedWarps["AA"]
      self.endPos = unpairedWarps["ZZ"]
   
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
      
      iterations = 1
      while len(currentTiles) > 0:
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
            if tile in self.teleportSpots:
               testTile = self.teleportSpots[tile]
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
   
mapStr = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """
mapData.FromString(mapStr)
   

print mapData.ToString()
print mapData.FindShortestDistance()