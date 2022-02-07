import math
import time

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
NUM_DIRECTIONS = 4

WALL = "#"
CLEAR = "."
START = "@"

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

class PathState:
   def __init__(self):
      self.keys = None
      self.positions = None
      self.hash = None
      
   def __eq__(self, other):
      for i in xrange(len(self.positions)):
         if self.positions[i] != other.positions[i]:
            return False
         
      if len(self.keys) != len(other.keys):
         return False
         
      for key in self.keys:
         if key not in other.keys:
            return False
      
      return True
      
   def __ne__(self, other):
      return not self.__eq__(other)
      
   def __hash__(self):
      if self.hash is not None:
         return self.hash
         
      self.hash = 0
      for key in self.keys:
         self.hash += key.__hash__()
      for pos in self.positions:
         self.hash += pos.__hash__()
      
      return self.hash
      
class MapData:
   def __init__(self):
      self.map = []
      self.width = 0
      self.height = 0
      self.keyPositions = {}
      self.cachedDistances = {} #(a,b)=>(dist, [keysNeeded])
      self.keysForBot = []
      
   def FromString(self, mapStr):
      self.map = []
      for rowStr in mapStr.splitlines():
         row = []
         for c in rowStr.strip():
            row.append(c)
         if len(row) > 0:
            self.map.append(row)
      self.map = self.map[::-1]
      self.height = len(self.map)
      self.width = len(self.map[0])
      self.keyPositions = {}
      
      startPos = self.GetStartPos()
      self.map[startPos[1]+1][startPos[0]-1] = '1'
      self.map[startPos[1]+1][startPos[0]] = WALL
      self.map[startPos[1]+1][startPos[0]+1] = '2'
      
      self.map[startPos[1]][startPos[0]-1] = WALL
      self.map[startPos[1]][startPos[0]] = WALL
      self.map[startPos[1]][startPos[0]+1] = WALL
      
      self.map[startPos[1]-1][startPos[0]-1] = '3'
      self.map[startPos[1]-1][startPos[0]] = WALL
      self.map[startPos[1]-1][startPos[0]+1] = '4'
      
      for y in xrange(self.height):
         for x in xrange(self.width):
            pos = (x,y)
            c = self.GetCharacterAt(pos)
            if c.islower():
               self.keyPositions[c] = pos
               
      self.ComputePairwiseDistances()
   
   def ToString(self):
      mapStr = ""
      for y in xrange(len(self.map)-1, -1, -1):
         row = self.map[y]
         for c in row:
            mapStr += c
         mapStr += "\n"
      return mapStr.strip()
      
   def ComputePairwiseDistances(self):
      self.cachedDistances = {}
      keyList = self.keyPositions.keys()
      self.CacheReachableKeys('1')
      self.CacheReachableKeys('2')
      self.CacheReachableKeys('3')
      self.CacheReachableKeys('4')
      for key in keyList:
         self.CacheReachableKeys(key)
         
      self.keysForBot = []
      for i in xrange(NUM_BOTS):
         botToken = str(i+1)
         botKeys = set()
         for key in keyList:
            if (botToken, key) in self.cachedDistances:
               botKeys.add(key)
         self.keysForBot.append(botKeys)
         
   def CacheReachableKeys(self, start):
      pos = self.GetPositionOfCharacter(start)
         
      exploredTiles = {} #pos->[keys]
      currentTiles = set()
      currentTiles.add(pos)
      exploredTiles[pos] = []
      
      iterations = 1
      while len(currentTiles) > 0:
         newTiles = set()
         for tile in currentTiles:
            for direction in xrange(NUM_DIRECTIONS):
               testTile = IncrementPosition(tile, direction)
               currentKeysNeeded = exploredTiles[tile]
               if testTile not in exploredTiles:
                  tileType = self.GetCharacterAt(testTile)
                  #Wall, done
                  if tileType == WALL:
                     continue
                  #Door or key
                  elif tileType != CLEAR and tileType != START:
                     #Door
                     if tileType.isupper():
                        key = tileType.lower()
                        #Locked door
                        currentKeysNeeded = currentKeysNeeded[:]
                        currentKeysNeeded.append(key)
                     #Key
                     else:
                        key = tileType
                        self.cachedDistances[(start, key)] = (iterations, currentKeysNeeded)
                  #If we got this far without a continue, we're on a clear tile
                  newTiles.add(testTile)
                  exploredTiles[testTile] = currentKeysNeeded
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
         
   def GetStartPos(self):
      for y in xrange(self.height):
         for x in xrange(self.width):
            if self.GetCharacterAt((x,y))==START:
               return (x,y)
               
               
   def GetPositionOfCharacter(self, c):
      for y in xrange(self.height):
         for x in xrange(self.width):
            if self.GetCharacterAt((x,y))==c:
               return (x,y)
               
   def GetNumKeys(self):
      return len(self.keyPositions)
         
        
   def FindShortestPath(self):
      numKeys = self.GetNumKeys()
      
      #state vector, position
      startState = PathState()
      startState.keys = set()
      startState.positions = ['1','2','3','4']
      
      currentStates = {}
      currentStates[startState] = 0
      
      for i in xrange(numKeys):
         print str(i) + ": " + str(len(currentStates))
            
         newStates = {}
         for state in currentStates:
            distance = currentStates[state]
            for botIdx in xrange(NUM_BOTS):
               for key in self.keysForBot[botIdx]:
                  if key in state.keys:
                     continue
                     
                  distToKey, requiredKeys = self.cachedDistances[(state.positions[botIdx], key)]
                  
                  hasNeededKeys = True
                  for reqKey in requiredKeys:
                     if reqKey not in state.keys:
                        hasNeededKeys = False
                        break
                        
                  if not hasNeededKeys:
                     continue
                  
                  newState = PathState()
                  #copy data, add new stuff
                  newState.keys = state.keys.copy()
                  newState.keys.add(key)
                  if len(newState.keys) < i+1:
                     print "uh oh"
                     print state.keys
                     print key
                  newState.positions = state.positions[:]
                  newState.positions[botIdx] = key
                  newDistance = distance + distToKey
                  
                  if newState in newStates:
                     oldDistance = newStates[newState]
                     if newDistance < oldDistance:
                        newStates[newState] = newDistance
                  else:
                        newStates[newState] = newDistance
         currentStates = newStates
      for state in currentStates:
         print str(state.keys) + " " + str(state.positions) + " " + str(currentStates[state])
      shortestState = None
      shortestDistance = 999999999
      for state in currentStates:
         if currentStates[state] < shortestDistance:
            shortestDistance = currentStates[state]
            shortestState = state
      print shortestDistance
      

mapData = MapData()
mapStr = ""
with open("input.txt", "r") as FILE:
   mapStr = FILE.read()
   
#mapStr = 
"""#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######"""
mapData.FromString(mapStr)
   

print mapData.ToString()
mapData.FillGaps()
print " "
print mapData.ToString()
#print mapData.cachedDistances[('@','m')]
"""startPos = mapData.GetStartPos()
keySet = set()
keySet.add('a')
keySet.add('f')
keySet.add('z')
keySet.add('i')
print mapData.GetReachableKeysFromPosition(keySet, startPos)"""
mapData.FindShortestPath()